# 111 Primary call disposition
# Basic mode
# NOTE TO SELF: Use base conda env 3.9.1

# Load packages

import csv
import os
import time
import multiprocessing as mp
import sys
import getopt
import logging

from numpy import number

try:
     __file__
except NameError: 
    __file__ = sys.argv[0]

os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from g import G
from hsm_model import HSM_Model

logging.basicConfig(format='%(asctime)s %(message)s', filename='model.log', encoding='utf-8', level=logging.DEBUG)

number_of_runs = G.number_of_runs
warm_up_time = G.warm_up_duration
pt_time_in_sim = G.sim_duration

# Create a file to store trial results
# with open("trial_111_results.csv", "w", newline='') as f:
#     writer = csv.writer(f, delimiter=",")
#     column_headers = ["Run",
#                       "Mean_Q_Time_Speak_to_GP"]
#     writer.writerow(column_headers)

# For the number of runs specified in the g class, create an instance of the
# ED_Model class, and call its run method

def runSim(run, total_runs):
    start = time.process_time()
    print (f"Run {run+1} of {total_runs}")
    logging.debug(f"Run {run+1} of {total_runs}")
    my_111_model = HSM_Model(run)
    my_111_model.run()
    print(f'Run {run+1} took {time.process_time() - start} seconds to run')
    logging.debug(f'Run {run+1} took {time.process_time() - start} seconds to run')

def prepStartingVars(argv):
    logging.debug('Prepping starting vars')
    # Update global variables, not create local version with same name
    global number_of_runs
    global warm_up_time
    global pt_time_in_sim
    # Stolen from: https://opensourceoptions.com/blog/how-to-pass-arguments-to-a-python-script-from-the-command-line/
    
    arg_help = "{0} -n <num_runs> -w <warm_up_time> -p <pt_time_in_sim>".format(argv[0])
    try:
        opts, args = getopt.getopt(argv[1:], "h:n:w:p:", ["help", "num_runs=", 
        "warm_up_time=", "pt_time_in_sim="])
    except:
        print(arg_help)
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)  # print the help message
            sys.exit(2)
        elif opt in ("-n", "--num_runs"):
            print(f'Number of runs: {arg}')
            number_of_runs = int(arg)
        elif opt in ("-w", "--warm_up_time"):
            warm_up_time = int(arg)
        elif opt in ("-p", "--pt_time_in_sim"):
            pt_time_in_sim = int(arg)


nprocess = 10

# if __name__ == '__main__':   
#     logging.debug('Model called')
#     prepStartingVars(sys.argv)
#     if os.path.isfile(G.all_results_location):
#         print('Deleting file')
#         os.remove(G.all_results_location)
#     pool = mp.Pool(processes=nprocess)
#     pool.starmap(runSim, zip(list(range(0, number_of_runs)), [number_of_runs] * number_of_runs))
#     logging.debug('Reached end of script')
#     logging.shutdown()
    
def parallelProcess(nprocess):
    logging.debug('Model called')
    # prepStartingVars(sys.argv)
    if os.path.isfile(G.all_results_location):
        print('Deleting file')
        os.remove(G.all_results_location)
    pool = mp.Pool(processes=nprocess)
    pool.starmap(runSim, zip(list(range(0, number_of_runs)), [number_of_runs] * number_of_runs))
    logging.debug('Reached end of script')
    logging.shutdown()
