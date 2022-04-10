# SIMULATION 1.0
import math, sys, collections
from config import *
from helpers import *
from chunkMap import *
from algorithms import *
import numpy as np
import collections
import statistics


def getDynamicconfig_bola(pv_list, bw, std, step):
    bw_step = step
    std_step = step
    ABRAlgo = ''
    bw_cut =int(float(bw)/bw_step)*bw_step
    std_cut = int(float(std)/std_step)*std_step
    abr_list = list()
    current_list = list()
    count = 0
    if True:
        if bw==-1 and std==-1:
            return 'BOLA', 0.0, 0.0, 0.0
        # if key not in performance vector
        if (bw_cut, std_cut) not in pv_list.keys():
            for i in range(2, 1000, 1):
                count += 1
                for bw_ in [bw_cut - (i - 1) * bw_step, bw_cut + (i-1) * bw_step]:
                    for std_ in range(std_cut - (i - 1) * std_step, std_cut + (i-1) * std_step + std_step, std_step):
                        if (bw_, std_) in pv_list.keys():
                            current_list = current_list + pv_list[(bw_, std_)]
                for std_ in [std_cut - (i - 1) * std_step, std_cut + (i-1) * std_step]:
                    for bw_ in range(bw_cut - (i - 2) * bw_step, bw_cut + (i-1) * bw_step, bw_step):
                        if (bw_, std_) in pv_list.keys():
                            current_list = current_list + pv_list[(bw_, std_)]
                if len(current_list)==0:
                    continue
                else:# len(abr_list)>0 and 'BB' not in abr_list:
                    ABRAlgo = 'BOLA'
                    break
        else:
            current_list = current_list + pv_list[(bw_cut, std_cut)]
            ABRAlgo = 'BOLA'

    if len(current_list)==0:
        return 'BOLA', 0.0, 0.0, 0.0
    if max(current_list) ==-sys.maxint:
        return 'BOLA', 0.0, 0.0, 0.0
    # print >> sys.stderr, ABRAlgo, min(current_list), np.percentile(current_list,50), max(current_list), bw, std
    return ABRAlgo, min(current_list), np.percentile(current_list,50), max(current_list)


def getDynamicconfig_mpc(pv_list_hyb, bw, std, step):
    bw_step = step
    std_step = step
    ABRAlgo = ''
    bw_cut =int(float(bw)/bw_step)*bw_step
    std_cut = int(float(std)/std_step)*std_step
    abr_list = list()
    current_list_1 = list()
    current_list_2 = list()
    current_list_bb_1 = list()
    current_list_bb_2 = list()
    current_list_hyb = list()
    count = 0
    if True:
        if bw==-1 and std==-1:
            return 'MPC', 0.0, 0.0, 0.0
        # if key not in performance vector
        if (bw_cut, std_cut) not in pv_list_hyb.keys():
            for i in range(2, 1000, 1):
                count += 1
                for bw_ in [bw_cut - (i - 1) * bw_step, bw_cut + (i-1) * bw_step]:
                    for std_ in range(std_cut - (i - 1) * std_step, std_cut + (i-1) * std_step + std_step, std_step):
                        if (bw_, std_) in pv_list_hyb.keys():
                            current_list_hyb = current_list_hyb + pv_list_hyb[(bw_, std_)]
                for std_ in [std_cut - (i - 1) * std_step, std_cut + (i-1) * std_step]:
                    for bw_ in range(bw_cut - (i - 2) * bw_step, bw_cut + (i-1) * bw_step, bw_step):
                        if (bw_, std_) in pv_list_hyb.keys():
                            current_list_hyb = current_list_hyb + pv_list_hyb[(bw_, std_)]
                if len(current_list_hyb)==0:
                    continue
                else:# len(abr_list)>0 and 'BB' not in abr_list:
                    ABRAlgo = 'MPC'
                    break
        else:
            current_list_hyb = current_list_hyb + pv_list_hyb[(bw_cut, std_cut)]
            ABRAlgo = 'MPC'

    if len(current_list_hyb)==0:
        return 'MPC', 0.0, 0.0, 0.0
    if max(current_list_hyb) ==-1.0:
        return 'MPC', 0.0, 0.0, 0.0
    return ABRAlgo, min(current_list_hyb), np.percentile(current_list_hyb,50), max(current_list_hyb)


