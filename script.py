import json
import os
import time
from modified_simulation import *
import multiprocessing
import threading

def main(file_name):
	file = open(file_name, "r")
	traces = file.read().split("\n")
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
	
	# try:
	# 	result_file = open(folder_name + "_" + str(MAX_BUFFLEN) + "_" + abr + "_result.json" + )
	# 	previous_results = json.load(result_file)
	# 	result_dict.update(previous_results)
	# except:
	# 	pass

	for i in range(0, len(traces)):
		# print(i)
		trace = traces[i]

		# check if the trace already exists in result i.e. min buflen for that trace has been found
		if result_dict.has_key(trace):
			print(trace + " min buflen already found.")
			continue

		processes[i] = multiprocessing.Process(target=simulate_trace, args=(trace, result_dict, i, ))
		processes[i].start()

	for j in range(0, len(traces)):
		if not processes[j] is None:
			processes[j].join()

	result_file_name = file_name + "_" + str(MAX_BUFFLEN) + "_" + abr + "_result.json"
	
	with open(result_file_name, 'w') as fout:
		json.dump(dict(result_dict), fout)

def simulate_trace(trace, result_dict, i):
	# print("Trace:", i, "Bufflen:", MAX_BUFFLEN)
	try:
		result = simulation(trace)

		result_dict[trace] = result
	except Exception as e:
		print(e)

file_name = sys.argv[1]
main(file_name)