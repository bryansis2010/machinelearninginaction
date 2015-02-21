#-------------------------------------------------------------------------------
# Name:        chap02
#
# Author:      bryansis2010
#
# Created:     21/02/2015
#-------------------------------------------------------------------------------

#imports from the textbook
from numpy import *
import operator

#my own imports to make things easier
import os

def classify0(in_X, data_set, labels, k):
    """
    in_X : the data point to classify
    data_set : list of all data points
    labels : vector of labels / buckets
    k : the no. of vectors used for voting

    returns : the label that the data point belongs to
    """

    #Find out the no. of elements in the data_set
    data_set_size = data_set.shape[0]
    diff_matrix = tile(in_X, (data_set_size, 1)) - data_set
    sq_diff_matrix = diff_matrix**2
    sq_distances = sq_diff_matrix.sum(axis=1)
    distances = sq_distances**0.5
    sorted_dist_indices = distances.argsort()
    print(sorted_dist_indices)
    class_histogram = {}

    for i in range(k):
        vote_label = labels[sorted_dist_indices[i]]
        class_histogram [vote_label] = class_histogram.get(vote_label, 0) + 1

    sorted_histogram = sorted(class_histogram.items(),
    key=operator.itemgetter(1), reverse=True)

    return sorted_histogram[0][0]

#end classify0


def file2matrix(filename):
    fr = open(filename)
    num_lines = len(fr.readlines())
    returned_matrix = zeros((num_lines,3))
    class_label_vector = []

    fr = open(filename)
    index = 0
    for line in fr.readlines():
        line = line.strip()
        list_from_line = line.split('\t')
        returned_matrix [index, :] = list_from_line[0:3]
        class_label_vector.append(int(list_from_line[-1]))
        index += 1
    return returned_matrix, class_label_vector
#end file2matrix


"""Example 2.1"""
group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
labels = ['A','A','B','B']
print(classify0([0.6, 0.6], group, labels, 3))

"""Example 2.2.1"""
datingDataMat, datingLabels = file2matrix