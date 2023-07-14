from cards import Analog_Card,Digital_Card
from cards import digitalcard,analogcard

class Channel:
    pass

class Digital_Channel(Channel):

    def __init__(self,digital_card,number,instrument="None"):
        self.type = "D"
        self.digital_card = digital_card
        self.number = number
        self.instrument = instrument
        self.address = digital_card.address
        if self.instrument == "None":
            self.connection = "not connected"
        else:
            self.connection = "connected"
            self.instrument = instrument

    def gen_data(self,value):

        data = self.digital_card.status
        if value == "ON":
            data[self.number-1] = 1
        if value == "OFF":
            data[self.number-1] = 0
        self.digital_card.update(data)
        #print("updated Data")
        return data


class Analog_Channel(Channel):

    def __init__(self,analog_card,number,instrument="None"):
        self.type = "A"
        self.analog_card = analog_card
        self.number = number
        self.instrument = instrument
        if self.instrument == "None":
            self.connection = "not connected"
        else:
            self.connection = "connected"
            self.instrument = instrument
        if number == 1:
            self.address = [0,0,0] + analog_card.address
        if number == 2:
            self.address = [0,0,1] + analog_card.address
        if number == 3:
            self.address = [0,1,0] + analog_card.address
        if number == 4:
            self.address = [0,1,1] + analog_card.address
        if number == 5:
            self.address = [1,0,0] + analog_card.address
        if number == 6:
            self.address = [1,0,1] + analog_card.address
        if number == 7:
            self.address = [1,1,0] + analog_card.address
        if number == 8:
            self.address = [1,1,1] + analog_card.address

    def gen_data(self,value):

        #Calibation function here

        data = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        integer = int( (value+10)/(20/(2**(16)-1)))
        '''
        dividend = integer
        i = 15
        while (not(dividend == 1 or dividend == 0):
            remainder = dividend%2
            dividend = dividend/2
            data[i] = remainder
            i = i-1
        '''
        binary = bin(integer)
        binary_list = list(binary)
        binary_list.reverse()
        for i in range(len(binary)-2):
            data[15-i]=int(binary_list[i])

        return data

#creating digital and analog channels
digital_channels  = {j:{i:Digital_Channel(digitalcard[j],i) for i in range(1,17)} for j in range(1,11)}
analog_channels = {j:{i:Analog_Channel(analogcard[j],i) for i in range(1,9)} for j in range(1,11)}

channel = {"A":analog_channels,"D":digital_channels}
