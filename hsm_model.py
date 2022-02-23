import os
from numpy import NaN
import simpy
import csv
import random
import pandas as pd
from caller import Caller
from g import G
# Health Care System model
# as it relates to 111 patients
class HSM_Model:
    def __init__(self, run_number):
        self.env = simpy.Environment()
        self.patient_counter = 0
        
        self.GP = simpy.PriorityResource(self.env, capacity=G.number_of_gp)
        self.ED = simpy.PriorityResource(self.env, capacity=8)
        self.Treble1 = simpy.PriorityResource(self.env, capacity=50)
        self.Treble9 = simpy.PriorityResource(self.env, capacity=10)
        
        self.mean_q_time_speak_to_gp = 0
        self.mean_q_time_contact_gp = 0
        
        # Create data frame to capture all sim acitivity
        self.results_df = pd.DataFrame()
        self.results_df["P_ID"]           = []
        self.results_df["run_number"]     = []
        self.results_df["journey_steps"]  = []
        self.results_df["location"]       = []
        self.results_df["wait_time_gp"]   = []
        self.results_df["wait_time_ed"]   = []
        self.results_df["wait_time_111"]  = []
        self.results_df["wait_time_999"]  = []
        self.results_df["visit_time_gp"]  = []
        self.results_df["visit_time_ed"]  = []
        self.results_df["visit_time_111"] = []
        self.results_df["visit_time_999"] = []
        self.results_df["v_number_ed"]    = []
        self.results_df["v_number_gp"]    = []
        self.results_df["v_number_111"]   = []
        self.results_df["v_number_999"]   = []
        self.results_df.set_index("P_ID", inplace=True)
        
        self.run_number = run_number
        
        # Think about baulk rate
        # Bypass to ED/999/111 ?
        
    def generate_111_calls(self):
        # Run generator until simulation ends
        # Stop creating patients after warmup/sim time to allow existing
        # patients 72 hours to work through sim
        if(self.env.now < G.sim_duration + G.warm_up_duration):
            while True:
                self.patient_counter += 1
                
                # Create a new caller
                pt = Caller(self.patient_counter, G.prob_male, G.prob_callback)
                
                self.env.process(self.patient_journey(pt))
                
                sampled_interarrival = random.expovariate(1.0 / G.call_inter)
                
                # Freeze function until interarrival time has elapsed
                yield self.env.timeout(sampled_interarrival)
                
    def next_destination(self, patient):
        return "baulk" if random.uniform(0, 1) < G.prob_baulk else random.choice(['GP', 'ED', '111', '999'])
            
    def patient_journey(self, patient):
        # Record the time a patient waits to speak/contact GP
        loop = 0
        break_loop = 0
    
        while patient.timer < (G.warm_up_duration + G.pt_time_in_sim):
            
            if(loop == 0):
                # First time will see GP
                next_dest = 'GP'
                loop += 1
            else:
                next_dest = self.next_destination(patient)
                
            patient.location = next_dest
            patient.journey_steps.append(next_dest)
                
            if(next_dest == 'GP'):
                #print(f'Patient {patient.id} is off to GP')
                start_wait_time = self.env.now
                with self.GP.request(priority=patient.priority) as req:
                    yield self.env.process(self.step_visit(patient, req, start_wait_time, 'GP'))
            elif(next_dest == 'ED'):
                #print(f'Patient {patient.id} is off to ED')
                start_wait_time = self.env.now
                with self.ED.request(priority=patient.priority) as req:
                    yield self.env.process(self.step_visit(patient, req, start_wait_time, 'ED'))
            elif(next_dest == '111'):
                #print(f'Patient {patient.id} is off to 111')
                start_wait_time = self.env.now
                with self.Treble1.request(priority=patient.priority) as req:
                    yield self.env.process(self.step_visit(patient, req, start_wait_time, '111'))
            elif(next_dest == '999'):
                #print(f'Patient {patient.id} is off to 999')
                start_wait_time = self.env.now
                with self.Treble9.request(priority=patient.priority) as req:
                    yield self.env.process(self.step_visit(patient, req, start_wait_time, '999'))
            elif(next_dest == 'baulk'):
                break_loop = 1
                break
                    
            self.store_patient_results(patient)
         
        # print(self.results_df)
        if(break_loop == 1):
            print(self.results_df)
        self.write_all_results() 

         
                    
    def visit_time(self, visit_type):
        
        visit_time_lookup = {
            'GP': G.gp_visit_time,
            'ED': G.ed_visit_time,
            '111': G.t1_visit_time,
            '999': G.t9_visit_time,
        }
        
        return visit_time_lookup[visit_type]


    def step_visit(self, patient, yieldvalue, start_time, visit_type):
        visit_duration = self.visit_time(visit_type)
        # Wait time to access service
        yield yieldvalue
        
        end_wait_time = self.env.now
        wait_time = end_wait_time - start_time
        
        # Duration of visit
        yield self.env.timeout(random.expovariate(1.0 / visit_duration))
        
        visit_time = self.env.now - end_wait_time
        
        if(visit_type == 'GP'):
            patient.v_number_gp = 1
            patient.wait_time_gp = wait_time,
            patient.visit_time_gp = visit_time


        elif(visit_type == "ED"):
            patient.v_number_ed = 1
            patient.wait_time_ed = wait_time,
            patient.visit_time_ed = visit_time
        elif(visit_type == "111"):
            patient.v_number_111 = 1
            patient.wait_time_111 = wait_time,
            patient.visit_time_111 = visit_time
        elif(visit_type == "999"):
            patient.v_number_999 = 1
            patient.wait_time_999 = wait_time,
            patient.visit_time_999 = visit_time

        if self.env.now > G.warm_up_duration:
            self.store_patient_results(patient)
            patient.timer += (wait_time + visit_time)
            
   
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
                "P_ID"            : [patient.id],
                "run_number"      : [self.run_number],
                "journey_steps"   : [patient.journey_steps],
                "location"        : [patient.location],
                "wait_time_gp"    : [patient.wait_time_gp],
                "wait_time_ed"    : [patient.wait_time_ed],
                "wait_time_111"   : [patient.wait_time_111],
                "wait_time_999"   : [patient.wait_time_999],
                "visit_time_gp"   : [patient.visit_time_gp],
                "visit_time_ed"   : [patient.visit_time_ed],
                "visit_time_111"  : [patient.visit_time_111],
                "visit_time_999"  : [patient.visit_time_999],
                "v_number_gp"     : [patient.v_number_gp],
                "v_number_ed"     : [patient.v_number_ed],
                "v_number_111"    : [patient.v_number_111],
                "v_number_999"    : [patient.v_number_999],
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
            
    def write_all_results(self):
        #print('Writing all results')
        # https://stackoverflow.com/a/30991707/3650230
        
        if not os.path.isfile(G.all_results_location):
           self.results_df.to_csv(G.all_results_location, header='column_names')
        else: # else it exists so append without writing the header
            self.results_df.to_csv(G.all_results_location, mode='a', header=False) 
    
    def run(self):
        # Start entity generators
        self.env.process(self.generate_111_calls())
        
        # Run simulation
        self.env.run(until=(G.sim_duration + G.warm_up_duration + G.pt_time_in_sim))
        
        # Calculate run results
        #self.calculate_mean_q_times()
        
        # Write run results to file
        # self.write_run_results()
        

        
        
        
   