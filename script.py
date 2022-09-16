import json
import os
import time
from modified_simulation import *

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

	result_dict = {}

	for i in range(0, len(traces)):
		trace = traces[i]

		simulate_trace(trace, result_dict, i)

	result_file_name = file_name + "_" + str(MAX_BUFFLEN) + "_" + abr + "_result.json"
	
	with open(result_file_name, 'w') as fout:
		json.dump(result_dict, fout)

def simulate_trace(trace, result_dict, i):
	# print("Trace:", i, "Bufflen:", MAX_BUFFLEN)
	try:
		result = simulation(trace)

		result_dict[trace] = result
	except Exception as e:
		print(e)

file_name = sys.argv[1]
main(file_name)