def getDynamicconfig_self(pv_list_hyb, bw, std, step):
    bw_step = step
    std_step = step
    ABRAlgo = ''
    bw_cut =int(float(bw)/bw_step)*bw_step
    std_cut = int(float(std)/std_step)*std_step
    abr_list = list()
    current_list_1 = list()
    current_list_2 = list()
    current_list_bb_1 = list()
    current_list_bb_2 = list()
    current_list_hyb = list()
    count = 0
    #if combination == True:
    if True:
        if bw==-1 and std==-1:
            return 'HYB', 0.25, 0.25, 0.25, 5, 5, 5, 0.4, 0.4, 0.4
        # if key not in performance vector
        if (bw_cut, std_cut) not in pv_list_hyb.keys():
            for i in range(2, 1000, 1):
                count += 1
                for bw_ in [bw_cut - (i - 1) * bw_step, bw_cut + (i-1) * bw_step]:
                    for std_ in range(std_cut - (i - 1) * std_step, std_cut + (i-1) * std_step + std_step, std_step):
                        if (bw_, std_) in pv_list_hyb.keys():
                            #abr_list = abr_list + ABRs[(bw_, std_)]
                            #current_list_bb_1 = current_list_bb_1 + pv_list_bb_1[(bw_, std_)]
                            #current_list_bb_2 = current_list_bb_2 + pv_list_bb_2[(bw_, std_)]
                            current_list_hyb = current_list_hyb + pv_list_hyb[(bw_, std_)]
                for std_ in [std_cut - (i - 1) * std_step, std_cut + (i-1) * std_step]:
                    for bw_ in range(bw_cut - (i - 2) * bw_step, bw_cut + (i-1) * bw_step, bw_step):
                        if (bw_, std_) in pv_list_hyb.keys():
                            #abr_list = abr_list + ABRs[(bw_, std_)]
                            #current_list_bb_1 = current_list_bb_1 + pv_list_bb_1[(bw_, std_)]
                            #current_list_bb_2 = current_list_bb_2 + pv_list_bb_2[(bw_, std_)]
                            current_list_hyb = current_list_hyb + pv_list_hyb[(bw_, std_)]
                if len(current_list_hyb)==0:
                    continue
                else:# len(abr_list)>0 and 'BB' not in abr_list:
                    ABRAlgo = 'HYB'
                    #print "HYB", bw_cut, std_cut, count, sys.argv[1]
                    break
        else:
            #abr_list = ABRs[(bw_cut, std_cut)]
            #current_list_bb_1 = current_list_bb_1 + pv_list_bb_1[(bw_cut, std_cut)]
            #current_list_bb_2 = current_list_bb_2 + pv_list_bb_2[(bw_cut, std_cut)]
            current_list_hyb = current_list_hyb + pv_list_hyb[(bw_cut, std_cut)]
            ABRAlgo = 'HYB'


    #if combination ==True:
    if len(current_list_hyb)==0:
        return 'HYB', 0.25, 0.25, 0.25, 5, 5, 5, 0.4, 0.4, 0.4
    #return ABRAlgo, min(current_list_hyb), statistics.median(current_list_hyb), max(current_list_hyb), 0,0,0,0,0,0
    return ABRAlgo, min(current_list_hyb), np.percentile(current_list_hyb,10), max(current_list_hyb), 0,0,0,0,0,0

def getBWandStd(path, fileName):
  trace = open(path+fileName, 'r')
  bw=[]
  for inputdata in trace:
    if len(inputdata) < 5:
      continue
    bw.append(float(inputdata.split("\n")[0].split(" ")[1]))
    #x = fileName.split(".")[-2].split("/")[-1].split("_")[1]
    #y = fileName.split(".")[-2].split("/")[-1].split("_")[2]
    # for real group, we need to calculate x and y manually
  x = sum(bw)/len(bw)
  y = np.std(bw, ddof=1)
  return x, y


