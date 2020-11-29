#BIN_SIZE = 30
#START_TIME = 0
import pandas as pd
from pandas import DataFrame
import xlsxwriter
import heart_rate
import os
import re

def get_labels(file):
    times = []
    datapts = []

    with open(file, "r") as filestream:
        for line in filestream:
            elem = re.findall(r'[^,;\s]+', line)
            time = float(elem[0])
            times.append(time)
            # collect datapoints
            datapts.append(float(elem[1]))
    return times, datapts


def parse_patient_data(file, start,end):
    patients = []
    times = []
    datapts = []

    patient = ((re.findall('\d+', file)))[0]
    with open(file, "r") as filestream:
        for line in filestream:

            elem = re.findall(r'[^,;\s]+', line)
            time = float(elem[0])

            if(float(time > start) and float(time < end)):

                times.append(time)
                #collect datapoints
                patients.append(patient)
                if (len(elem) == 2):
                    datapts.append(float(elem[1]))

                #if the dataset has more than one datapoint ex.accleration
                else:
                    datapt = []
                    for i in range(1, len(elem)):
                        datapt.append(float(elem[i]))
                    datapts.append(datapt)

    print("patient " + ((re.findall('\d+', file )))[0] + " done")
    return patients, times, datapts

def collect_labels(directory):
    patient_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file = os.path.join(directory, filename)
            patient_files.append(get_labels(file))
        else:
            continue
    return patient_files


def collect_data(directory,start, labels):
    patient_files = []
    print(directory + ' data:')
    i = 0
    for filename in os.listdir(directory):
        sleep_label_time = labels[i][0]
        end = sleep_label_time[-1]

        if filename.endswith(".txt"):
            file = os.path.join(directory, filename)
            patient_files.append(parse_patient_data(file,start,end))
        else:
            continue
    return patient_files

#two_bins must be fed a data set with time data and corresponding output data
#def to_bins(dataset, bins):
 #   for
  #  return

def main():
    #returns patient heart rate data
    sleep_labels = collect_labels('labels')

    heart_rate_data = collect_data('heart_rate',0,sleep_labels)
    #example: patient 1: out put is list with time stamp and heart rate at that time
    #print(heart_rate_data[0])

    df_list =[]
    for item in heart_rate_data:

        df = DataFrame(item).transpose()
        df.columns = ['patient','time','heart rate']
        df.set_index('patient', inplace=True, drop=True)
        df_list.append(df)
    tot_data = pd.concat(df_list)
    print(tot_data)

    # create excel writer
    writer = pd.ExcelWriter('hr_output.xlsx')
    # write dataframe to excel sheet named 'marks'
    tot_data.to_excel(writer,'hr')
    # save the excel file
    writer.save()
    print('DataFrame is written successfully to Excel Sheet.')

    # returns patient steps data
    #steps_data = collect_data('steps')

    # returns patient motion data
    #motion_data = collect_data('motion')

    #collects labelled sleep


   # to_bins(heart_rate_data, sleep_labels)

main()
