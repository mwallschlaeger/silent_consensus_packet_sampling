import sys,collections,time,datetime, math
import numpy as np 

from scapy.all import *

class SeqIntermediateHopCollector():
	
	def __init__(self,filename,reporter,interval=1,history_len=5,history_steps_in_interval=1):
		self.reporter = reporter
		self.filename = filename
		self.time_acc = 1
		self.history_step = 1
		self.last_floor = -1

		self.interval = interval
		self.history_steps_in_interval = history_steps_in_interval
		self.history_len = history_len

		self.ignore_init = history_len * 2
		self.tcp_connections = {}

#
# Forecasting Section
#
	def init_history(self,history_len):
		history = collections.deque(maxlen=history_len)
		for i in range(0,history_len):
			history.append(1500)
		return history 
		
	def init_forecast(self, history_len):
		x = np.array(np.arange(0,history_len))
		A = np.vstack([x, np.ones(len(x))]).T
		return A

	def forecast_seq(self,history,A):
		y = np.array(history)
		m, c = np.linalg.lstsq(A, y,rcond=None)[0]
		next_seq = m * len(history) + 1 + c
		return next_seq,m

#
# Packet handling Section
#
	def start_sniff(self):
		sniff(offline=self.filename, prn=self.pkt_callback)
		self.reporter.final_report(self.tcp_connections,
									self.interval,
									self.history_len,
									self.history_steps_in_interval)

	def create_connection(self,key,p):
		''' initialize new connection '''
		seq = p[TCP].seq 
		self.tcp_connections[key] = {}
		self.tcp_connections[key]["history"] = self.init_history(self.history_len)
		self.tcp_connections[key]["A"] = self.init_forecast(self.history_len)
		self.tcp_connections[key]["initial_seq"] = seq
		self.tcp_connections[key]["seq_resets"] = 0 # number of times 32bit are filled, so its started by 0 again
		self.tcp_connections[key]["first"] = seq
		self.tcp_connections[key]["last"] = seq 
		self.tcp_connections[key]["EI"] = []
		self.tcp_connections[key]["PI"] = []
		self.tcp_connections[key]["t_minus1"] = -1  # last last seq
		self.tcp_connections[key]["prediction"] = -1.0

	def update_connection(self,key,p):
		''' update ongoing connection '''
		self.tcp_connections[key]["last"] = p[TCP].seq 

	def reset_connection(self,key):
		self.tcp_connections[key]["t_minus1"] = self.tcp_connections[key]["first"]
		if (self.tcp_connections[key]["last"] < self.tcp_connections[key]["first"]):
			self.tcp_connections[key]["seq_resets"] += 1
		self.tcp_connections[key]["first"] = self.tcp_connections[key]["last"]
	
	def predict(self,key):
		self.tcp_connections[key]["prediction"],self.tcp_connections[key]["slope"] = self.forecast_seq(self.tcp_connections[key]["history"],self.tcp_connections[key]["A"])

	def distributed_consensus(self,key):
		forecasted_seq = self.tcp_connections[key]["prediction"]
		last_seq =  self.tcp_connections[key]["last"]
		slope = self.tcp_connections[key]["slope"]
		k = 10
		z_ = math.floor(forecasted_seq / k ) * k
		z__ = z_ + k
		self.tcp_connections[key]["consens_seq"] = z_
		self.tcp_connections[key]["consens_seq_"] = z__
		# TODO ADD TIMESTAMP OF ARRIVAL

	def pkt_callback(self,pkt):
		'''Executed on each packet read from the pcap file'''
		if not pkt.haslayer(IP):
			return
		if not pkt.haslayer(TCP):
			return 
		
		if self.last_floor == -1:
			self.last_floor = pkt.time

		# 4-Tuple
		key = pkt[IP].dst + \
					":" + \
					str(pkt[TCP].dport) + \
					"_" + \
					pkt[IP].src + \
					":" + \
					str( pkt[TCP].sport ) \

		if key in self.tcp_connections:
			self.update_connection(key,pkt)
		else:	
			self.create_connection(key,pkt)
		
		# HISTORY UPDATE
		if (pkt.time * self.time_acc % 1) > (1 / self.history_steps_in_interval * self.history_step):
			for key,conn in self.tcp_connections.items():
				self.tcp_connections[key]["history"].append(self.tcp_connections[key]["last"])
			self.history_step += 1

		# INTERVAL EXECUTION
		if math.floor(pkt.time * self.time_acc) == (math.floor(self.last_floor)+self.interval):
			self.last_floor = pkt.time
			self.do_in_interval( pkt )

			self.history_step = 1
			for key,conn in self.tcp_connections.items():
				self.tcp_connections[key]["history"].append(self.tcp_connections[key]["last"])

		
	def do_in_interval(self,pkt):
		''' executed each interval e.g. 1 sec '''
		for key,conn in self.tcp_connections.items():
			self.reset_connection(key)
		if self.ignore_init > 0:
			self.ignore_init -= 1
			return
		
		for key,conn in self.tcp_connections.items():
			self.predict(key)
			self.distributed_consensus(key)
		self.reporter.report(self.tcp_connections,pkt.time)


