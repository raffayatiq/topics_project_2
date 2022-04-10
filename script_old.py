import json
import os
import time
from modified_simulation import *
import multiprocessing
import threading

def main(step_size):
	traces = os.listdir('./synthetic_trace_for_configmap')
	abr = None

	if MPC_ABR:
		abr = "mpc"
	elif HYB_ABR:
		abr = "hyb"
	elif BOLA_ABR:
		abr = "bola"

	manager = multiprocessing.Manager()
	result_dict = manager.dict()
	processes = [None] * len(traces)
	
	try:
		result_file = open(abr + "_result.json")
		previous_results = json.load(result_file)
		result_dict.update(previous_results)
	except:
		pass

	for i in range(0, len(traces), step_size):
		print(i)
		trace = traces[i]

		# check if the trace already exists in result i.e. min buflen for that trace has been found
		if result_dict.has_key(trace):
			print(trace + " min buflen already found.")
			continue

		processes[i] = multiprocessing.Process(target=simulate_trace, args=(trace, result_dict, i, ))
		processes[i].start()

	for j in range(0, len(traces), step_size):
		if not processes[j] is None:
			processes[j].join()

	result_file_name = abr + "_" + "result" + ".json"
	
	with open(result_file_name, 'w') as fout:
		json.dump(dict(result_dict), fout)

def simulate_trace(trace, result_dict, i):
	print("Trace:", i, "Bufflen:", MAX_BUFFLEN)
	try:
		result = simulation(trace)

		if (result["buftime"] == 0):
			result["bufflen"] = MAX_BUFFLEN
			result_dict[trace] = result
	except Exception as e:
		print(e)

step_size = int(sys.argv[1])
main(step_size)