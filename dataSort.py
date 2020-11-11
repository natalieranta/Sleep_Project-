BIN_SIZE = 30
START_TIME = 0

import heart_rate
import os
import re

def parse_patient_data(file):
    times = []
    datapts = []
    with open(file, "r") as filestream:
        for line in filestream:

            elem = re.findall(r'[^,;\s]+', line)
            time = float(elem[0])

            if(float(time > START_TIME)):

                times.append(time)
                #collect datapoints
                if (len(elem) == 2):
                    datapts.append(float(elem[1]))

                #if the dataset has more than one datapoint ex.accleration
                else:
                    datapt = []
                    for i in range(1, len(elem)):
                        datapt.append(float(elem[i]))
                    datapts.append(datapt)

    print("patient " + ((re.findall('\d+', file )))[0] + " done")
    return times, datapts

def collect_data(directory):
    patient_files = []
    print(directory + ' data:')
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file = os.path.join(directory, filename)
            patient_files.append(parse_patient_data(file))
        else:
            continue
    return patient_files


def main():
    #returns patient heart rate data
    heart_rate_data = collect_data('heart_rate')

    #example: patient 1: out put is list with time stamp and heart rate at that time
    print(heart_rate_data[0])

    # returns patient steps data
    #steps_data = collect_data('steps')

    # returns patient motion data
    #motion_data = collect_data('motion')

    #collects labelled sleep
    #sleep_labels = collect_data('labels')

main()