def readPerformanceVerctor():
    #print "reading table"
    bw_step = 100
    std_step = 100
    path = "/home/zahaib/convivaProj/convivaData/fit_trace_0_7500_0_15000/"
    f_vector = "comparison_result_10800_allconfigonly_uppergap.txt"
    lines = open(f_vector).readlines()
    performanceVector_all = dict()
    pv_list = dict()
    cnt = 0
    for l in lines:
        #cnt+=1
        #if cnt%1000 == 0:
        #    print cnt
        l = l.replace(",", "").replace(")", "").replace("(", "").replace("\'", "").rstrip().split(" ")
        #grnd_avgbr = float(l[1])
        #grnd_rebuf = float(l[2])
        sim_avgbr = float(l[1])
        sim_rebuf = float(l[2])
        all_avgbr = float(l[3])
        all_rebuf = float(l[4])
        all_bsm = float(l[6])
        bw_, std_ = getBWandStd(path, l[0])
        performanceVector_all[(int(bw_), int(std_))] = all_bsm

#    pv_list = dict()
#    for key in performanceVector_all.keys():
#        bw = key[0]
#        std = key[1]
        #bsm = performanceVector_all[key]
        bw_cut =int(bw_/bw_step)*bw_step
        std_cut = int(std_/std_step)*std_step
        if (bw_cut, std_cut) not in pv_list.keys():
            pv_list[(bw_cut, std_cut)] = list()

        pv_list[(bw_cut, std_cut)].append(all_bsm)
    #print "reading table done"
    print pv_list
    return pv_list

def getABRChoice(BB_or_HYB, bw, std):
    bw_step = 100
    std_step = 100
    if bw == -1 and std == -1:
        return 'HYB'
    bw_cut =int(float(bw)/bw_step)*bw_step
    std_cut = int(float(std)/std_step)*std_step
    if (bw_cut, std_cut) not in BB_or_HYB.keys():
        #print bw_cut, std_cut
        #return 'HYB'
        if bw_cut < 10000 and float(std) / float(bw) > 0.70:
            return 'BB'
        else:
            return getNearestABR(BB_or_HYB, bw_cut, std_cut, bw_step, std_step)
    #print >> sys.stderr, 'here'
    if 'BB' in BB_or_HYB[bw_cut, std_cut]:
        return 'BB'
    return 'HYB'

def getNearestABR(pv_list, bw_cut, std_cut, bw_step, std_step):
  for i in range(2, 4, 1):
    for bw in range(bw_cut - (i - 1) * bw_step, bw_cut + i * bw_step, bw_step):
      for std in range(std_cut - (i - 1) * std_step, std_cut + i * std_step, std_step):
        if bw == bw_cut and std == std_cut or (bw, std) not in pv_list.keys():
          continue
        if 'BB' in pv_list[bw, std]:
          return 'BB'
  return 'HYB'   
      


