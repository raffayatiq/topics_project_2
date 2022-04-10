# LIST OF HELPER FUNCTIONS
import numpy as np
import random, sys
import traceback
import inspect
from algorithms import *
from config import *
from chunkMap import *
from simulation_performance_vector import *
from configmap_hyb_oboe import *
from configmap_mpc_oboe import *
from configmap_bola_oboe import *
import bayesian_changepoint_detection.online_changepoint_detection as oncd
from functools import partial
import timeit

def onlineCD(session_history, chunk_when_last_chd, interval, player_visible_bw):
  chd_detected = False
  chd_index = chunk_when_last_chd
  trimThresh = 1000
  lenarray = len(player_visible_bw)
  player_visible_bw, cutoff = trimPlayerVisibleBW(player_visible_bw, trimThresh)
  R, maxes = oncd.online_changepoint_detection(np.asanyarray(player_visible_bw), partial(oncd.constant_hazard, 250), oncd.StudentT(0.1,0.01,1,0))
  interval = min(interval, len(player_visible_bw))
  changeArray = R[interval,interval:-1]
  for i,v in reversed(list(enumerate(changeArray))): #reversed(list(enumerate(changeArray))): # enumerate(changeArray):
    if v > 0.01 and i + cutoff > chunk_when_last_chd and not (i == 0 and chunk_when_last_chd > -1):
      chd_index = i + cutoff
      chd_detected = True
      break
  return chd_detected, chd_index

def trimPlayerVisibleBW(player_visible_bw, thresh):
  ret = []
  cutoff = 0
  lenarray = len(player_visible_bw)
  if lenarray <= thresh:
    return player_visible_bw, cutoff

  cutoff = lenarray - thresh
  ret = player_visible_bw[cutoff:]
  return ret, cutoff


# function returns the most dominant bitrate played, if two are dominant it returns the bigger of two
def getDominant(dominantBitrate):
  ret = 0
  maxFreq = -sys.maxint
  for b in sorted(dominantBitrate.keys()):
    if maxFreq <= dominantBitrate[b]:
      ret = b
      maxFreq = dominantBitrate[b]
  return ret, maxFreq, sum(dominantBitrate.values())


# function returns the initial bandwidth using the jointime of the session
def printPercentile(target):
  for i in range (0,101):
    print str(i/float(100)) + "\t" + str(np.percentile(target, i))
    
def getInitBWCalculated(init_br, jointime, chunksize):
  return int(init_br * chunksize / float(jointime) * 1000)

def getInitBW(bw_array):
  return bw_array[0][1]

# update session history because a chunk just finished downloading
def updateSessionHistory(bitrate, clock, chunkid, CHUNKSIZE, session_history, first_chunk, time_residue, attempt_id, completed, chunk_residue):
  #print "update sessionshistory"
  if CHUNK_AWARE_MODE and bitrate in size_envivo:
    bitrate = size_envivo[bitrate][chunkid] * 8
  
  time_residue = max(0, time_residue - SIMULATION_STEP)

  if first_chunk:
    size = bitrate * CHUNKSIZE * (1 - 1.25/5.0)
  elif completed == False:
    size = bitrate * CHUNKSIZE * chunk_residue
  else:
    size = bitrate * CHUNKSIZE
  session_history[attempt_id].append(clock)
  session_history[attempt_id].append(bitrate)
  session_history[attempt_id].append(chunkid)
  session_history[attempt_id].append(completed)
  session_history[attempt_id + 1] = [clock  + time_residue]
  return session_history

# getBWFeaturesWeighted with player visible BW
def getBWFeaturesWeightedPlayerVisible(player_visible_bw, chunk_when_last_chd_ran):
  lookbackwindow = len(player_visible_bw) - min(51, len(player_visible_bw) - chunk_when_last_chd_ran)
  currentstateBWArray = player_visible_bw[lookbackwindow:]
  return np.mean(currentstateBWArray), np.std(currentstateBWArray)

