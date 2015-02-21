#-------------------------------------------------------------------------------
# Name:        chap02
#
# Author:      bryansis2010
#
# Created:     21/02/2015
#-------------------------------------------------------------------------------

#imports relevant to the text
from numpy import *
import operator
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.legend_handler

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
    """Covered in the explanation"""
    diff_matrix = tile(in_X, (data_set_size, 1)) - data_set
    sq_diff_matrix = diff_matrix**2
    sq_distances = sq_diff_matrix.sum(axis=1)
    distances = sq_distances**0.5
    sorted_dist_indices = distances.argsort()

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
        #substitutes the row of 0s to values from the text file
        returned_matrix [index, :] = list_from_line[0:3]
        #adds the label using the last entry of the row.
        class_label_vector.append(int(list_from_line[-1]))
        index += 1
    return returned_matrix, class_label_vector
#end file2matrix


def autoNorm(data_set):
    min_vals = data_set.min(0)
    max_vals = data_set.max(0)
    ranges = max_vals - min_vals
    normalised_data_set = zeros(shape(data_set))
    num_records = data_set.shape[0]
    normalised_data_set = data_set - tile(min_vals, (num_records, 1))
    normalised_data_set = normalised_data_set/tile(ranges, (num_records, 1))
    return normalised_data_set, ranges, min_vals
#end autoNorm

def datingClassTest():
    resource_path = os.path.dirname(__file__)
    file_name = 'resource\datingTestSet2.txt'
    dating_test_txtfile = os.path.join(resource_path, file_name)

    hoRatio = 0.10
    dating_data_matrix, dating_labels = file2matrix(dating_test_txtfile)
    normalized_data_set, ranges, min_vals = autoNorm(dating_data_matrix)
    num_records = normalized_data_set.shape[0]
    num_test_vectors = int(num_records*hoRatio)
    error_count = 0.0

    for i in range(num_test_vectors):
        classifier_result = classify0(normalized_data_set[i,:],
        normalized_data_set[num_test_vectors:num_records, :],
        dating_labels[num_test_vectors:num_records], 3)
        print("the classifier came back with : %d, the real answer is %d"
        %(classifier_result, dating_labels[i]))
        if(classifier_result != dating_labels[i]):
            error_count += 1.0
            #print("Error!")
    print("the total error rate is : %f" %(error_count/float(num_test_vectors)))
#end datingClassTest

def classifyPerson():
    resource_path = os.path.dirname(__file__)
    file_name = 'resource\datingTestSet2.txt'
    dating_test_txtfile = os.path.join(resource_path, file_name)

    result_list = ["not at all", "in small doses", "in large doses"]
    pct_video_games = float(input("percentage of time spent playing video games?"))
    num_flier_miles = float(input("frequent flier miles earned per year?"))
    ltr_ice_cream = float(input("liters of ice cream consumed per week?"))
    dating_data_matrix, dating_labels = file2matrix(dating_test_txtfile)
    normalized_data_set, ranges, min_vals = autoNorm(dating_data_matrix)
    input_vector = array([num_flier_miles, pct_video_games, ltr_ice_cream])
    input_vector = (input_vector-min_vals)/ranges
    classifierResult = classify0(input_vector,normalized_data_set,
    dating_labels,3)
    print ("You will probably like this person: %s" % result_list[classifierResult - 1])
#end classifyPerson


"""Example 2.1
group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
labels = ['A','A','B','B']
print(classify0([0.6, 0.6], group, labels, 3))"""

"""Example 2.2.1
resource_path = os.path.dirname(__file__)
file_name = 'resource\datingTestSet2.txt'
dating_test_txtfile = os.path.join(resource_path, file_name)
dating_data_matrix, dating_labels = file2matrix(dating_test_txtfile)"""

"""Example 2.2.2 - Fig 2.3 (use with Eg. 2.2.1)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(dating_data_matrix[:, 1], dating_data_matrix[:, 2])
ax.set_xlabel("Percentage of Time Spent Playing Video Games")
ax.set_ylabel("Liters of Ice Cream Consumed Per Week")
plt.show()"""

"""Example 2.2.2 - Fig 2.4 (use with Eg. 2.2.1)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(dating_data_matrix[:, 1], dating_data_matrix[:, 2],
15.0*array(dating_labels), 15.0*array(dating_labels))
ax.set_xlabel("Percentage of Time Spent Playing Video Games")
ax.set_ylabel("Liters of Ice Cream Consumed Per Week")
plt.show()"""

"""Example 2.2.2 - Fig 2.5 (use with Eg. 2.2.1)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(dating_data_matrix[:, 0], dating_data_matrix[:, 1],
15.0*array(dating_labels), 15.0*array(dating_labels))
ax.set_xlabel("Frequent Flier Miles Earned per Year")
ax.set_ylabel("Percentage of Time Spent Playing Video Games")
plt.show()"""

"""Example 2.2.3
normalized_data_set, ranges, min_vals = autoNorm(dating_data_matrix)"""

"""Example 2.2.4
datingClassTest()"""

"""Example 2.2.5
classifyPerson()"""

"""Example 2.3.1"""
def img2vector(filename):
    return_vector = zeros((1, 1024))
    fr= open(filename)
    for i in range(32):
        row = fr.readline()
        for j in range(32):
            return_vector[0, 32*i+j] = int(row[j])
    return return_vector
#end img2vector

def handwritingClassTest():
    handwriting_labels = []

    resource_path = os.path.dirname(__file__)
    training_file_list = os.listdir(os.path.join(resource_path,'resource\\trainingDigits'))
    num_records = len(training_file_list)
    #print("No. of training records = %d" % (num_records))
    training_matrix = zeros((num_records, (32*32)))

    for i in range(num_records):
        file_name_string = training_file_list[i]
        file_name = file_name_string.split('.')[0]
        class_num_string = int(file_name.split('_')[0])
        #add the labels
        handwriting_labels.append(class_num_string)
        training_matrix[i, :] = img2vector(os.path.join(resource_path,'resource\\trainingDigits\\',file_name_string))

    test_file_list = os.listdir(os.path.join(resource_path,'resource\\testDigits'))
    error_count = 0.0
    num_test_records = len(test_file_list)

    for j in range(num_test_records):
        file_name_string = test_file_list[j]
        file_name = file_name_string.split('.')[0]
        class_num_string = int(file_name.split('_')[0])
        test_vector = img2vector(os.path.join(resource_path,'resource\\trainingDigits\\',file_name_string))
        result = classify0(test_vector, training_matrix, handwriting_labels, 4)
        #print("%d. the classifier came back with : %d, the real answer is %d"
        #% (j, result, class_num_string))
        if(result != class_num_string):
            error_count += 1.0
    print("the total number of errors is: %d" % error_count)
    print("the total error rate is %f" % (error_count/(num_test_records)))
#end handwritingClassTest

handwritingClassTest()
