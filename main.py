from instruments import instruments,instru_func
import pandas as pd
import numpy as np
from functions import *
from functools import reduce

with open ("working_address.txt","r") as f:
    address_of_timeline_file = f.read()
#address_of_timeline_file = "time_sequence.xlsx"

clk_time = 2     # Clk time is 2 microseconds = 500kHz

df = pd.read_excel(address_of_timeline_file,sheet_name="time_sequence",usecols=["Instrument","Time","status","Time_rep"],dtype={"Instrument":str,"Time":int,"status":float,"Time_rep":str},na_filter=False) # reading time sequence file
#df.to_excel("1_user_input.xlsx",engine='openpyxl') # to check occasionally

#----------------------------------- to check time repeatition-------------------------------------------------------------#
time_repeat_location = []
for index, value in df["Time_rep"].items():  # checking how many row contains repeation symbol
    if ':' in value or '|' in value:
        time_repeat_location.append((index, value))
if len(time_repeat_location) > 1:
    raise RuntimeError(f"Row: {time_repeat_location[0]} and {time_repeat_location[1]} have : and | symbols repeated " )
if len(time_repeat_location) == 1:
    print(df["Instrument"][time_repeat_location[0][0]],"instrument will be repeated.")
    time_repeat_list = get_multiple_time(time_repeat_location[0][1])
    print(f"This experiment will be done {len(time_repeat_list)} times for {df["Instrument"][time_repeat_location[0][0]]} \n for time value {time_repeat_list}u in microseconds . ")
    df.at[time_repeat_location[0][0],"Time"] = time_repeat_list[0]
    extended_df = df.copy()
    for time_repeat_item in time_repeat_list[1:]:
        df2 = df.copy()
        df2.at[0,"Time"] = 10000 # Adding delay of 10 ms second for each iteration
        df2.at[time_repeat_location[0][0],"Time"] = time_repeat_item
        extended_df = pd.concat([extended_df,df2],ignore_index=True)
    #extended_df.to_excel("2_time_repeated.xlsx",engine='openpyxl') # to check occasionally
    df = extended_df
#------------time_repeatblock complete---------#

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

def make_even(x):
    return x + 1 if x % 2 != 0 else x
df['Absolute time'] = df['Absolute time'].apply(make_even)  # This will ensure that time will be always multiple of 2 microsec

def check_consecutive(df):
    for i in range(1, len(df)):
        if df.loc[i, 'Absolute time'] == df.loc[i-1, 'Absolute time'] :
            if ( df.loc[i,'Channel Type'] == 'A' or df.loc[i-1,'Channel Type'] == 'A'):
                raise RuntimeError(f"Warning: Instrument  {df.loc[i, 'Instrument']} and {df.loc[i-1, 'Instrument']} is overlapping with each other and one of them is analog " )
            if df.loc[i, 'Instrument'] == df.loc[i-1, 'Instrument']:
                raise RuntimeError(f"Warning: Consecutive same time and instrument {df.loc[i, 'Instrument']} found at index {i-1} and {i}")
            if df.loc[i,'Channel Type'] == 'D':
                if df.loc[i,'Instrument'].channel.digital_card.number !=  df.loc[i-1,'Instrument'].channel.digital_card.number :
                    raise RuntimeError(f"Warning: {df.loc[i, 'Instrument']} is connected to digital card {df.loc[i,'Instrument'].channel.digital_card.number} while  {df.loc[i-1, 'Instrument']} is connected to digital card {df.loc[i-1,'Instrument'].channel.digital_card.number} and both are overlapping")

check_consecutive(df)

#df.to_excel("3_time_info.xlsx",engine='openpyxl')  # to check occasionally
# Block to convert user input of analog signal to required number using calibrated curve
for idx, row in df.iterrows():
    instru = row["Instrument"]
    stat = row["status"]
    if instruments[instru].channel.type == "A":
        df.at[idx, "status"] = instru_func[instru](float(stat))
#df.to_excel("4_analog_trans.xlsx",engine='openpyxl')  # to check occasionally
def merge_lists(x):
    if isinstance(x, list):
        return [item for sublist in x for item in sublist]
    else:
        return x
df_merged = df.groupby('Absolute time').agg({'Instrument': list,'Time': list, 'status': merge_lists, 'Channel Object': merge_lists, 'Cumulitive time': list,'Instrument delay': list }).reset_index()

#df_merged.to_excel("5_merging.xlsx",engine='openpyxl')  # to check occasionally

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
df_merged["signal number"] = (df_merged['Absolute time'] / 2).astype(int)
df_merged["data"] = df_merged.apply(lambda row:generate_data(row['Channel Object'],row['status'],row['signal number']), axis=1)# gen_data(df["status"]))
#df_merged.to_excel("6_with_data.xlsx",engine='openpyxl')
# Define a lambda function to convert binary lists to integers
to_integer = lambda binary_list: reduce(lambda x, y: (x << 1) | y, binary_list)
df_merged['integer_value'] = df_merged['data'].apply(to_integer)
#df_merged.to_excel("7_with_32int.xlsx",engine='openpyxl')
df_merged.to_csv('text.txt',columns=['integer_value','signal number'] ,header=False, index=False, sep='\t')
print("text file ready")
