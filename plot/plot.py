from mvmt.metrics import mvmtMetrics
from datamodel.datamodel import *
import datetime
import matplotlib.pyplot as plt 

m = DataSetFromShapeFile(r'C:\Users\Alexandre\Desktop\PhD\ZOOHACKATHON_2020\DataBase\Multi-species\SHP\etosha_15_elephants',[])

fig, ax = plt.subplots(3,figsize=(10,15))

for sp , c in zip(['LA1','LA2','LA3','LA4','LA5'],['blue','red','purple','green','gray']):
    f = m.filter(IdDataFilter(sp))
    f = f.filter(TimeWindow(datetime.datetime(2008, 11, 1, 0, 0), datetime.datetime(2008, 11, 1, 23, 59)))

    points = [(o.longitude,o.latitude) for o in f.animal_positions]

    mvmt = mvmtMetrics(points)
    t = mvmt.TurningAngles
    d = mvmt.distances
    a = mvmt.AbsoluteAngles

    time = [o.timestamp for o in f.animal_positions]

    ax[0].plot_date(time,[0]+d,'o', color=c, ydate=False, tz='UTC+02:00')

    ax[1].plot_date(time,[0]+t+[0],'o', color=c, ydate=False, tz='UTC+02:00')

    ax[2].plot_date(time,[0]+a,'o', color=c, ydate=False, tz='UTC+02:00')

ax[0].set_ylabel('Displacement (m)')
ax[1].set_ylabel('Turning angle (°)')
ax[2].set_ylabel('Absolute angle (°)')
ax[2].set_xlabel('Time')

