import simpy
import csv
import random
import pandas as pd
from caller import Caller
from g import G
# Health Care System model
# as it relates to 111 patients
class HMS_Model:
    def __init__(self, run_number):
        self.env = simpy.Environment()
        self.patient_counter = 0
        
        self.GP = simpy.PriorityResource(self.env, capacity=G.number_of_gp)
        
        self.mean_q_time_speak_to_gp = 0
        self.mean_q_time_contact_gp = 0
        
        self.results_df = pd.DataFrame()
        self.results_df["P_ID"] = []
        self.results_df["Q_Time_Speak_to_GP"] = []
        self.results_df.set_index("P_ID", inplace=True)
        
        self.run_number = run_number
        
        # Think about baulk rate
        # Bypass to ED/999/111 ?
        
    def generate_111_calls(self):
        # Run generator until simulation ends
        while True:
            self.patient_counter += 1
            
            # Create a new caller
            pt = Caller(self.patient_counter, G.prob_male, G.prob_callback)
            
            self.env.process(self.patient_journey(pt))
            
            sampled_interarrival = random.expovariate(1.0 / G.call_inter)
            
            # Freeze function until interarrival time has elapsed
            yield self.env.timeout(sampled_interarrival)
            
    def patient_journey(self, patient):
        # Record the time a patient waits to speak/contact GP
        start_q_GP = self.env.now
        
        with self.GP.request(priority=patient.priority) as req:
            yield req
            
            end_q_GP = self.env.now
            patient.q_time_gp_contact = end_q_GP - start_q_GP
            #print(f'Patient waited {patient.q_time_gp_contact} to be seen')
            
            yield self.env.timeout(10)
            
        if self.env.now > G.warm_up_duration:
            self.store_patient_results(patient)
   
    def calculate_mean_q_times(self):
        self.mean_q_time_contact_gp = (self.results_df["Q_Time_Speak_to_GP"].mean())
            
    def store_patient_results(self, patient):        
        # NaNs are automatically ignored by Pandas when calculating the mean
        # etc.  We can create a nan by casting the string 'nan' as a float :
        # float("nan")
        # if patient.acu_patient == True:
        #     patient.q_time_ed_assess = float("nan")
        # else:
        #     patient.q_time_acu_assess = float("nan")
            
        df_to_add = pd.DataFrame(
            {
                "P_ID":[patient.id],
                "Q_Time_Speak_to_GP":[patient.q_time_gp_contact]
            }
        )
        
        df_to_add.set_index("P_ID", inplace=True)
        self.results_df = self.results_df.append(df_to_add)   
        
    def write_run_results(self):
        print('Writing run results')
        print(self.results_df.head())
        with open("trial_111_results.csv", "a", newline='') as f:
            writer = csv.writer(f, delimiter=",")
            results_to_write = [self.run_number,
                                self.mean_q_time_contact_gp]
            writer.writerow(results_to_write)        
            
    def run(self):
        # Start entity generators
        self.env.process(self.generate_111_calls())
        
        # Run simulation
        self.env.run(until=(G.sim_duration + G.warm_up_duration))
        
        # Calculate run results
        self.calculate_mean_q_times()
        
        
        # Write run results to file
        self.write_run_results()
   