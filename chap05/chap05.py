#-------------------------------------------------------------------------------
# Name:        chap05
#
# Author:      bryansis2010
#
# Created:     05/04/2015
#-------------------------------------------------------------------------------
#imports relevant to the text
from numpy import *
import re
#my own imports to make things easier
import os

resource_path = os.path.dirname(__file__)
file_name = r"resource\testSet.txt"
testSet_txtfile = ("%s\%s" % (resource_path, file_name))
testSet_fh = open(testSet_txtfile)
testSet_text = testSet_fh.readlines()

dataMat = []; labelMat = []
for line in testSet_text:
    line_array = line.split("\t")
    dataMat.append([1.0, float(line_array[0]), float(line_array[1])])
    labelMat.append(int(line_array[-1]))

#print(testSet_text)