# inserts the jointime and bandwidth as an additional timestamp and bandwidth  
def insertJoinTimeandInitBW(ts, bw, bw_array):
  t = []
  t.append(ts)
  b = []
  b.append(bw)
  row = zip(t,b)
  bw_array = row + bw_array
  return bw_array

# funtion returns the time it will take to download a single chunk whether downloading a new chunk or finishing up a partial chunk
def timeToDownloadSingleChunk(CHUNKSIZE, bitrate, BW, chunk_residue, chunkid):
  if BW == 0:
    return 1000000 # one thousand seconds, very large number
  if CHUNK_AWARE_MODE and bitrate in size_envivo:
    bitrate = size_envivo[bitrate][chunkid] * 8
  return round((bitrate  - bitrate  * chunk_residue)/float(BW),2)

# function returns the remaining time to finish the download of the chunk
def timeRemainingFinishChunk(chunk_residue, bitrate, bandwidth, chunkid, chunksize):
  if CHUNK_AWARE_MODE and bitrate in size_envivo:
    bitrate = size_envivo[bitrate][chunkid]*8

  #bandwidth = bandwidth / 2.0
  ret = (1 - chunk_residue) * ((bitrate ) / float(bandwidth))
  return ret

# function returns the past 5 BW samples
def getPastFiveBW(session_history, chunkid):
  past_five = list()
  start = max(chunkid - 5 + 1, 0)
  for i in range(start, chunkid + 1):
    bw_sample = (session_history[i][2] / 8) / (float(session_history[i][1] - session_history[i][0])) / 1000.0 # KBytes/ms or MBytes/sec
    past_five.append(bw_sample)
  return past_five

# function returns the BW needed by MPC
def getMPCBW(session_history, bandwidthEsts, pastErrors, chunkid, discount):
  curr_error = 0
  if len(bandwidthEsts) > 0:
    last_chunk_bw = (session_history[chunkid][2] / 8) / float(session_history[chunkid][1] - session_history[chunkid][0]) / 1000.0 # KBytes/ms or MBytes/sec
    curr_error = abs(bandwidthEsts[-1] - last_chunk_bw) / float(last_chunk_bw)
  pastErrors.append(curr_error)
  past_five = getPastFiveBW(session_history, chunkid)
  bandwidth_sum = 0
  for past_val in past_five:
      bandwidth_sum += (1/float(past_val))
  harmonic_bandwidth = 1.0/(bandwidth_sum/len(past_five))
  bandwidthEsts.append(harmonic_bandwidth)

  max_error = 0

  if discount < 0:
  #### Original code start ####
    error_pos = -5
    if ( len(pastErrors) < 5 ):
      error_pos = -len(pastErrors)
    max_error = float(max(pastErrors[error_pos:]))
    future_bandwidth = harmonic_bandwidth/(1+max_error)
  #### Original code end.. ####
  else:
    max_error = discount / 100.0
    future_bandwidth = harmonic_bandwidth/(1+max_error)
  future_bandwidth = future_bandwidth * 8 * 1000.0 # converted to kbps
  return future_bandwidth, max_error, bandwidthEsts, pastErrors

