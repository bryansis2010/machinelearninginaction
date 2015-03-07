#-------------------------------------------------------------------------------
# Name:        chap04
#
# Author:      bryansis2010
#
# Created:     07/03/2015
#-------------------------------------------------------------------------------

#imports relevant to the text
from numpy import *
import re
#my own imports to make things easier
import os

def createVocabList(dataSet):
    """Creates a set of all unique words from the dataset"""
    vocab_set = set([])
    for document in dataSet:
        vocab_set = vocab_set | set(document)
    return list(vocab_set)
#end createVocabList

def setOfWordsToVec(vocab_list, input_set):
    vector_to_return = zeros(len(vocab_list))
    #print(vector_to_return)
    for word in input_set:
        if word in vocab_list:
            vector_to_return[vocab_list.index(word)] = 1
        else:
            print("The word: %s is not in my Vocabulary!" % (word))
    return vector_to_return
#end setOfWordsToVec

def bagOfWordsToVecNM(vocab_list, input_set):
    vector_to_return = zeros(len(vocab_list))
    #print(vector_to_return)
    for word in input_set:
        if word in vocab_list:
            vector_to_return[vocab_list.index(word)] += 1
    return vector_to_return
#end bagOfWordsToVecNM

def trainNB0(trainMatrix, trainCategory):
    num_train_docs = len(trainMatrix)
    num_words = len(trainMatrix[0])
    prob_abusive = sum(trainCategory)/float(num_train_docs)
    #prob_0_num = zeros(num_words); prob_1_num = zeros(num_words)
    #prob_0_denom = 0.0; prob_1_denom = 0.0

    prob_0_num = ones(num_words); prob_1_num = ones(num_words)
    prob_0_denom = 2.0; prob_1_denom = 2.0

    for i in range(num_train_docs):
        if trainCategory[i] == 1:
            prob_1_num += trainMatrix[i]
            prob_1_denom += sum(trainMatrix[i])
        else:
            prob_0_num += trainMatrix[i]
            prob_0_denom += sum(trainMatrix[i])

    #prob_1_vector = prob_1_num / prob_1_denom
    #prob_0_vector = prob_0_num / prob_0_denom

    prob_1_vector = log(prob_1_num / prob_1_denom)
    prob_0_vector = log(prob_0_num / prob_0_denom)
    return prob_0_vector, prob_1_vector, prob_abusive

def classifyNB(vec_to_classify, p0vec, p1vec, pClass1):
    p1 = sum(vec_to_classify * p1vec) + log(pClass1)
    p0 = sum(vec_to_classify * p0vec) + log(1.0 - pClass1)

    if p1 > p0:
        return 1
    else:
        return 0
#end classifyNB

def textParse(bigString):
    list_of_tokens = re.split(r'\W*', bigString)
    return [tok.lower() for tok in list_of_tokens if len(tok) > 2]
#end textParse

def spamTest(resource_path):
    doc_list = []; class_list = []; full_text = []

    resource_path = os.path.dirname(__file__)

    for i in range(1, 26):


        #get the bigString
        spam_file_name = r"resource\email\spam\%d.txt" % i
        spam_txtfile = ("%s\%s" % (resource_path, spam_file_name))
        spam_file_handler = open(spam_txtfile)
        spam_text = spam_file_handler.read()
        #...followed by the word_list
        word_list = textParse(spam_text)
        doc_list.append(word_list)
        full_text.extend(word_list)
        class_list.append(1)

        #get the bigString
        ham_file_name = r"resource\email\ham\%d.txt" % i
        ham_txtfile = ("%s\%s" % (resource_path, ham_file_name))
        ham_file_handler = open(ham_txtfile)
        ham_text = ham_file_handler.read()
        #...followed by the word_list
        word_list = textParse(ham_text)
        doc_list.append(word_list)
        full_text.extend(word_list)
        class_list.append(0)

    vocab_list = createVocabList(doc_list)
    training_set = list(range(50)) ; test_set = []

    for i in range(30):
        rand_index = int(random.uniform(0, len(training_set)))
        test_set.append(training_set[rand_index])
        training_set.pop(rand_index)

    train_matrix = []; train_classes = []

    for doc_index in training_set:
        train_matrix.append(setOfWordsToVec(vocab_list, doc_list[doc_index]))
        train_classes.append(class_list[doc_index])

    p0V, p1V, pSpam = trainNB0(array(train_matrix), array(train_classes))

    error_count = 0

    for doc_index2 in test_set:
        word_vector = setOfWordsToVec(vocab_list, doc_list[doc_index2])
        if(classifyNB(array(word_vector), p0V, p1V, pSpam) != class_list[doc_index2]):
            print("Classification Error: ", word_vector)
            error_count += 1
    print("The error rate is : %f" % (float(error_count)/len(test_set)))
#end spamTest
"""4.5
postingList = [
            ['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
            ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
            ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
            ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
            ['mr', 'licks', 'ate', 'my', 'steak', 'how','to', 'stop', 'him'],
            ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid'],
            ]

classVec = [0,1,0,1,0,1] #1 is abusive, 0 not

set_of_words = createVocabList(postingList)

train_mat = []

for p in postingList:
    train_mat.append(setOfWordsToVec(set_of_words, p))

p0v, p1v, pAb = trainNB0(array(train_mat), array(classVec))

test_entry = ['love', 'my', 'dalmation']
this_document = array(setOfWordsToVec(set_of_words, test_entry))
print(test_entry, " classified as: ", classifyNB(this_document, p0v, p1v, pAb))

test_entry = ['stupid', 'my', 'garbage']
this_document = array(setOfWordsToVec(set_of_words, test_entry))
print(test_entry, " classified as: ", classifyNB(this_document, p0v, p1v, pAb))"""

#mySent='This book is the best book on Python or M.L. I have ever laid eyes upon.'

"""
resource_path = os.path.dirname(__file__)
file_name = r"resource\email\ham\6.txt"
email6_txtfile = ("%s\%s" % (resource_path, file_name))
file_handler = open(email6_txtfile)
email_text = file_handler.read()
regEx = re.compile('\\W*')
list_of_tokens = regEx.split(email_text)"""
resource_path = os.path.dirname(__file__)
spamTest(resource_path)