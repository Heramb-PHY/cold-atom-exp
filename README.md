# cold-atom-exp
This this the program to control the cold atom experiments using national instruments NI-6535-B card

# Documentation for Software of Computer Control 

## How to use this software ?
   
   .... will update in future

## Working of code 

The code is distributed in several files, which are interlinked to produce signal in the form of text file that we want to send to the C-executable.

- main.py -: generates the time line by reding excel file(csv file).
- channnels.py -: handles individual channel and value of channel.
- cards.py -:
- instruments.py-: creates instrument objects from insturment information (instrument_info.csv)
  
User_timeline (class object) is the information about instrument timing as entered by user. We want this events to happen in this timeline.The code in this User_timeline extracts data from excel(csv) file created by user.
  
csv file format:
|Instrument|sec|mili|micro|Time_rep|
|----------|---|----|-----|--------|
|AOM|0|0|4| |

For Time_rep read {How to generate multiple experiments using Time_rep?}



# cold-atom-exp
