import sys, datetime
import matplotlib
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
			time_value = float(elements[0])
			data_point = int(round(float(elements[element_id].split(" ")[2].strip())))
			data.append(data_point)
			t.append(time_value)
	return data,t

def plot_seq(filename,out_plot):
	fontsize = 28
	csfont = {'fontname':'Times New Roman'}

	f = open(filename)
	data,t = parse_file(f,2)
	throughput = []
	last_d = 0
	for d in data:
		if last_d == 0:
			last_d = d
			continue
		throughput.append(abs(last_d-d))
		last_d = d

#	plt.title("Growing sequence number over time",fontsize=fontsize, **csfont)
	plt.plot(throughput,label="", linewidth=1.2)
	plt.ylabel("Throughput in Bytes",fontsize=fontsize, **csfont)
	plt.xlabel("Time", fontsize=fontsize, **csfont)  
	plt.xticks(size='large')
	#plt.yticks([0,10000,20000,30000,40000,50000])
	#plt.ylim(-2000,50000)

	ax = plt.axes()
	ax.grid(True)
	ax.xaxis.set_major_formatter(plt.NullFormatter())
	ax.yaxis.set_major_formatter(plt.NullFormatter())
	#legend = plt.legend(loc='upper left',fontsize=18)
	#plt.title(filename[0])
	plt.ioff()
#legend = plt.legend(loc='upper left')
	
	plt.ioff()
	plt.show()
	#plt.savefig(out_plot + "-seq_number.png")	
	f.close()

def main():
	in_filename = sys.argv[1]
	out_plot = "plots/" + str(datetime.datetime.now())

	if len(sys.argv) > 2:
		out_plot = sys.argv[2] 

	plot_seq(in_filename,out_plot)
	#boxplot_seq(in_filename,out_plot)
	exit(0)

if __name__ == '__main__':
	main()

