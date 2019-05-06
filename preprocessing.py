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
for x in documents:
    print(x)

#1. tokenizing stopword dan stemming
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

#2. Menghilangkan kata duplikat
termFrequency = {}

for i in range(0, len(documents)):
    listOfNoDuplicates = []
    for wordFreq in dictOfWords[i]:
        if wordFreq not in listOfNoDuplicates:
            listOfNoDuplicates.append(wordFreq)
        termFrequency[i] = listOfNoDuplicates
print(termFrequency)

#3. Normalisasi TF
#Kemunculan kata/istilah(t) dalam kalimat / jumlah kata dalam dokumen/kalimat(d)
normalizedTermFrequency = {}
for i in range(0, len(documents)):
    sentence = dictOfWords[i]
    lenOfSentence = len(sentence) #menghitung jumlah kata dalam kalimat
    listOfNormalized = []
    for wordFreq in termFrequency[i]:
        normalizedFreq = wordFreq[1]/lenOfSentence #pembagain kemunculan kata dengan jumlah kata dalam kalimat
        listOfNormalized.append((wordFreq[0],normalizedFreq))
    normalizedTermFrequency[i] = listOfNormalized
print(normalizedTermFrequency)

#4.IDF ngelu
# RUMUS = log(n/df) n= jumlah dokumen df = jumlah dimana istilah/kata muncul

allDocuments = ''
for sentence in documents:
    for f in sentence:
        allDocuments += f + ' '
# print(allDocuments)
# allDocumentsTokenized = allDocuments.split(' ')

# print(allDocumentsTokenized)
#
# allDocumentsNoDuplicates = []
#
# for word in allDocumentsTokenized:
#     if word not in allDocumentsNoDuplicates:
#         allDocumentsNoDuplicates.append(word)
# allDocumentsNoDuplicates = []

#IKI PERCOBAAN JANGAN HIRAUKAN
# for t in tokenizedWords:
#     if t not in listStopword:
#         allDocumentsNoDuplicates.append(t)
# for w in allDocumentsNoDuplicates:
#     print(w)

