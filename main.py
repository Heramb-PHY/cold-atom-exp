from instruments import instruments
import pandas as pd
import numpy as np
from functions import *
from functools import reduce

address_of_timeline_file = "time_sequence.xlsx"
clk_time = 2     # Clk time is 2 microseconds = 500kHz
df = pd.read_excel(address_of_timeline_file,sheet_name="time_sequence",usecols=[0,4,5,6],na_filter=False) # reading time sequence file
df.to_excel("1_user_input.xlsx",engine='openpyxl') # to check occasionally
# adding new columns in dataframe
df["Channel Object"] = df["Instrument"].apply(lambda x: instruments[x].channel)
df["Channel Type"] = df["Instrument"].apply(lambda x: instruments[x].channel.type)
df["Cumulitive time"] = df["Time"].cumsum()
df["Instrument delay"] = df["Channel Object"].apply(lambda x: x.instrument.delay)
df["Absolute time"] = df["Cumulitive time"] - df["Instrument delay"]
# sorting using absolute time
df = df.sort_values(by = ['Absolute time'],ascending=True,ignore_index=True)
#adjusting origin of absolute time to zero
df["Absolute time"] = df["Absolute time"] - df["Absolute time"][0]
df.to_excel("2_time_info.xlsx",engine='openpyxl')  # to check occasionally

def merge_lists(x):
    if isinstance(x, list):
        return [item for sublist in x for item in sublist]
    else:
        return x
df_merged = df.groupby('Absolute time').agg({'Instrument': merge_lists,'Time': merge_lists, 'status': merge_lists, 'Channel Object': merge_lists, 'Cumulitive time': merge_lists,'Instrument delay': merge_lists }).reset_index()

df_merged.to_excel("3_merging.xlsx",engine='openpyxl')  # to check occasionally

def generate_data(x, y,z):
    if isinstance(x, np.ndarray) and isinstance(y, np.ndarray):
        for a,b in zip(x,y): # to accomodate multiple values of digital card
            a.gen_data(b)
        data_list = a.gen_data(b) + a.address + [int(abs(z%2-1)),1,0,0,0,0,0,0]
        data_list.reverse()
        return data_list
    else:
        data_list = x.gen_data(y) + x.address + [int(abs(z%2-1)),1,0,0,0,0,0,0]
        data_list.reverse()
        return data_list
#df["data"] = df.apply(lambda x:x["Channel Object"].gen_data(x["status"]), axis=1)# gen_data(df["status"]))
df_merged["signal number"] = (df['Absolute time'] / 2).astype(int)
df_merged["data"] = df_merged.apply(lambda row:generate_data(row['Channel Object'],row['status'],row['signal number']), axis=1)# gen_data(df["status"]))
df_merged.to_excel("4_with_data.xlsx",engine='openpyxl')
# Define a lambda function to convert binary lists to integers
to_integer = lambda binary_list: reduce(lambda x, y: (x << 1) | y, binary_list)
df_merged['integer_value'] = df_merged['data'].apply(to_integer)
df_merged.to_excel("5_with_32int.xlsx",engine='openpyxl')
df_merged.to_csv('text.txt',columns=['integer_value','signal number'] ,header=False, index=False, sep='\t')
print("text file ready")
