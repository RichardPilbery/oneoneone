# Global parameter values
class G:
    call_inter = 0.5            # Call inter-arrival time in minutes
    start_day = "Mon"
    start_hour = 9
    
    sim_duration = 57600         # 96 hours 5760
    warm_up_duration = 1440     # 24 hours = 1440
    number_of_runs = 50         # Number of runs
    number_of_gp = 5
    number_of_ed = 5
    number_of_111 = 10
    number_of_999 = 6
    
    prob_callback = 0.5
    prob_male = 0.4
    prob_baulk = 0.5
    
    pt_time_in_sim = 4320 # 4320 for 72 hours
    
    all_results_location = 'all_results.csv'
    
    gp_wait_time = 360
    ed_wait_time = 1440
    t1_wait_time = 360
    t9_wait_time = 1440
    
    gp_visit_time = 10
    ed_visit_time = 240
    t1_visit_time = 10
    t9_visit_time = 90
     