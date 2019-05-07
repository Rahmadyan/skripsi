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
# for x in documents:
#     print(x)

#1. tokenizing stopword dan stemming
dictOfWords = {}

for index, sentence in enumerate(documents):
    for b in sentence:
        b = b.translate(str.maketrans('', '', string.punctuation))

    tokenizedWords = word_tokenize(b)

    listStopword = set(stopwords.words('indonesian'))

    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    wordsFiltered = []
    for t in tokenizedWords:
        if t not in listStopword:
            wordsFiltered.append(t)
    wordsFiltered = [stemmer.stem(word) for word in wordsFiltered]
    dictOfWords[index] = [(word,wordsFiltered.count(word)) for word in wordsFiltered]
# print(dictOfWords)

#2. Menghilangkan kata duplikat
termFrequency = {}

for i in range(0, len(documents)):
    listOfNoDuplicates = []
    for wordFreq in dictOfWords[i]:
        if wordFreq not in listOfNoDuplicates:
            listOfNoDuplicates.append(wordFreq)
        termFrequency[i] = listOfNoDuplicates
# print(termFrequency)

#3. Normalisasi TF
#Kemunculan kata/istilah(t) dalam kalimat / jumlah kata dalam dokumen/kalimat(d)
normalizedTermFrequency = {}
for i in range(0, len(documents)):
    sentence = dictOfWords[i]
    lenOfSentence = len(sentence) #menghitung jumlah kata dalam kalimat
    # print(lenOfSentence)
    listOfNormalized = []
    for wordFreq in termFrequency[i]:
        normalizedFreq = wordFreq[1]/lenOfSentence #pembagain kemunculan kata dengan jumlah kata dalam kalimat
        listOfNormalized.append((wordFreq[0],normalizedFreq))
    normalizedTermFrequency[i] = listOfNormalized
# print(normalizedTermFrequency)

#4.IDF ngelu
# RUMUS = log(n/df) n= jumlah dokumen df = jumlah dokumen dimana istilah/kata itu muncul

allDocuments = ''
for sentence in documents:
    for w in sentence:
        allDocuments += w + ' '
    allDocuments = allDocuments.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(allDocuments)
listStop = set(stopwords.words('indonesian'))

stemm = StemmerFactory()
stemmer = stemm.create_stemmer()

wordsFilter = []
for t in tokens:
    if t not in listStop:
        wordsFilter.append(t)
wordsFilter = [stemmer.stem(word) for word in wordsFilter]
print(wordsFilter)


#IKI PERCOBAAN JANGAN HIRAUKAN
# for t in tokenizedWords:
#     if t not in listStopword:
#         allDocumentsNoDuplicates.append(t)
# for w in allDocumentsNoDuplicates:
#     print(w)

