import json
import os
import time
from modified_simulation import *
import multiprocessing
import threading

def main(abr):
	traces = os.listdir('./synthetic_trace_for_configmap')
	
	abr_dict = {}
	abr_dict["mpc"] = False
	abr_dict["hyb"] = False
	abr_dict["bola"] = False
	abr_dict[abr] = True

	manager = multiprocessing.Manager()
	result_arr = manager.list()
	processes = [None] * len(traces)
	
	for i in range(0, 5):
		print(i)
		trace = traces[i]
		processes[i] = multiprocessing.Process(target=simulate_trace, args=(trace, abr_dict, result_arr, i, ))
		processes[i].start()

	for j in range(0, 5):
		processes[j].join()

	result_file_name = abr + "_" + "result" + ".json"
	
	with open(result_file_name, 'w') as fout:
		json.dump(list(result_arr), fout)

def simulate_trace(trace, abr_dict, result_arr, i):
	BUFFLENS = [2, 4, 6, 8, 10]

	for bufflen in BUFFLENS:
		print("Trace:", i, "Bufflen:", bufflen)
		try:
			result = simulation(trace, bufflen, abr_dict["mpc"], abr_dict["hyb"], abr_dict["bola"])

			if (result["buftime"] == 0):
				result["bufflen"] = bufflen
				result_arr.append(result)
				break

			if (bufflen == 10):
				print("BUFFLENS ARRAY EXCEEDED")
		except Exception as e:
			print(e)
			continue

start = time.time()
print("Doing mpc")
main("mpc")
end = time.time()
print("Time elapsed: ", end - start)
print("Doing hyb")
main("hyb")
print("Doing bola")
main("bola")