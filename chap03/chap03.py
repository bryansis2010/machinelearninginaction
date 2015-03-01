#-------------------------------------------------------------------------------
# Name:        chap03
#
# Author:      bryansis2010
#
# Created:     21/02/2015
#-------------------------------------------------------------------------------

#imports from the text
from math import log
from numpy import *

#my own imports to make things easier
import os

def calcShannonEntropy(dataSet):
    num_records = len(dataSet)
    label_counts = {}

    for features in dataSet:
        #get the last value of the record ie the class
        current_label = features[-1]
        if current_label not in label_counts:
            label_counts[current_label] = 1
        else:
            label_counts[current_label] +=1

    shannon_entropy = 0.0
    #print(label_counts)
    for key in label_counts:
        probability_of_value = (float)(label_counts[key])/num_records
        #log in python is taking natural log
        entropy_value = probability_of_value*math.log(probability_of_value, 2)
        shannon_entropy -= entropy_value
        #print(shannon_entropy)
    return shannon_entropy
#end calcShannonEntropy


def splitDataSet(dataSet, axis, value):
    ret_data_set = []
    for feature_vector in dataSet:
        if feature_vector[axis] == value:
            #--this line takes up to the column, without it
            reduced_feature_vector = feature_vector[:axis]
            #--this line takes everything after the coumn
            reduced_feature_vector.extend(feature_vector[axis+1:])
            #finally, add this smaller vector to the list of vectors
            ret_data_set.append(reduced_feature_vector)
    return ret_data_set
#end splitDataSet

def chooseBestFeatureToSplit(dataSet):
    #how many features are there in a vector?
    num_features = len(dataSet[0]) - 1
    #calculate the base entropy
    base_entropy = calcShannonEntropy(dataSet)
    #print("Base entropy : %f" % (base_entropy))
    best_info_gain = 0.0; best_feature = -1

    for i in range(num_features):
        #get the vertical array from the 2D array
        feature_list = [example[i] for example in dataSet]
        #print(feature_list)
        unique_values = set(feature_list)
        new_entropy = 0.0

        for value in unique_values:
            sub_data_set = splitDataSet(dataSet, i, value)
            probability = len(sub_data_set)/float(len(dataSet))
            new_entropy += probability * calcShannonEntropy(sub_data_set)
        #print("i = %d, New entropy : %f" % (i,new_entropy))
        info_gain = base_entropy - new_entropy
        #print("i = %d, Info_Gain = %f" % (i, info_gain))
        if info_gain > best_info_gain:
            best_info_gain = info_gain
            best_feature = i
    return best_feature
#end chooseBestFeatureToSplit

def majorityCount(classList):
    class_count = {}
    for vote in classList:
        if vote not in class_count.keys():
            class_count[vote] = 0
        class_count[vote] += 1
    sorted_class_count = sorted(classCount.items(),
    key=operater.itemgetter(1), reverse=True)
    return sorted_class_count[0]
#end majorityCount

def file2matrix(filename):
    fr = open(filename)
    num_lines = len(fr.readlines())
    returned_matrix = []
    class_label_vector = []

    fr = open(filename)
    index = 0
    for line in fr.readlines():
        line = line.strip()
        list_from_line = line.split('\t')
        #print(list_from_line)
        #substitutes the row of 0s to values from the text file
        returned_matrix.append(list_from_line[0:5])
        #adds the label using the last entry of the row.
        class_label_vector.append(list_from_line[-1])
        index += 1
    return returned_matrix, class_label_vector
#end file2matrix

def createTree(dataSet, labels):
    #get all the classes
    class_list = [example[-1] for example in dataSet]
    #print(class_list)
    #stop when all the classes are equal
    if (class_list.count(class_list[0]) == len(class_list)):
        return class_list[0]
    if (len(dataSet[0]) == 1):
        return majorityCount(class_list)

    best_feature = chooseBestFeatureToSplit(dataSet)
    best_feature_label = labels[best_feature]
    my_tree = {best_feature_label : {}}
    del(labels[best_feature])
    feature_values = [example[best_feature] for example in dataSet]
    unique_values = set(feature_values)

    for value in unique_values:
        sub_labels = labels[:]
        my_tree[best_feature_label][value] = createTree(
        splitDataSet(dataSet,best_feature,value),
        sub_labels)
    return my_tree
#end createTree

"""Example 3.1.1
dataSet = [
[1, 1, 'yes'],
[1, 1, 'yes'],
[1, 0, 'no'],
[0, 1, 'no'],
[0, 1, 'no']
]
labels = ['no surfacing','flippers']"""
#print(calcShannonEntropy(dataSet))

"""Example 3.1.2"""
#print(splitDataSet(dataSet,0,1))
#print(chooseBestFeatureToSplit(dataSet))

"""Children Example
http://stackoverflow.com/questions/1859554/what-is-entropy-and-information-gain
data_set_1 = [
['Jason', 'M'], ['Mark', 'M'], ['Josh', 'M'],
['Christian', 'M'], ['Tosh', 'M'], ['Al', 'M'],
['Iris', 'F'],
['Charlie', 'M'], ['Tommi', 'M'], ['Jackie', 'M'],
['Christie', 'F'],['Jackie', 'F'], ['Maci', 'F'], ['Nikki', 'F'],
]

print("H_1(Y) = %f" % (calcShannonEntropy(data_set_1)))
data_set_2_0 = [
['Jason', 'M'], ['Mark', 'M'], ['Josh', 'M'],
['Christian', 'M'], ['Tosh', 'M'], ['Al', 'M'],
['Iris', 'F'],
]
data_set_2_1 = [
['Charlie', 'M'], ['Tommi', 'M'], ['Jackie', 'M'],
['Christie', 'F'],['Jackie', 'F'], ['Maci', 'F'], ['Nikki', 'F'],
]
h_2_0 =calcShannonEntropy(data_set_2_0)
h_2_1 =calcShannonEntropy(data_set_2_1)
print("H_2,0(Y) = %f" % (h_2_0))
print("H_2,1(Y) = %f" % (h_2_1))
h_2 = h_2_0*7/14 + h_2_1*7/14
print("H_2(Y) = %f" % (h_2))
data_set_1_binary = [
['0', 'M'], ['0', 'M'], ['0', 'M'],
['0', 'M'], ['0', 'M'], ['0', 'M'],
['0', 'F'],
['1', 'M'], ['1', 'M'], ['1', 'M'],
['1', 'F'],['1', 'F'], ['1', 'F'], ['1', 'F'],
]
print(chooseBestFeatureToSplit(data_set_1_binary))"""

"""Example 3.1.3"""
#my_tree = createTree(dataSet,labels)


"""Example 3.4"""
resource_path = os.path.dirname(__file__)
file_name = 'resource\lenses.txt'
lenses_txtfile = os.path.join(resource_path, file_name)
lenses_data_matrix, lenses_labels = file2matrix(lenses_txtfile)
lenseslabels = ['age', 'prescript', 'astigmatic', 'tearRate']
my_tree = createTree(lenses_data_matrix,lenseslabels)