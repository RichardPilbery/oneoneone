# 111 Primary call disposition
# Basic mode
# NOTE TO SELF: Use base conda env 3.9.1

# Load packages

import csv
from hsm_model import HSM_Model
from g import G


# Create a file to store trial results
# with open("trial_111_results.csv", "w", newline='') as f:
#     writer = csv.writer(f, delimiter=",")
#     column_headers = ["Run",
#                       "Mean_Q_Time_Speak_to_GP"]
#     writer.writerow(column_headers)

# For the number of runs specified in the g class, create an instance of the
# ED_Model class, and call its run method
for run in range(G.number_of_runs):
    print (f"Run {run+1} of {G.number_of_runs}")
    my_111_model = HSM_Model(run)
    my_111_model.run()