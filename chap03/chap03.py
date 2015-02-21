#-------------------------------------------------------------------------------
# Name:        chap03
#
# Author:      bryansis2010
#
# Created:     21/02/2015
#-------------------------------------------------------------------------------

#imports from the text
from math import log

def calcShannonEntropy(dataSet):
    num_records = len(dataSet)
    label_counts = {}

    for features in dataSet:
        current_label = features[-1]
        if current_label not in label_counts:
            label_counts[current_label] = 1
        else:
            label_counts[current_label] +=1

    shannon_entropy = 0.0

    for key in label_counts:
        probability_of_value = (float)(label_counts[key])/num_records
        entropy_value = probability_of_value*log(probability_of_value, 2)
        shannon_entropy -= entropy_value

    return shannon_entropy
#end calcShannonEntropy

"""Example 3.1.1"""
dataSet = [[1, 1, 'yes'],
[1, 1, 'yes'],
[1, 0, 'no'],
[0, 1, 'no'],
[0, 1, 'no']]
labels = ['no surfacing','flippers']
