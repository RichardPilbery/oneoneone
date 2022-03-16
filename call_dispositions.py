import pandas as pd
import numpy as np

class CallDispositions:
    
    dx_codes = pd.DataFrame(
        {
            "disposition"       : ["Dx05", "Dx06", "Dx07", "Dx08", "Dx11", "Dx12", "Dx13", "Dx14", "Dx15", "Dx61", "Dx75", "Dx116", "Dx117"],
            "time_frame_hours"  : [2, 6, 12, 24, 1, 2, 6, 12, 24, 0.3, 72, 6, 1],
            "contact_speak"     : ["contact", "contact", "contact", "contact", "speak", "speak", "speak", "speak", "speak", "speak", "contact", "speak", "speak"],
            "prob"              : [0.05, 0.2, 0.1, 0.05, 0.01, 0.20, 0.30, 0.03, 0.01, 0.02, 0.01, 0.01, 0.01],
        }
    )
    dx_codes.set_index("disposition", inplace=True)
    
    # print(sum([0.05, 0.2, 0.1, 0.05, 0.01, 0.20, 0.30, 0.04, 0.01, 0.02, 0.01, 0.01]))

    
# Dx116	Speak to the Primary Care Service within 6 hours for Expected Death - Perhaps remove these?
# Dx117	Speak to a Primary Care Service within 1 hour for Palliative Care - Perhaps remove these?
    hours_of_day = list(range(0,24))
    # dow = ["Mon", "Tue", "Wed","Thu","Fri","Sat","Sun"]
    weekday = ["weekend", "weekday"]
    inter_arrival_csv = pd.read_csv("inter_arrival_times.csv")

    call_arrivals = pd.DataFrame(
        {
            "hour"              : hours_of_day * 2,
            "weekday"           : np.repeat(weekday, 24),
            "interarrival_time" : inter_arrival_csv['mean_inter_arrival_time'].tolist()
        }
    )
    