import os
from numpy import NaN
import simpy
import csv
import random
import pandas as pd
from caller import Caller
from g import G
from call_dispositions import CallDispositions
from math import floor

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
        self.results_df["activity"]       = []
        self.results_df["timestamp"]      = []
        self.results_df["status"]         = []
        self.results_df["instance_id"]    = []
        self.results_df.set_index("P_ID", inplace=True)
        
        self.run_number = run_number
        
        self.call_interarrival_times_lu = CallDispositions.call_arrivals
        
    # Method to determine the current day and hour
    # based on starting day/hour and elapsed sim time
    def date_time_of_call(self, elapsed_time):
        dow = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        G.start_day # Mon
        G.start_hour # 9
        
        index_dow = dow.index(G.start_day)
        # Calculate this day of the week it is, taking into account the starting day
        # and start hour.    
        elapsed_days = floor((elapsed_time + (G.start_hour * 60)) / 1440) % 7 + index_dow
        if elapsed_days > 6:
            elapsed_days = elapsed_days - 7
            
        index_dow = dow.index(G.start_day)        
        elapsed_days = floor(elapsed_time / 1440) % 7 + index_dow
        if elapsed_days > 6:
            elapsed_days = elapsed_days - 7
            
        elapsed_hours = floor(elapsed_time + (G.start_hour * 60)) % 24
        if elapsed_hours > 24:
            elapsed_hours = elapsed_hours - 24
        
        return [dow[elapsed_days], elapsed_hours]
        
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
                
                # Get current day of week and hour of day
                [dow, hod] = self.date_time_of_call(self.env.now)
                inter_time = float(self.call_interarrival_times_lu.query("hour == @hod & day == @dow")["interarrival_time"])
                sampled_interarrival = random.expovariate(1.0 / inter_time) 
                # Some of the longer mean interarrival times will result in a >60 minute time, which will put the call
                # into the next hour
                if sampled_interarrival > 60:
                    sampled_interarrival = 59
                # print(f'Patient is {pt.id} and  Inter time is {inter_time} and sample interarrival is {sampled_interarrival}')
                
                # Freeze function until interarrival time has elapsed
                yield self.env.timeout(sampled_interarrival)
                
    def next_destination(self, patient):
        return "baulk" if random.uniform(0, 1) < G.prob_baulk else random.choice(['GP', 'ED', '111', '999'])
            
    def patient_journey(self, patient):
        # Record the time a patient waits to speak/contact GP
        loop = 0
        break_loop = 0
        instance_id = 0
        patient_enters_sim = self.env.now
    
        while patient.timer < (G.warm_up_duration + G.pt_time_in_sim):
            
            instance_id += 1
            
            next_dest = self.next_destination(patient)
                            
            results = {
                "patient_id"  : patient.id,
                "activity"    : next_dest,
                "timestamp"   : self.env.now,         
                "status"      : 'scheduled',
                "instance_id" : instance_id,
            }

            
            if self.env.now > G.warm_up_duration:
                self.store_patient_results(results)
            
            if(next_dest == 'GP'):
                #print(f'Patient {patient.id} is off to GP')
                with self.GP.request(priority=patient.priority) as req:
                    yield self.env.process(self.step_visit(patient, req, instance_id, 'GP'))
            elif(next_dest == 'ED'):
                #print(f'Patient {patient.id} is off to ED')
                with self.ED.request(priority=patient.priority) as req:
                    yield self.env.process(self.step_visit(patient, req, instance_id, 'ED'))
            elif(next_dest == '111'):
                #print(f'Patient {patient.id} is off to 111')
                with self.Treble1.request(priority=patient.priority) as req:
                    yield self.env.process(self.step_visit(patient, req, instance_id, '111'))
            elif(next_dest == '999'):
                #print(f'Patient {patient.id} is off to 999')
                with self.Treble9.request(priority=patient.priority) as req:
                    yield self.env.process(self.step_visit(patient, req, instance_id, '999'))
            elif(next_dest == 'baulk'):
                break_loop = 1
                break
            
            patient.timer = self.env.now - patient_enters_sim
                    
    def visit_time(self, visit_type):
        
        visit_time_lookup = {
            'GP': G.gp_visit_time,
            'ED': G.ed_visit_time,
            '111': G.t1_visit_time,
            '999': G.t9_visit_time,
        }
        
        return visit_time_lookup[visit_type]


    def step_visit(self, patient, yieldvalue, instance_id, visit_type):
        visit_duration = self.visit_time(visit_type)
        # Wait time to access service
        yield yieldvalue
        
        results = {
            "patient_id"  : patient.id,
            "activity"    : visit_type,
            "timestamp"   : self.env.now,         
            "status"      : 'start',
            "instance_id" : instance_id,
        }

        if self.env.now > G.warm_up_duration:
            self.store_patient_results(results)
        
        # Duration of visit
        yield self.env.timeout(random.expovariate(1.0 / visit_duration))
        
        results = {
            "patient_id"  : patient.id,
            "activity"    : visit_type,
            "timestamp"   : self.env.now,         
            "status"      : 'completed',
            "instance_id" : instance_id,
        }
        
        if self.env.now > G.warm_up_duration:
            self.store_patient_results(results)
            
   
    def calculate_mean_q_times(self):
        self.mean_q_time_contact_gp = (self.results_df["Q_Time_Speak_to_GP"].mean())
            
    def store_patient_results(self, results):        
        df_to_add = pd.DataFrame(
            {
                "P_ID"            : [results["patient_id"]],
                "run_number"      : [self.run_number],
                "activity"        : [results["activity"]],
                "timestamp"       : [results["timestamp"]],
                "status"          : [results["status"]],
                "instance_id"     : [results["instance_id"]]
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
        self.write_all_results() 
        

        
        
        
   