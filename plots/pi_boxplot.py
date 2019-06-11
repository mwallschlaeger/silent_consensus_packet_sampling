import sys, datetime
import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def parse_file(file_pointer,element_id):
	'''
	parses file
	file_pointer ...
	element_id ...
	return value list , timestamp list
	'''
	t = []
	data = []
	for row in file_pointer:
		r= row.strip()
		elements = r.split(',')
		connection =  elements[1].split(" ")[2].strip()
		if connection.endswith(":1935"):
			data_point = float(elements[element_id].split(" ")[2].strip()) * 100
			data.append(data_point)
	return data

def boxplot_seq(filename,out_plot):
	f = open(filename)
	data,t = parse_file(f,2)
	plt.boxplot(data,notch=0, sym='+', vert=1, whis=1.5)
	plt.ylabel("seq num percent")
	plt.xlabel("connection_a")  
	#legend = plt.legend(loc='upper left')
	plt.ioff()
	plt.savefig(out_plot + "-forecast_precision.png")	
	f.close()

def plot_seq(filename,out_plot):
	f = open(filename)
	data,t = parse_file(f,2)
	plt.plot(t,data,label="Growing Sequence Number", linewidth=1.0)
	plt.ylabel("seq_num")
	plt.xlabel("time")  
	legend = plt.legend(loc='upper left')
	plt.ioff()
	plt.savefig(out_plot + "-seq_number.png")	
	f.close()

def main():
	file_prefix="/home/mwall/huawei/seq-paper/logs/paper-eval-forecasting"
	resolution = "4k"
	hosts = ["router","server","client"]
	#conf = "1_2_2"


	CONFIGURATIONS = ["1_2_2",
					"1_2_1",
					"1_3_1",
					"1_3_2",
					"1_5_1",
					"1_5_2",
					"2_2_2",
					"2_2_1",
					"2_3_1",
					"2_3_2",
					"2_5_1",
					"2_5_2",
					"5_2_2",
					"5_2_1",
					"5_3_1",
					"5_3_2",
					"5_5_1",
					"5_5_2",
					"10_2_2",
					"10_2_1",
					"10_3_1",
					"10_3_2",
					"10_5_1",
					"10_5_2"]


	_4k = []
	_hd = []
	_480p = []

	for conf in CONFIGURATIONS:
		for host in hosts:
			f = open(file_prefix + "/" + host + "_" + "4k" + "_" + conf + ".log" )
			_4k += parse_file(f,5) 
			f.close()


		for host in hosts:
			f = open(file_prefix + "/" + host + "_" + "hd" + "_" + conf + ".log" )
			_hd += parse_file(f,5) 
			f.close()


		for host in hosts:
			f = open(file_prefix + "/" + host + "_" + "480p" + "_" + conf + ".log" )
			_480p += parse_file(f,5) 
			f.close()

		data = [_4k,_hd,_480p]

		ti = np.arange(0.01, 20.0, 0.01)
		plt.semilogy(ti, np.exp(-ti/5.0))

		plt.boxplot(data)
		plt.xticks([1,2,3],["4k","hd","480p"])
		plt.savefig("pi_boxplot_" + '_' + conf + "_" + "logarithm" +".png")	
		plt.close()

	exit(0)

if __name__ == '__main__':
	main()

