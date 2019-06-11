import sys, datetime
import matplotlib
#matplotlib.use('Agg')
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
	fontsize = 28
	csfont = {'fontname':'Times New Roman'}

	f = open(filename)
	data,t = parse_file(f,3	)


	sublength_begin = 0#len(data2)-100
	sublength_end =  len(data)

	plt.plot(t[sublength_begin:sublength_end],data[sublength_begin:sublength_end],label="Switch1 vs. Switch2", linewidth=1.3)


	plt.ylabel("Sequence Number",fontsize=fontsize, **csfont)
	plt.xlabel("Time", fontsize=fontsize-4, **csfont)  
	plt.tick_params(labelsize=16)
    #	axis='x',          # changes apply to the x-axis
    #	which='both',      # both major and minor ticks are affected
    # 	labelbottom=False) # labels along the bottom edge are off
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
	plt.show()
	#print(out_plot)
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

