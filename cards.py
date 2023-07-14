import csv
import pandas as pd

def check_str(list):
    for index,num in enumerate(list):
         if isinstance(num,str) == True:
             list[index] = int(num)
    return list

class Card:
    pass
'''
    @classmethod
    def info_from_csv(self):
        with open("card_info.csv","r") as f:
            reader = csv.reader(f)
            line_list = list(reader)
        for line in line_list[1:]:
            if line[0] == "D" :
                number = int(line[1])
                address = line[3:]
                check_str(address)
                digitalcard = Digital_Card(number,address)
            if line[0] =="A":
                number = int(line[1])
                address = line[3:]
                check_str(address)
                analogcard = Analog_Card(1,address)
'''

class Digital_Card(Card):

    def __init__(self,number:int,address,type="D"):

        assert number >= 0 , f"Digital Card Number{number} is negative."
        assert len(address)== 8 , f"Digital Card number {number} address {address} is not 8 bit"
        self.number = number
        self.type = type
        self.address = address
        self.status = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    def update(self,array):
        assert len(array) == 16, f"Digital card status{array} is not 16 bit."
        self.status = array

    def connection_status(self):
        pass # shows which channels have which instrument



class Analog_Card(Card):

    def __init__(self,number:int,address,type="A"):

        assert number >= 0 , f"Analog Card Number{number} is negative."
        assert len(address)== 5 , f"Analog Card number {number} address {address} is not 5 bit"
        self.number = number
        self.type = type
        self.address = address

class DDS_card(Card):
    pass

df = pd.read_excel("card_info.xlsx")

digitalcard = { i:Digital_Card(i, df.iloc[i,8:16].tolist()) for i in range(1,11) }
analogcard = { i:Analog_Card(i, df.iloc[i,1:6].tolist()) for i in range(1,11) }


'''
def info_from_csv():

    with open("card_info.csv","r") as f:
        reader = csv.reader(f)
        line_list = list(reader)
    for line in line_list[1:]:
        if line[0] == "D" :
            number = int(line[1])
            address = line[3:]
            check_str(address)
            digitalcard = Digital_Card(number,address)
            print("functionruns")
        if line[0] =="A":
            number = int(line[1])
            address = line[3:]
            check_str(address)
            analogcard = Analog_Card(1,address)

#digitalcard = Digital_Card(1,[0,0,0,0,0,0,0,1])
#analogcard = Analog_Card(1,[0,0,0,0,1])
#Card.info_from_csv()

info_from_csv()
print(digitalcard.type)
print(digitalcard.number)
print(digitalcard.address)
print(analogcard.type)
print(analogcard.number)
print(analogcard.address)
'''
