import math
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import string
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user= "root",
    passwd="",
    database="news"
)

mycursor = mydb.cursor()
mycursor.execute("SELECT content FROM news_tb")
documents = mycursor.fetchall()

#token stem stop
dictOfWords = {}

for index, sentence in enumerate(documents):
    for b in sentence:
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        output = stemmer.stem(b)
        output = output.translate(str.maketrans('', '', string.punctuation)).lower()
    tokenizedWords = word_tokenize(output)

    listStopword = set(stopwords.words('indonesian'))

    wordsFiltered = []
    for t in tokenizedWords:
        if t not in listStopword:
            wordsFiltered.append(t)
    dictOfWords[index] = [(word,wordsFiltered.count(word)) for word in wordsFiltered]
print(dictOfWords)

#Menghilangkan kata duplikat
termFrequency = {}

for i in range(0, len(documents)):
    listOfNoDuplicates = []
    for wordFreq in dictOfWords[i]:
        if wordFreq not in listOfNoDuplicates:
            listOfNoDuplicates.append(wordFreq)
        termFrequency[i] = listOfNoDuplicates
print(termFrequency)
#
# #Third: normalized term frequency
# normalizedTermFrequency = {}
# for i in range(0, len(documents)):
#     sentence = dictOfWords[i]
#     lenOfSentence = len(sentence)
#     listOfNormalized = []
#     for wordFreq in termFrequency[i]:
#         normalizedFreq = wordFreq[1]/lenOfSentence
#         listOfNormalized.append((wordFreq[0],normalizedFreq))
#     normalizedTermFrequency[i] = listOfNormalized
#
# #print(normalizedTermFrequency)
#
#
# #---Calculate IDF
#
# #First: put al sentences together and tokenze words
#
# allDocuments = ''
# for sentence in documents:
#     allDocuments += sentence + ' '
# allDocumentsTokenized = allDocuments.split(' ')
#
# #print(allDocumentsTokenized)
#
# allDocumentsNoDuplicates = []
#
# for word in allDocumentsTokenized:
#     if word not in allDocumentsNoDuplicates:
#         allDocumentsNoDuplicates.append(word)
#
#
# #print(allDocumentsNoDuplicates)
#
# #Second calculate the number of documents where the term t appears
#
# dictOfNumberOfDocumentsWithTermInside = {}
#
# for index, voc in enumerate(allDocumentsNoDuplicates):
#     count = 0
#     for sentence in documents:
#         if voc in sentence:
#             count += 1
#     dictOfNumberOfDocumentsWithTermInside[index] = (voc, count)
#
# #print(dictOfNumberOfDocumentsWithTermInside)
#
#
# #calculate IDF
#
# dictOFIDFNoDuplicates = {}
#
#
# for i in range(0, len(normalizedTermFrequency)):
#     listOfIDFCalcs = []
#     for word in normalizedTermFrequency[i]:
#         for x in range(0, len(dictOfNumberOfDocumentsWithTermInside)):
#             if word[0] == dictOfNumberOfDocumentsWithTermInside[x][0]:
#                 listOfIDFCalcs.append((word[0],math.log(len(documents)/dictOfNumberOfDocumentsWithTermInside[x][1])))
#     dictOFIDFNoDuplicates[i] = listOfIDFCalcs
#
# #print(dictOFIDFNoDuplicates)
#
# #Multiply tf by idf for tf-idf
#
# dictOFTF_IDF = {}
# for i in range(0,len(normalizedTermFrequency)):
#     listOFTF_IDF = []
#     TFsentence = normalizedTermFrequency[i]
#     IDFsentence = dictOFIDFNoDuplicates[i]
#     for x in range(0, len(TFsentence)):
#         listOFTF_IDF.append((TFsentence[x][0],TFsentence[x][1]*IDFsentence[x][1]))
#     dictOFTF_IDF[i] = listOFTF_IDF
#
# print(dictOFTF_IDF)
#
# from nltk.text import TextCollection
#
# mytexts = TextCollection(['the the universe has very many stars','the galaxy contains many stars','the cold breeze of winter made it very cold outside'])
#
# print("NLTK tf_idf")
# print(mytexts.tf_idf('very','the the universe has very many stars'))
#
# def test_tf(term, text):
#     newText = text.split(' ')
#     print(text.count(term))
#     print(len(newText))

#test_tf('universe','the the universe has very many stars')