def chunksDownloaded(s, param, time_prev):
  # declaring local variables which do not need to be updated in the state
  chunk_count = 0.0
  time_residue_this_interval = 0.0
  completion_time_stamps = []
  bitrate = s.BR
  bitrate_at_interval_start = bitrate
  bitrate_at_interval_end = bitrate
  next_chunk_bitrate = -2
  time_curr, chunkid, bandwidth, attempt_id = s.CLOCK, s.CHUNKS_DOWNLOADED, s.BW, s.ATTEMPT_ID

  if CHUNK_AWARE_MODE:
    bitrate = getRealBitrate(bitrate_at_interval_start, chunkid, CHUNKSIZE)
  # first add the residue time from the previous interval
  time_prev += s.chunk_sched_time_delay
  time2FinishResidueChunk = (((1 - s.chunk_residue) * bitrate)/float(bandwidth))
  time2DownloadFullChunk = (bitrate /float(bandwidth))
  # if there is a residue chunk from the last interval, then handle it first
  if s.chunk_residue > 0 and time_prev + time2FinishResidueChunk <= time_curr:
    chunk_count +=  1 - s.chunk_residue
    completionTime = time_prev + time2FinishResidueChunk
    completion_time_stamps.append(completionTime)
    nextChunkDelay = getRandomDelay(bitrate, chunkid, CHUNKSIZE, s.BLEN)
    time_prev += time2FinishResidueChunk + nextChunkDelay
    ## update session_history here, since a chunk finished download
    s.session_history = updateSessionHistory(bitrate_at_interval_start, completionTime, chunkid, CHUNKSIZE, s.session_history, s.first_chunk,
                                              nextChunkDelay, attempt_id, True, s.chunk_residue)
    
    # update calculate of avg bitrate
    s.AVG_SESSION_BITRATE += VIDEO_BIT_RATE[bitrate_at_interval_start] * CHUNKSIZE * 1000.0

    est_bandwidth = est_std = 0
    # if online change point detection is enabled, run the change detection and find the configuration
    if OBOE_ACTIVE:
      # CD_INTERVAL is window size for change detection, defined in config
      ch_detected, ch_index = onlineCD(s.session_history, s.chunk_when_last_chd_ran, CD_INTERVAL, s.player_visible_bw)
      est_bandwidth, est_std = getBWFeaturesWeightedPlayerVisible(s.player_visible_bw, ch_index)
      if ch_detected:
        s.chunk_when_last_chd_ran = ch_index
        #s.gradual_transition = nsteps
        if HYB_ABR:
          dict_name_backup = "configmap_hyb_oboe_"+str(s.minCellSize)
          performance_t = (globals()[dict_name_backup])
          ABRChoice, p1_min, p1_median, p1_max, p2_min, p2_median, p2_max,p3_min, p3_median, p3_max = getDynamicconfig_self(performance_t, est_bandwidth, est_std, s.minCellSize)
          param = p1_min
        elif MPC_ABR:
          dict_name_backup = "configmap_mpc_oboe_"+str(s.minCellSize)
          performance_t = (globals()[dict_name_backup])
          ABRChoice, disc_min, disc_median, disc_max = getDynamicconfig_mpc(performance_t, est_bandwidth, est_std, s.minCellSize)
          param = disc_median
        elif BOLA_ABR:
          dict_name_backup = "configmap_bola_oboe_"+str(s.minCellSize)
          performance_t = (globals()[dict_name_backup])
          ABRChoice, bola_gp_min, bola_gp_median, bola_gp_max = getDynamicconfig_bola(performance_t, est_bandwidth, est_std, s.minCellSize)
          param = bola_gp_max

    if MPC_ABR:
      future_bandwidth, s.max_error, s.bandwidthEsts, s.pastErrors = getMPCBW(s.session_history, s.bandwidthEsts, s.pastErrors, chunkid, param)
      bitrateMPC = getMPCDecision(s.BLEN, bitrate_at_interval_start, chunkid, CHUNKSIZE, future_bandwidth, s.windowSize)
      bitrate_at_interval_end = bitrateMPC
    elif HYB_ABR:
      bitrateDASH = getUtilityBitrateDecision_dash(s.session_history, chunkid, chunkid+1, s.BLEN+CHUNKSIZE, param)
      bitrate_at_interval_end = bitrateDASH
    elif BOLA_ABR:
      bitrateBOLA = getBOLADecision(s.BLEN + CHUNKSIZE, param, s.bola_vp)
      bitrate_at_interval_end = bitrateBOLA

    s.change_magnitude += abs(VIDEO_BIT_RATE[bitrate_at_interval_end] - VIDEO_BIT_RATE[bitrate_at_interval_start])
    chunkid+=1

    # Selecting the bitrate after adding the delay.
    s.configsUsed.append((time_curr/1000.0, s.active_abr, bandwidth, int(est_bandwidth), int(est_std), param, round(s.chunk_residue,2), round(s.BLEN,2), chunkid-1, bitrate_at_interval_end, round(s.BUFFTIME,2)))
    # residue chunk is complete so now move to next chunkid and get the actual bitrate of the next chunk
    if CHUNK_AWARE_MODE:
      bitrate = getRealBitrate(bitrate_at_interval_end, chunkid, CHUNKSIZE)
    bandwidth = max(interpolateBWInterval(time_prev, s.used_bw_array, s.bw_array),0.01)
    attempt_id += 1
    time2DownloadFullChunk = (bitrate /float(bandwidth))
     
  # loop untill chunks can be downloaded in the interval, after each download add random delay
  while time_prev + time2DownloadFullChunk <= time_curr:
    chunk_count += 1
    completionTime = time_prev + time2DownloadFullChunk
    completion_time_stamps.append(completionTime)
    nextChunkDelay = getRandomDelay(bitrate, chunkid, CHUNKSIZE, s.BLEN)
    time_prev += time2DownloadFullChunk + nextChunkDelay
    ## update session_history here, since a chunk finished download
    s.session_history = updateSessionHistory(bitrate_at_interval_end, completionTime, chunkid, CHUNKSIZE, s.session_history, s.first_chunk,
                                              nextChunkDelay, attempt_id, True, s.chunk_residue)
    if CHUNK_AWARE_MODE:
      bitrate = getRealBitrate(bitrate_at_interval_end, chunkid, CHUNKSIZE)
    bandwidth = max(interpolateBWInterval(time_prev, s.used_bw_array, s.bw_array),0.01)
    chunkid += 1
    attempt_id += 1
    time2DownloadFullChunk = (bitrate /float(bandwidth))
  # if there is still some time left, download the partial chunk  
  if time_prev < time_curr:
    chunk_count += bandwidth/(float(bitrate)) * (time_curr - time_prev)
  # if the delay was enough to make time_prev greater than time_curr then we need to transfer over the remaining delay to next interval
  if time_prev >= time_curr:
    time_residue_this_interval = time_prev - time_curr
  s.numChunks = chunk_count
  s.chunk_sched_time_delay = time_residue_this_interval
  s.BR = bitrate_at_interval_end
  if bitrate_at_interval_start != bitrate_at_interval_end:
    s.oldBR = bitrate_at_interval_start
  return s, param