class Reporter():

	def __init__(self,outfile):
		self.log_file = open(outfile+".log","w")
		self.final_report_file = open(outfile+"_final.log","w")

	def report(self,tcp_connections,time_now):
		for key,conn in tcp_connections.items():
			ei = abs(tcp_connections[key]["last"] - tcp_connections[key]["prediction"])
			tcp_connections[key]["EI"].append(ei)
			pi = abs(100 * ei /  tcp_connections[key]["prediction"])
			if not (pi == float('Inf')):
				tcp_connections[key]["PI"].append(pi)
			else:
				tcp_connections[key]["PI"].append(-1)

			output = (str(time_now) + \
					 ", connection: " + \
					 str(key) + \
					 ", current_seq: " + \
					 str(tcp_connections[key]["last"]) + \
					 ", predicted_seq: " + \
					 str(tcp_connections[key]["prediction"]) + \
					 ", ei: " + \
	 				 str(ei) + \
					 ", pi: " + \
					 str(pi) + \
					 ", consens_seq: " + \
					 str(tcp_connections[key]["consens_seq"]) + \
					 ", consens_seq_: " + \
					 str(tcp_connections[key]["consens_seq_"]) + \
					 ", seq_grown_last_SEC: " + \
					 str(self.grown_in_interval(conn)))
			self.log_file.write(output+"\n")
			self.log_file.flush()
			#print(output)

	def grown_in_interval(self,conn):
		return conn["last"] - conn["t_minus1"]

	def final_report(self,tcp_connections,interval,history_len,history_steps_in_interval):
		for key,conn in tcp_connections.items():
			pi_sum = sum(tcp_connections[key]["PI"])
			ei_sum = sum(tcp_connections[key]["EI"])
			
			mape = pi_sum / float(len(tcp_connections[key]["PI"]))
			mae = ei_sum / float(len(tcp_connections[key]["EI"]))
			rmse = math.sqrt(mae**2)
			
			seqs_grown_overall = (tcp_connections[key]["last"] \
								- tcp_connections[key]["initial_seq"] \
								+ tcp_connections[key]["seq_resets"] * 2**32)


			results="connection: " + \
					str(key) + \
					",max_pi: " + \
					str(max((tcp_connections[key]["PI"]))) + \
					",min_pi: " + \
					str(min((tcp_connections[key]["PI"]))) + \
					",MAE: " + \
					str(mae) + \
					",RMSE: " + \
					str(rmse) + \
			 		",mape: " + \
					str(mape) + \
					",overall seqs: " + \
					str(seqs_grown_overall)	
			configuration="connection " + \
							str(key) + \
							"interval " + \
							str(interval) + \
							"history_length " + \
							str(history_len) + \
							"history_steps_in_interval " + \
							str(history_steps_in_interval) 
						
			self.final_report_file.write(results+"\n")
			self.final_report_file.flush()
			print(results)

	def close(self):
		self.log_file.close()
		self.final_report_file.close()


def main():
	in_filename = sys.argv[1]
	out_filename = "logs/" + str(datetime.datetime.now())
	interval = 1
	history_len = 5
	history_steps_in_interval = 1

	if len(sys.argv) == 3:
		out_filename =  sys.argv[2] 
	
	if len(sys.argv) == 6:
		out_filename =  sys.argv[2] 
		interval = sys.argv[3]
		history_len = sys.argv[4]
		history_steps_in_interval = sys.argv[5]

	
	reporter = Reporter(out_filename)
	print("Executing experiment with infile: " + in_filename + " ,outfile: " + out_filename + " ,interval " + str(interval) + " ,history_len: " + str(history_len) + " ,history_steps_in_interval: " + str(history_steps_in_interval))
	try:
		seq = SeqIntermediateHopCollector(in_filename,reporter,int(interval),int(history_len),int(history_steps_in_interval))
	except:
		print("last 3 parameters has to be integer")
		exit(1)
	seq.start_sniff()

	reporter.close()

	sys.exit(0)

if __name__ == '__main__':
	main()
