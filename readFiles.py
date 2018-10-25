''' ===================== HYBRID SELECTION STRATEGY (HSS) ======================
        Universidade Federal de Sao Carlos - UFSCar, Sorocaba - SP - Brazil

        Master of Science Project       Artificial Intelligence

        Prof. Tiemi Christine Sakata    (tiemi@ufscar.br)
        Author: Vanessa Antunes         (tunes.vanessa@gmail.com)
   
    ============================================================================ '''

import sys, getopt
import numpy as np
import os

def sentence():
    print 'Usage: selection.py -p <partitions_path> -d <dataset_path> -t <true_partition_path> -o <output_path> -f <plot_path> -a <region division algorithm: 1- kmeans, 2- single-link, 3- complete-link, 4- average-link, 5- ward> -c <percentage selection (ex: 0.3)>'

def inOut(argv):

    try:
        opts, args = getopt.getopt(argv,"hp:d:t:o:f:a:c:",["partitions=","dataset=", "tp=", "output=", "figure=", "algorithm=", "percentage="])

    #   Exception getopt.GetoptError: This is raised when an unrecognized option is found in the argument list or when an option requiring an argument is given none. 
    except getopt.GetoptError:
        sentence()
        sys.exit(2)

    if len(opts) < 7:
        sentence()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            sentence()
            sys.exit()
        elif opt in ("-p", "--partitions"):
            partitionsPath = arg
        elif opt in ("-d", "--dataset"):
            dataset = arg
        elif opt in ("-t", "--tp"):
            tpPath = arg
        elif opt in ("-o", "--output"):
            output = arg
            outputreg = arg
        elif opt in ("-f", "--figure"):
            figureName = arg
        elif opt in ("-a", "--algorithm"):
            algorithm = arg
        elif opt in ("-c", "--percentage"):
            percentage = float(arg)

    figureName += '/' + dataset.split('/')[-1].split('.')[0] + '.png'
    output += dataset.split('/')[-1].split('.')[0] + '.csv'
    outputreg += dataset.split('/')[-1].split('.')[0]
    # for mock and mocle:
    #output += partitionsPath.split('/')[5] + "/" + partitionsPath.split('/')[5] + '_' + partitionsPath.split('/')[6] + '.csv'

    print 'Partitions path: ', partitionsPath
    print 'Dataset: ', dataset
    print 'TP path is: ', tpPath
    print 'Output Path: ', output
    print 'Figure Name: ', figureName
    print 'Algorithm: ', algorithm
    print 'Percentage: ', percentage

    return partitionsPath, dataset, tpPath, output, figureName, algorithm, percentage, outputreg


def whichSplit(text):
    if '\t' in text:
        spt = '\t'
    else:
        spt = ' '
    return spt

def readPartitions(partitionPath):
    
    # Read partitions
    numberOfFiles = len(os.listdir(partitionPath))
    partitions = []
    name = []

    mydt = np.dtype([('id', np.str_, 100), ('cluster', np.int)])

    for _ in range(0, numberOfFiles):
        file = os.listdir(partitionPath)[_]
        name.append(file)

        absoluteFileName = os.path.join(partitionPath, file)
        with open(absoluteFileName) as f:
            lines = f.readlines()

        spt = whichSplit(lines[0])
        lines = [line.strip('\n').split(spt) for line in lines] 


        part = np.array([(lines[0][0], int(lines[0][1]))], dtype = mydt)
        
        for __ in range(1, len(lines)):
            part = np.insert(part, len(part), (lines[__][0], int(lines[__][1])), axis=0)

        part.sort(order='id')
        partitions.append(part)

    return name, partitions


def readDataset(datasetPath):
    # Read dataset to np.array
    lines = [line.rstrip('\r\n') for line in open(datasetPath)]
    spt = whichSplit(lines[1])
    nAtrib = len(lines[1].split(spt))
    mydt = np.dtype([('id', np.str_, 32), ('atrib', np.float32, (nAtrib - 1,))])

    l = []
    for __ in range(1, nAtrib):
        l.append(float(lines[1].split(spt)[__]))
    dataset = np.array([(lines[1].split(spt)[0], l)], dtype = mydt)
    for _ in lines[2:]:
        l = []
        for __ in range(1, nAtrib):
            l.append(float(_.split(spt)[__]))
        
        dataset = np.insert(dataset, len(dataset), (_.split(spt)[0], l), axis=0)

    dataset.sort(order='id')

    return dataset
