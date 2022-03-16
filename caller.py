from math import floor
import random
from g import G
from call_dispositions import CallDispositions
# Class representing patients who have made a 111 call
class Caller:
    def __init__(self, p_id, prob_male, prob_callback):
        self.id = p_id
        self.age = 50
        self.prob_male = prob_male
        self.sex = "male" if random.uniform(0, 1) < self.prob_male else "female" 
        self.acu_patient = False
        self.prob_callback = prob_callback
        self.timer = 0
        self.activity = ''
        self.gp = ""
        # Choose the patient's initial 111 call disposition
        # We can extend this to include symptom groups etc once we have this data
        self.disposition = random.choices(CallDispositions.dx_codes.index, weights=CallDispositions.dx_codes["prob"])[0]
        
        self.priority = self.determine_priority()         # Priority of triage call
        
        # Keep track of cumulatative time and exit after 4320 minutes i.e. 72 hours
        self.time_since_call = 0
        # Keep track of time and day caller made call to 111
        self.hour = G.start_hour
        self.day = G.start_day
        self.weekday = "weekend" if G.start_day in ["Sat", "Sun"] else "weekday"
        
        # Baulk rate? Perhaps based on 111 call abandonment
            
    # Method to determine the patient's acuity and thus priority
    # for a GP contact
    def determine_priority(self):
        self.priority = random.randint(1,5)
    
        
         