from seq_collector_file_based import Reporter,SeqIntermediateHopCollector
import sys

def main():

	CONFIGURATIONS = [(1,2,2),
					(1,2,1),
					(1,3,1),
#					(1,3,2)
#					(1,5,1),
#					(1,5,2),
#					(2,2,2),
#					(2,2,1),
#					(2,3,1),
#					(2,3,2),
#					(2,5,1),
#					(2,5,2),
#					(5,2,2),
#					(5,2,1),
#					(5,3,1),
#					(5,3,2),
#					(5,5,1),
#					(5,5,2),
#					(10,2,2),
#					(10,2,1),
#					(10,3,1),
#					(10,3,2),
#					(10,5,1),
#					(10,5,2)]
	]
	#HOSTS = ["server","client","router"]
	HOSTS = ["client","router"]

	#HOSTS = ["server"]
#	RESOLUTIONS = ["4k","hd","480p"]
	RESOLUTIONS = ["480p"]

	for host in HOSTS:
		for reso in RESOLUTIONS:
			for conf in CONFIGURATIONS:
				in_filename = "pcap_files/" + reso + "_1_" + host + ".pcap"
				out_filename = "logs_new/paper-eval-forecasting/" + host + "_" + reso + "_" + str(conf[0]) + "_" + str(conf[1]) + "_" + str(conf[2])
				interval,history_len,history_steps_in_interval = conf
				reporter = Reporter(out_filename)
				print(str(conf[0]) + " " + str(conf[1]) + " " + str(conf[2]) + " " + host + " " + reso )
				seq = SeqIntermediateHopCollector(in_filename,reporter,interval,history_len,history_steps_in_interval)
				seq.start_sniff()
				reporter.close()

	sys.exit(0)

if __name__ == '__main__':
	main()
