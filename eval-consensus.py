import math, sys

DIR = "logs/paper-eval-forecasting"

def get_data(filepointer,element_id):
	data = {}
	for row in filepointer:
		elements = row.split(',')
		connection = elements[1].split(" ")[2].strip()
		if connection.endswith(":1935"):			
			time_value = math.floor(float(elements[0]))
			consens_seq_a = int(round(float(elements[element_id].split(" ")[2].strip())))
			consens_seq_b = int(round(float(elements[element_id+1].split(" ")[2].strip())))

			data[time_value] = [consens_seq_a,consens_seq_b]
	
	return data


def main():

	CONFIGURATIONS = [(1,2,2),
		(1,2,1),
		(1,3,1),
		(1,3,2),
		(1,5,1),
		(1,5,2),
		(2,2,2),
		(2,2,1),
		(2,3,1),
		(2,3,2),
		(2,5,1),
		(2,5,2),
		(5,2,2),
		(5,2,1),
		(5,3,1),
		(5,3,2),
		(5,5,1),
		(5,5,2),
		(10,2,2),
		(10,2,1),
		(10,3,1),
		(10,3,2),
		(10,5,1),
		(10,5,2)]

	HOSTS = ["server","client","router"]
	RESOLUTIONS = ["4k","hd","480p"]

	for reso in RESOLUTIONS:
		for conf in CONFIGURATIONS:
			 a = DIR + "/" + HOSTS[0] + "_" + reso + "_" + str(conf[0]) + "_" + str(conf[1]) + "_" + str(conf[2]) + ".log"
			 b = DIR + "/" + HOSTS[1] + "_" + reso + "_" + str(conf[0]) + "_" + str(conf[1]) + "_" + str(conf[2]) + ".log"
			 c = DIR + "/" + HOSTS[2] + "_" + reso + "_" + str(conf[0]) + "_" + str(conf[1]) + "_" + str(conf[2]) + ".log"
			 print(reso + "_" + str(conf[0]) + "_" + str(conf[1]) + "_" + str(conf[2]))
			 eval(a,b,c)


def ainb(a, b):
  return not set(a).isdisjoint(b)


def eval(a_filename,b_filename,c_filename):
	
	fa = open(a_filename)
	fb = open(b_filename)
	fc = open(b_filename)

	data_a = get_data(fa,6)
	data_b = get_data(fb,6)		
	data_c = get_data(fc,6)		

	fa.close()
	fb.close()
	fc.close()

	a_keys = dict.fromkeys(data_a)
	same = 0
	two_a = 0
	two_b = 0
	two_c = 0

	overall = 0
	none = 0
	time_error = 0
	abs_diff = 0

	for key in a_keys:
		abs_diff += abs(data_a[key][0] - data_b[key][0])

	for key in a_keys:
		try:
			if ainb(data_a[key],data_b[key]):
				if ainb(data_a[key],data_c[key]):
					same+=1
				else: 
					two_a+=1
			elif ainb(data_a[key],data_c[key]):
				two_b+=1
			elif ainb(data_b[key],data_c[key]):
				#print(data_b[key],data_c[key])
				two_c+=1
			else:
				none+=1
			overall += 1 
		except Exception as e:
			print(str(e)) 
			time_error += 1

	print("all: " + str(same) + " " + "two_of_three " + str(two_c) + " avg_diff: " + str( abs_diff / float(overall) ) + " overall: " + str(overall) + " ratio: " + str(same/float(overall)))

if __name__ == '__main__':
	main()

