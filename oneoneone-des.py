# 111 Primary call disposition
# Basic mode
# NOTE TO SELF: Use base conda env 3.9.1

# Load packages

import csv
import os
import time
from hsm_model import HSM_Model
import multiprocessing as mp
from g import G

if os.path.isfile(G.all_results_location):
    print('Deleting file')
    os.remove(G.all_results_location)
# Create a file to store trial results
# with open("trial_111_results.csv", "w", newline='') as f:
#     writer = csv.writer(f, delimiter=",")
#     column_headers = ["Run",
#                       "Mean_Q_Time_Speak_to_GP"]
#     writer.writerow(column_headers)

# For the number of runs specified in the g class, create an instance of the
# ED_Model class, and call its run method

def runSim(run):
    start = time.process_time()
    print (f"Run {run+1} of {G.number_of_runs}")
    my_111_model = HSM_Model(run)
    my_111_model.run()
    print(f'Run {run+1} took {time.process_time() - start} seconds to run')

nprocess = 10

if __name__ == '__main__':    
    pool = mp.Pool(processes=nprocess)
    pool.map(runSim, list(range(0, G.number_of_runs)))
    