def getRandomDelay(bitrate, chunkid, CHUNKSIZE, BLEN):
  return 87
  chunksizeBytes = getChunkSizeBytes(bitrate, chunkid, CHUNKSIZE)
  zero = 0.0
  five = 0.00002 * chunksizeBytes + 34.8
  twentyfive = 0.0003 * chunksizeBytes - 107.71
  fifty = 0.0007 * chunksizeBytes - 287.3
  seventyfive = 0.0009 * chunksizeBytes - 239.42
  lower = min(five, BLEN * 1000)
  upper = max(min(twentyfive, BLEN * 1000),0)
  #if upper < 0:
  #  upper = 0
  #if lower == upper:
  #  return 0
  #return random.randint(int(zero), int(upper))
  #return twentyfive
  #print chunksizeBytes, upper
  return upper

# function return the actual size of a chunk in bits
def getChunkSizeBytes(bitrate, chunkid, CHUNKSIZE):
  ret = (bitrate * CHUNKSIZE * 1000) / 8
  if CHUNK_AWARE_MODE and bitrate in size_envivo:
    ret = size_envivo[bitrate][chunkid]
  return ret

# function returns the actual bitrate of the label bitrate and the specific chunk
def getRealBitrate(bitrate, chunkid, CHUNKSIZE):
  ret = bitrate
  #print bitrate, chunkid
  if CHUNK_AWARE_MODE and bitrate in size_envivo and chunkid <len(size_envivo[bitrate]):
    ret = size_envivo[bitrate][chunkid]*8
  return ret

# function return the actual size of a chunk in bits
def getChunkSizeBits(bitrate, chunkid, CHUNKSIZE):
  ret = bitrate * CHUNKSIZE * 1000
  if CHUNK_AWARE_MODE and bitrate in size_envivo:
    ret = size_envivo[bitrate][chunkid] * 8
  return ret
  