def getDynamicconfig_combine(pv_list_hyb, pv_list_bb_1, pv_list_bb_2, ABRs, bw, std, combination):
    bw_step = 300
    std_step = 300
    ABRAlgo = ''
    bw_cut =int(float(bw)/bw_step)*bw_step
    std_cut = int(float(std)/std_step)*std_step
    abr_list = list()
    current_list_1 = list()
    current_list_2 = list()
    current_list_bb_1 = list()
    current_list_bb_2 = list()
    current_list_hyb = list()
    count = 0
    if combination == True:
        if bw==-1 and std==-1:
            return 'BB', 5, 5, 5, 0.4, 0.4, 0.4
        # if key not in performance vector
        if (bw_cut, std_cut) not in ABRs.keys():
            for i in range(2, 1000, 1):
	        count += 1
                for bw_ in [bw_cut - (i - 1) * bw_step, bw_cut + (i-1) * bw_step]:
                    for std_ in range(std_cut - (i - 1) * std_step, std_cut + (i-1) * std_step, std_step):
                        if (bw_, std_) in ABRs.keys():
                            abr_list = abr_list + ABRs[(bw_, std_)]
                            current_list_bb_1 = current_list_bb_1 + pv_list_bb_1[(bw_, std_)]
                            current_list_bb_2 = current_list_bb_2 + pv_list_bb_2[(bw_, std_)]
                            current_list_hyb = current_list_hyb + pv_list_hyb[(bw_, std_)]
                for std_ in [std_cut - (i - 1) * std_step, std_cut + (i-1) * std_step]:
                    for bw_ in range(bw_cut - (i - 2) * bw_step, bw_cut + (i-1) * bw_step, bw_step):
                        if (bw_, std_) in ABRs.keys():
                            abr_list = abr_list + ABRs[(bw_, std_)]
                            current_list_bb_1 = current_list_bb_1 + pv_list_bb_1[(bw_, std_)]
                            current_list_bb_2 = current_list_bb_2 + pv_list_bb_2[(bw_, std_)]
                            current_list_hyb = current_list_hyb + pv_list_hyb[(bw_, std_)]
                if len(abr_list)==0:
                    continue
                elif len(abr_list)>0 and 'BB' in abr_list:
                    ABRAlgo = 'BB'
		    #print "BB", bw_cut, std_cut, count, sys.argv[1]
                    break
                else:# len(abr_list)>0 and 'BB' not in abr_list:
                    ABRAlgo = 'HYB'
		    #print "HYB", bw_cut, std_cut, count, sys.argv[1]
                    break
        else:
            abr_list = ABRs[(bw_cut, std_cut)]
            current_list_bb_1 = current_list_bb_1 + pv_list_bb_1[(bw_cut, std_cut)]
            current_list_bb_2 = current_list_bb_2 + pv_list_bb_2[(bw_cut, std_cut)]
            current_list_hyb = current_list_hyb + pv_list_hyb[(bw_cut, std_cut)]
            if 'BB' in abr_list:
                ABRAlgo = 'BB'
            else: 
                ABRAlgo = 'HYB'
        
    else:
        if bw==-1 and std==-1:
            return 'HYB', 0.25, 0.25, 0.25, 0.25, 0.25, 0.25
        if (bw_cut, std_cut) not in pv_list_hyb.keys():
            for i in range(2, 1000, 1):
                for bw_ in [bw_cut - (i - 1) * bw_step, bw_cut + (i-1) * bw_step]:
                    for std_ in range(std_cut - (i - 1) * std_step, std_cut + (i-1) * std_step, std_step):
                        if (bw_, std_) in pv_list_hyb.keys():
                            current_list_hyb = current_list_hyb + pv_list_hyb[(bw_, std_)]
                for std_ in [std_cut - (i - 1) * std_step, std_cut + (i-1) * std_step]:
                    for bw_ in range(bw_cut - (i - 2) * bw_step, bw_cut + (i-1) * bw_step, bw_step):
                        if (bw_, std_) in pv_list_hyb.keys():
                            current_list_hyb = current_list_hyb + pv_list_hyb[(bw_, std_)]
                if len(current_list_hyb)==0:
                    continue
                else:
                    ABRAlgo = 'HYB'
                    break
        else:
            current_list_hyb = current_list_hyb + pv_list_hyb[(bw_cut, std_cut)]
            ABRAlgo = 'HYB'
    if combination ==True:    
        return ABRAlgo, min(current_list_hyb), statistics.median(current_list_hyb), max(current_list_hyb), min(current_list_bb_1), statistics.median(current_list_bb_1), max(current_list_bb_1), min(current_list_bb_2), statistics.median(current_list_bb_2), max(current_list_bb_2)
    else:
        return ABRAlgo, min(current_list_hyb), statistics.median(current_list_hyb), max(current_list_hyb), 0,0,0,0,0,0
       
#mode 0 : min
#mode 1 : median
#mode 2 : max
def getDynamicconfig(pv_list, bw, std, mode):    
    bw_step = 100
    std_step = 100
    if bw==-1 and std==-1:
        return 0.25, 0.25, 0.25
    bw_cut =int(float(bw)/bw_step)*bw_step
    std_cut = int(float(std)/std_step)*std_step
    if (bw_cut, std_cut) not in pv_list.keys():
        if float(bw) > 10000:
            return 0.97, 0.97, 0.97
        elif float(bw) < 500:
            return 0.01, 0.01, 0.01
        elif float(std)*2 > float(bw):
            return 0.01, 0.01, 0.01
        else:
            return 0.25, 0.25, 0.25
    current_list = pv_list[(bw_cut, std_cut)]
    if len(current_list)==0:
        if float(bw) > 12000:
            return 0.97, 0.97, 0.97
        elif float(bw) < 500:
            return 0.01, 0.01, 0.01
        elif float(std) > float(bw)*2:
            return 0.1, 0.01, 0.01
        else:
            return 0.25, 0.25, 0.25
    else:
        if mode ==0:
            return min(current_list), statistics.median(current_list), max(current_list)
        elif mode ==1:
            return statistics.median(current_list), min(current_list), max(current_list)
        elif mode == 2:
            return max(current_list), statistics.median(current_list), min(current_list)
        else:
            return 0.25, 0.25, 0.25
    return 0.25, 0.25, 0.25


