#string = "ON"
#string = "-2:2" # [-2,2]
#string = "10.0:-10.0:0.1" # [-2,-1,0,1,2]
#string = "2:23:1" # [2,1,0,-1,-2]
#string = "2|10" # [2,2,2,2,2,2,2,2,2,2]
#string = "OFF:3" # [ON,OFF,ON]
#string = "ON|4" # [ON,ON,ON,ON]
#string = "ON:OFF" # [ON,OFF]

# "start:end:step_size"
# "value|copies of value"
# one_value:second_value

def get_multiple_status(string):

    if "|" in string:

        separated = string.split("|")

        if separated[0] == "ON" or separated[0] == "OFF" :
            status_list = [separated[0]]*int(separated[1])
        else:
            status_list = [float(separated[0])]*int(separated[1])


    if ":" in string:

        if string.count(":") == 1 :
            separated = string.split(":")

            if  separated[0] == "ON" or separated[0] == "OFF" :
                if separated[1] == "ON" or separated[1] == "OFF":
                    status_list = [separated[0],separated[1]]
                else:
                    status_list = [separated[0]]
                    for i in range(0,int(separated[1])-1):
                        if status_list[i] == "ON":
                            status_list.append("OFF")
                        if status_list[i] == "OFF":
                            status_list.append("ON")

            else:

                status_list = [float(ele) for ele in separated]

        if string.count(":") == 2 :
            separated = string.split(":")

            initial_value = float(separated[0])
            final_value = float(separated[1])
            step_value = float(separated[2])

            if final_value < initial_value :
                step_value = -step_value

            status_list = [initial_value + i*step_value for i in range(int(abs(final_value-initial_value)/abs(step_value))+1)]

    return status_list

def get_multiple_time(string):
    time_dict = {"s":1000000,"m":1000,"u":1}

    if string.count(":") == 2 :
        separated = string.split(":")

        initial_value = float(separated[0][0:-1])*int(time_dict[separated[0][-1]])
        final_value = float(separated[1][0:-1])*int(time_dict[separated[1][-1]])
        step_value = float(separated[2][0:-1])*int(time_dict[separated[2][-1]])

        if final_value < initial_value :
            step_value = -step_value

        status_list = [initial_value + i*step_value for i in range(int(abs(final_value-initial_value)/abs(step_value))+1)]

    if string.count(":") == 1:
        separated = string.split(":")

        first_value = float(separated[0][0:-1])*int(time_dict[separated[0][-1]])
        second_value = float(separated[1][0:-1])*int(time_dict[separated[1][-1]])

        status_list = [first_value,second_value]

    return status_list

def get_multiple_values(list):
    if list[0]=="status":
        return get_multiple_status(list[2])
    if list[0]=="Time_rep":
        return get_multiple_time(list[2])