# function returns interpolated bandwidth at the time of the heartbeat
def interpolateBWInterval(time_heartbeat, used_bw_array, bw_array):
    try:
        if time_heartbeat == bw_array[-1][0]:
            return bw_array[-1][1]
    except TypeError:
        print used_bw_array, bw_array
        sys.exit()

    time_prev, time_next, bw_prev, bw_next = findNearestTimeStampsAndBandwidths(time_heartbeat, used_bw_array, bw_array) # time_prev < time_heartbeat < time_next
    intervalLength = time_next - time_prev
    try:
        aa = int((intervalLength - (time_heartbeat - time_prev))/float(intervalLength) * bw_prev + (intervalLength - (time_next - time_heartbeat))/float(intervalLength) * bw_next)
    except ZeroDivisionError:
        print >> sys.stderr, "Divide by zero error, exiting..." + sys.argv[1], time_heartbeat, time_prev, time_next, inspect.stack()[1][3]
        sys.exit()
    return int((intervalLength - (time_heartbeat - time_prev))/float(intervalLength) * bw_prev + (intervalLength - (time_next - time_heartbeat))/float(intervalLength) * bw_next)

def estimateBWPrecisionServerStyleSessionHistory(time_heartbeat, BLEN, used_bw_array, session_history, chunkid, bw_array):  
  #print chunkid, session_history
  if chunkid - 2 not in session_history.keys() and chunkid - 1 in session_history.keys():
    return session_history[chunkid - 1][2] / (float(session_history[chunkid - 1][1] - session_history[chunkid - 1][0]) / 1000.0)
  
  if chunkid - 2 not in session_history.keys() and chunkid - 1 not in session_history.keys():
    return interpolateBWInterval(time_heartbeat, used_bw_array, bw_array)

  start_1 = session_history[chunkid - 1][0]
  end_1 = session_history[chunkid - 1][1]
  size_1 = session_history[chunkid - 1][2]
  bw_1 = size_1 / (float(end_1 - start_1) / 1000.0)

  start_2 = session_history[chunkid - 2][0]
  end_2 = session_history[chunkid - 2][1]
  size_2 = session_history[chunkid - 2][2]
  bw_2 = size_1 / (float(end_2 - start_2) / 1000.0)
  #if time_prev_prev == 0:
  #  return interpolateBWInterval(time_heartbeat, used_bw_array)
  if BLEN < 10:
    return min(bw_1, bw_2)

  return (bw_1 + bw_2)/2

# function returns the nearest timestamps and bandwidths to the heartbeat timestamp
def findNearestTimeStampsAndBandwidths(time_heartbeat, used_bw_array, bw_array):
  time_prev, time_next, bw_prev, bw_next = 0, 0, 0, 0
  if len(used_bw_array) > 1 and time_heartbeat > bw_array[len(bw_array) - 1][0]:
    bw_next = pickRandomFromUsedBW(used_bw_array)
    time_next = time_heartbeat
  for i in range(0, len(bw_array)):
    if bw_array[i][0] < time_heartbeat:
      time_prev = bw_array[i][0]
      bw_prev = bw_array[i][1]
  for i in range(len(bw_array) - 1, -1, -1):
    if bw_array[i][0] > time_heartbeat:
      time_next = bw_array[i][0]
      bw_next = bw_array[i][1]
  return time_prev, time_next, bw_prev, bw_next

# function just returns a bandwidth randomly form the second half of the session
def pickRandomFromUsedBW(used_bw_array):
  return used_bw_array[random.randint(len(used_bw_array)/2 ,len(used_bw_array) - 1)]
  
def getTrueBW(clock, currBW, stepsize, decision_cycle, bw_array, used_bw_array, sessiontimeFromTrace):
  ret = currBW
  num = 1.0
  for c in range(clock + stepsize, int(min(clock + decision_cycle + stepsize, sessiontimeFromTrace)), stepsize):
    ret += interpolateBWInterval(c, used_bw_array, bw_array)
    num += 1.0

  return ret / num 