def getDynamicconfigBB_lower(pv_list, bw, std, mode):
    bw_step = 100
    std_step = 100
    if bw==-1 and std==-1:
        return 5, 5, 5
    bw_cut =int(float(bw)/bw_step)*bw_step
    std_cut = int(float(std)/std_step)*std_step
    if (bw_cut, std_cut) not in pv_list.keys():
        if float(bw) > 10000:
            return 1, 1, 1
        elif float(bw) < 500:
            return 75, 75, 75
        elif float(std)*2 > float(bw):
            return 75, 75, 75
        else:
            return 5, 5, 5
    current_list = pv_list[(bw_cut, std_cut)]
    if len(current_list)==0:
        if float(bw) > 12000:
            return 1, 1, 1
        elif float(bw) < 500:
            return 75, 75, 75
        elif float(std) > float(bw)*2:
            return 75, 75, 75
        else:
            return 5, 5, 5
    else:
        if mode ==0:
            return min(current_list), statistics.median(current_list), max(current_list)
        elif mode ==1:
            return statistics.median(current_list), min(current_list), max(current_list)
        elif mode == 2:
            return max(current_list), statistics.median(current_list), min(current_list)
    return 5, 5, 5

def getDynamicconfigBB_upper(pv_list, bw, std, mode):
    bw_step = 100
    std_step = 100
    if bw==-1 and std==-1:
        return 0.4, 0.4, 0.4
    bw_cut =int(float(bw)/bw_step)*bw_step
    std_cut = int(float(std)/std_step)*std_step
    if (bw_cut, std_cut) not in pv_list.keys():
        if float(bw) > 10000:
            return 0.33, 0.33, 0.33
        elif float(bw) < 500:
            return 0.9, 0.9, 0.9
        elif float(std)*2 > float(bw):
            return 0.9, 0.9, 0.9
        else:
            return 0.4, 0.4, 0.4
    current_list = pv_list[(bw_cut, std_cut)]
    if len(current_list)==0:
        if float(bw) > 12000:
            return 0.33, 0.33, 0.33
        elif float(bw) < 500:
            return 0.9, 0.9, 0.9
        elif float(std) > float(bw)*2:
            return 0.9, 0.9, 0.9
        else:
            return 0.4, 0.4, 0.4
    else:
        if mode ==0:
            return min(current_list), statistics.median(current_list), max(current_list)
        elif mode ==1:
            return statistics.median(current_list), min(current_list), max(current_list)
        elif mode == 2:
            return max(current_list), statistics.median(current_list), min(current_list)
    return 0.4, 0.4, 0.4

def findMaxConfig(tups):
    #print tups
    bsm = -1.0
    for tup in tups:
        if bsm < tup[1]:
            bsm = tup[1]
    weight =-1000000.0
    for tup in tups:
        if tup[1]!=bsm:
            continue
        #print tup[0], weight
        if tup[0] > weight:
            weight = tup[0]
        #print tup[0], weight
    return weight, bsm



def dominantconfig(configs):
    #print configs
    old_bitrate = 10000.0
    old_rebuf = 10000.0
    configs_dominant = collections.OrderedDict()

    configs = collections.OrderedDict(sorted(configs.items()))
    for bit in configs.keys():
        configs[bit] = collections.OrderedDict(sorted(configs[bit].items()))

    for bit in reversed(configs.keys()):
        for rebuf in reversed(configs[bit].keys()):
            list_p = list()
            if float(old_bitrate) > float(bit) and float(old_rebuf) > float(rebuf):
                old_bitrate = float(bit)
                old_rebuf = float(rebuf)
                for tup in configs[bit][rebuf]:
                    list_p.append(tup)
            if len(list_p) > 0:
                configs_dominant[(bit, rebuf)] = list_p

    for tup in configs_dominant.keys():
        if tup[1] > 0:
            continue
        else:
            return findMaxConfig(configs_dominant[tup])
    return findMaxConfig(configs_dominant[tup])

