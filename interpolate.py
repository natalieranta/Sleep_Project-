import numpy as np
import datetime
from dataSort import collect_data
import pandas as pd
today = datetime.datetime.today()

#interpolate data for 1 second
def interpolate_seconds(x,y):
    x_data = np.array(x)
    y_data = np.array(y)

    t_data = []
    for pt in x_data:

        x_data = datetime.timedelta(seconds=pt)
        t = today + x_data
        t_data.append(t)

    index = pd.DatetimeIndex(t_data)
    data = pd.Series(y_data, index=index)
    interp_data = data.resample('1s').mean().interpolate()

    print(interp_data)


#testing on heart rate data 
heart_rate_data = collect_data('heart_rate')
interpolate_seconds(heart_rate_data[0][0], heart_rate_data[0][1])
