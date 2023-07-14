# cold-atom-exp
This this the program to control the cold atom experiments using national instruments NI-6535-B card

# Documentation for Software of Computer Control 

## How to use this software ?
   
   Write timesequence in time_sequence.xlsx file.
   Instrument name, time and status.
   xlsx file format:
|Instrument|sec|mili|micro|status|Time_rep|
|----------|---|----|-----|-----|--------|
|AOM|0|0|4| | |
   Run the python code

## Working of code 

The code is distributed in several files, which are interlinked to produce signal in the form of text file that we want to send to the C-executable.

- cards.py -: exctracts infrmation about card address from card_info.xlsx
- channnels.py -: handles individual channel and value of channel.
- instruments.py-: creates instrument objects from insturment information (instrument_info.csv)
- main.py -: generates the time line by reding excel file(xlsx file).

1. Firstly programs reads the excel file
2. Then it creates "Channel Object","Channel Type","Cumulitive time", "Instrument delay" columns and calculate the "Absolute time".
3. Arranging in ascending order with repsect to absolute time.
4. We group by "Absolute time".
  


For Time_rep read {How to generate multiple experiments using Time_rep?}



# cold-atom-exp
