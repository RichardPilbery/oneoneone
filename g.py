# Global parameter values
class G:
    call_inter = 0.5            # Call inter-arrival time in minutes
    start_day = "Sun"
    start_hour = 9
    
    sim_duration = 5760       # 96 hours 5760
    warm_up_duration = 1440    # 24 hours = 1440
    number_of_runs = 2         # Number of runs
    number_of_gp = 2
    number_of_ed = 2
    number_of_111 = 5
    number_of_999 = 3
    
    prob_callback = 0.5
    prob_male = 0.4
    prob_baulk = 0.5
    
    pt_time_in_sim = 4320 # 4320 for 72 hours
    
    all_results_location = 'all_results.csv'
    
    gp_wait_time = 360
    ed_wait_time = 1440
    t1_wait_time = 360
    t9_wait_time = 1440
    baulk_wait_time = 120
    
    gp_visit_time = 10
    ed_visit_time = 240
    t1_visit_time = 10
    t9_visit_time = 90
     