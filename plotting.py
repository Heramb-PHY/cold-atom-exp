import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
import pandas as pd

df = pd.read_excel("time_info.xlsx",usecols=[1,2,3,4],na_filter=False) 
t_final = 100
total_device = 2
x = [0, 16, 26, 34, 44, 56,70,77,80,90] # absolute time for change
y = [1, 1, 0, 1, 1, 1,0,1,0,0]     # status value

#input of function : device name,device type, (x,y)


# Create a figure and axis
fig, axs = plt.subplots(total_device+1,sharex=True,squeeze=True)

# Plot broken barh : https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.broken_barh.html
# for digital type of device
#x = [0, 15, 25, 35, 45, 55] # absolute time for change
#y = [0, 1, 0, 1, 0, 1]     # status value

#-- for device in range dictionary of devices
barx = [(x[i], x[i+1] - x[i]) for i in range(len(x)-1) if (y[i]==1 and y[i+1]==0) or (y[i]==1 and y[i+1]==1)]
device = 'Camera'
axs[0].broken_barh(barx, (0, 1), facecolors=['green'])
axs[0].set_ylabel(device)
axs[0].set_xticks(np.arange(0,t_final,2))
axs[0].grid(True)
axs[0].tick_params(axis='x',labelcolor='blue')

# Plot step function (for analog type devices)
#x = [0, 16, 26, 34, 44, 56] # absolute time for change
#y = [0, 1, 0, 1, 0, 1]     # status value
axs[1].step(x, y, where='post', color='blue')
axs[1].set_ylabel('780 detuning')
axs[1].set_xticks(np.arange(0,t_final,2))
axs[1].grid(True)
axs[1].tick_params(axis='x',labelcolor='blue')

# Phase of the experiment
#-- Phase input--> phase 'name',ini_time,phase_duration
phase_name='Phase'
phase_init_time = 0
phase_duration = 10
bbox1 = patches.FancyBboxPatch((phase_init_time, 0), phase_duration, 2, boxstyle="round,pad=0.1", edgecolor='red', facecolor='yellow')
axs[2].add_patch(bbox1)
axs[2].set_ylabel(phase_name)
axs[2].text(5, 0.5, "loading", rotation=0, color="blue", ha="center", va="center")
axs[2].grid(True)


plt.xlabel('Absolute time')
plt.xticks(rotation='vertical')
plt.get_current_fig_manager().full_screen_toggle() # toggle fullscreen mode
plt.show()
