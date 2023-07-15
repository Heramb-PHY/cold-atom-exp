from channels import *
import pandas as pd
import numpy as np
from numpy.polynomial import Polynomial


df = pd.read_excel("instrument_info.xlsx") 

class Instrument:

    def __init__(self,name:str,channel,delay:float=0):
        # delay is in microseconds
        #validations
        all = []
        assert delay >=0, f"Delay of instrument {delay} is negative quantity"
        assert delay%2==0,f"Delay of instrument {delay} is should be even muliple of clk period(2 micro sec)"
        self.name = name
        self.delay = delay
        self.channel = channel
        #Instrument.all.append(self)
instruments = {}

for i in df.index:
    chan=channel[df['card'][i]][df['card_number'][i]][df['channel_number'][i]] # calling particular channel
    device = Instrument(name=df['name'][i],channel=chan,delay = df['delay'][i]) # assigning channel to instrument
    chan.instrument = device # assigning instrument to channel
    instruments[device.name] = device
df2 = pd.read_excel("instrument_info.xlsx",sheet_name="instrument_function",usecols=[0,1,2],na_filter=False)
# converting string into -> list -> np.array
df2["coeffs"] = df2['coeffs'].apply(eval).apply(np.array) 
# converting parametrs into functions
df2["function"] = df2["coeffs"].apply(Polynomial)

for instru_name, fun in zip(df2["name"],df2["function"]):
    instruments[instru_name].function = fun 
#print(instruments["AOM"].channel.address)
#print(channel["D"][1][1].instrument.name)
'''
   @classmethod
   def connection(self):
        '''
'''
        with open("instrument_info.csv","r") as f:
            reader = csv.DictReader(f)
            items = list(reader)
        '''
        
'''
        for instru in items:
            if instru.get("card") == "D":
                device = Instrument(name=instru.get('name'),delay = int(instru.get('delay')))
                card_number = int(instru.get("card_number"))
                channel_number = int(instru.get("channel_number"))
                di[channel_number-1].instrument = device
            if instru.get("card") == "A":
                device = Instrument(name=instru.get('name'),delay = int(instru.get('delay')))
                card_number = int(instru.get("card_number"))
                channel_number = int(instru.get("channel_number"))
                analog_card_1_channels[channel_number-1].instrument = device
        
        



AOM = Instrument("AOM",4)
Camera = Instrument("Camera",12)
Blue_MOT = Instrument("Blue MOT",16)
H_coil = Instrument("Helmholtz Coil",32)

print(analog_card_1_channels[0].instrument.name)
print(instruments)

'''
