# Global parameter values
class G:
    call_inter = 5              # Call inter-arrival time in minutes
    sim_duration = 1000          # 96 hours 5760
    warm_up_duration = 0      # 24 hours = 1440
    number_of_runs = 1          # Number of runs
    number_of_gp = 5
    number_of_ed = 5
    number_of_111 = 20
    number_of_999 = 10
    
    prob_callback = 0.5
    prob_male = 0.4
    prob_baulk = 0.5
    
    pt_time_in_sim = 1440 # 4320 for 72 hours
    
    all_results_location = 'all_results.csv'
    
    gp_wait_time = 360
    ed_wait_time = 1440
    t1_wait_time = 360
    t9_wait_time = 1440
    
    gp_visit_time = 10
    ed_visit_time = 240
    t1_visit_time = 10
    t9_visit_time = 90
     