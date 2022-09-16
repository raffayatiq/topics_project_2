"""
    This config file has a range of configuration variables including the usage
    player buffer length in seconds, the active ABR, the specifics of the video 
    being simulated and ABR specific configurations. You can activate/deactivate
    Oboe on a selected ABR by setting OBOE_ACTIVE variable to True/False.

    This version of the simulator only works for a partciular video we used in the
    Oboe paper. Chaning the video would require generating the corresponding map
    of chunks (chunkmap) as well regeneration of various Oboe tools. Generation
    of the table requires additional scripts which are not provided with this
    simulator. We are going to try to release those scripts but are constrained
    by time other work.
"""
import math

### Player settings
MAX_BUFFLEN = 20

### Select ABR to simulate
MPC_ABR = False
HYB_ABR = False
BOLA_ABR = True

### Video settings
TOTAL_CHUNKS = 49
NUM_BITRATES = 6
VIDEO_BIT_RATE = [300,750,1200,1850,2850,4300]
VIDEO_BIT_RATE_TO_INDEX = {300:0,750:1,1200:2,1850:3,2850:4,4300:5}
CHUNKSIZE = 4.0

### QoE metric settings
REBUF_PENALTY = 4.3
SMOOTH_PENALTY = 0.0

### BB settings
conf = {'maxbuflen':120, 'r': 5, 'maxRPct':0.50, 'xLookahead':50}

### MPC settings
MPC_WINDOWSIZE = 5

### BOLA settings
MINIMUM_BUFFER_S = 10 #10 # BOLA should never add artificial delays if buffer is less than MINIMUM_BUFFER_S. Orig val: 10
BUFFER_TARGET_S = 30 # If Schedule Controller does not allow buffer level to reach BUFFER_TARGET_S, this can be a virtual buffer level. Orig val: 30
REBUFFER_SAFETY_FACTOR = 0.5 # Used when buffer level is dangerously low, might happen often in live streaming.
BOLA_BITRATES = [br * 1000.0 for br in VIDEO_BIT_RATE]
BOLA_UTILITIES = [math.log(br) for br in BOLA_BITRATES]

### OBOE activation
# set OBOE_ACTIVE to True to augment the ABR with Oboe
OBOE_ACTIVE = False

### debug settings
DEBUG = False
#VERBOSE_DEBUG = False
#CHUNK_DEBUG = False

### chunkmap settings
CHUNK_AWARE_MODE = True



# Only change any of the config below if you really know what you are doing,
# otherwise your simulations are likely to get messed up.

### simulation settings
SIMULATION_STEP = 50
VALIDATION_MODE = False
ESTIMATED_BANDWIDTH_MODE = True
INDUCE_BW_ERROR = False

### Operation mode
CONFIGMAP_GENERATION_MODE = False

## chunk interunption
ALLINTERUPT = False
SMARTINTERUPT = False
NOINTERUPT = True

## other misc settings
LOCK = 0
DASH_BUFFER_ADJUST = True
CD_INTERVAL = 5
