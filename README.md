## Intro
This is a trace driven simulator for Oboe, Bola and HYB. We used a version of this simulator
to test and build Oboe extensively. This simulator is a re-factored version of the
simulator we used for many experiments in the Oboe paper. The refactoring in this version
was done on the following acconts (i) removing experimental code to launch experiments and
(ii) dead code we accumulated due to our various experiments. However, still plenty of 
dead code remains and plenty of other experimental things we tried still remains.

## Setup
The only thing that really needs to be setup is the external change point detection package.
We have not implemented this change point detector. The code for this detector is on
github (https://github.com/hildensia/bayesian_changepoint_detection). We are including
here as well. To install the package do the following steps:

	$> cd bayesian_changepoint_detection-master
	$> python setup.py install 

If you are missing any other Python dependencies, you should be able to get those up by
once running the simulator (described below) and following the missing dependency prompts

## Code

Disclaimer: the code in this simulator is quite messy and bad. We are working to clean this
up and make it easier to understand but the work on it has been slower than expected. 
Unfortunately both Yun and I (Zahaib) got pulled in to other projects soon we published the
Oboe paper and since then have had trouble finding time to clean up this code.

This means that you will  right now encounter bad variable names, inconsistent variable 
naming conventions etc. We apologize for this in advance.

First open config.py to see a host of settings that you can adjust according to your
experiment. you'll find options to select ABR (MPC, Bola, HYB). To activate Oboe on any ABR
set the OBOE_ACTIVE variable to True. Also go through some other settings which you may be
able to recognize from our paper such as the Rebuffering penalty and Bitrate change penalty
used to calculate the QoE. You can play around with these. There are some settings which
you should not change. Those are experimental settings which can mess up your simulation.

The main file that drives the simulation is simulation.py file. This executes the main
simulation loop and prints out the statistics once simulation is complete. You might want
to go through this file to understand how the simulator works. Everything is (unfortunately)
inside one big function.

The vplayer_state.py file mostly contains the data structure which maintain state as the
simulation executes. You can look through it to see what variables are maintained.

algorithms.py is where you will find the implementation of various ABR algorithms. You
will find implementations of BBA algorithms as well. Of those only BBA0 is tested and
usable. BBA1 and BBA2 are buggy, do not use as is.

helpers.py is a file that provides a number of helper functions. The most important
function in this file is called chunksDownloaded(...). You may want to go through this func
as well.

chunkMap.py is just a table of the chunk sizes of the video at its various bitrates.
The chunk sizes are in bytes.

You will also find three files including configmap_hyb_oboe.py, configmap_bola_oboe.py
and configmap_mpc_oboe.py. These files contain the configmaps we have generated which
Oboe uses to reconfigure HYB, BOLA and MPC algorithms. 

simulation_performance_vector.py provides function for Oboe to obtains the best
configuration from the configmap when the TCP connection state change is detected. You
will not need to know much about the code here.

Usage:

	$> python simulation.py <path to trace file>

## Trace Files
Trace files capture available throughput at periodic intervals in time. Each trace file
comprises of two columns. The first colums in the time in milliseconds and the second 
column is the available throughput in kbps. The time gap between each row in the trace
is 1 second. In other words, trace contain bandwidth samples spaced 1 seconds apart.

There are three directories for traces:
	1. dash_generated_trace
	2. test_trace
	3. synthetic_trace_for_configmap

Of these the dash_generated_trace directory contains traces directly captured from
a dash player. The test_trace directory contains a mix of traces captured from
dash player as well as some hand generated traces. We primarily used these traces
to test different changes to the code. The synthetic_trace_for_configmap directory
contains the set of synthetic trace we used to build a ConfigMap (see paper for 
details) 


# topics_project_2
