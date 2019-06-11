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

	f = open(filename[0])
	ei,__ = parse_file(f,4)

	f = open(filename[0])
	z,t = parse_file(f,6)

	f = open(filename[1])
	z2,t = parse_file(f,6)

	f = open(filename[2])
	z3,t = parse_file(f,6)
	
	
	diff1 = []
	diff2 = []
	diff3 = []

	for i in range(len(z2)):
		a = abs(z[i]-z2[i])
		b = abs(z[i]-z3[i])
		c = abs(z2[i]-z3[i])

		# client vs server
		diff1.append(a)
		diff2.append(b)
		diff3.append(c)


	sublength_begin = 0#len(data2)-100
	sublength_end =  len(z2)

	plt.plot(t[sublength_begin:sublength_end],diff2[sublength_begin:sublength_end],label="Switch1 vs. Switch2", linewidth=1.2)

	plt.plot(t[sublength_begin:sublength_end],diff1[sublength_begin:sublength_end],label="Switch1 vs. Switch3 ", linewidth=1.2)
	#plt.plot(t[sublength_begin:sublength_end],ei[sublength_begin:sublength_end],label="Forecasting Error", linewidth=0.8,alpha=0.6, color='grey')

	plt.ylabel("Sequence Number Error",fontsize=fontsize, **csfont)
	plt.xlabel("Interval Steps", fontsize=fontsize-4, **csfont)  
	plt.tick_params(labelsize=16)
    #	axis='x',          # changes apply to the x-axis
    #	which='both',      # both major and minor ticks are affected
    # 	labelbottom=False) # labels along the bottom edge are off
	plt.xticks(size='large')
	plt.yticks([0,10000,20000,30000,40000,50000])
	plt.ylim(-2000,50000)

	ax = plt.axes()
	ax.grid(True)
	ax.xaxis.set_major_formatter(plt.NullFormatter())
	#ax.yaxis.set_major_formatter(plt.NullFormatter())
	legend = plt.legend(loc='upper left',fontsize=18)
	#plt.title(filename[0])
	#plt.ioff()
	plt.show()
	#print(out_plot)
	#plt.savefig(out_plot + "-seq_number.png")	
	f.close()

def main():
	in_filename = sys.argv[1],sys.argv[2], sys.argv[3]
	out_plot = "plots/" + str(datetime.datetime.now())

	#if len(sys.argv) > 2:
	#	out_plot = sys.argv[2] 

	plot_seq(in_filename,out_plot)
	#boxplot_seq(in_filename,out_plot)
	exit(0)

if __name__ == '__main__':
	main()

