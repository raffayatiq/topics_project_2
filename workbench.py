import os
traces = os.listdir("./" + "synthetic_trace_for_configmap")
traces_of_interest = []

for trace in traces:
	avg_bandwidth = trace.split("_")[1]
	
	if (int(avg_bandwidth) <= 5000):
		traces_of_interest.append(trace)

file_counter = 1
current_file = "trace_set_" + str(file_counter) + ".txt"
trace_set = [traces_of_interest[0]]
trace_counter = 0 # set to 0 since there are 3601 traces, and this will make it 3600 traces to process in the loops, which gives a nice 900 traces per trace_set to deal with

for i in range(1, len(traces_of_interest)):
	trace_set.append(traces[i])
	trace_counter += 1

	if (trace_counter % 900 == 0 and trace_counter != 0):
		with open(current_file, 'w') as file:
			file.write("\n".join(trace_set))

		trace_counter = 0
		trace_set = []
		file_counter += 1
		current_file = "trace_set_" + str(file_counter) + ".txt"

