import math
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import string
import itertools
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user= "root",
    passwd="",
    database="news"
)

mycursor = mydb.cursor()
mycursor.execute("SELECT content FROM news_tb")
x = mycursor.fetchall()
# print(x)
# print(x)
documents = list(itertools.chain(*x))
# print(documents)

# documents = [list(x) for x in b]
# print(documents)

#1. tokenizing stopword dan stemming
dictOfWords = {}

for index, sentence in enumerate(documents):
    sentence = sentence.translate(str.maketrans('', '', string.punctuation))
    # print(sentence)
    tokenizedWords = word_tokenize(sentence)

    listStopword = set(stopwords.words('indonesian'))

    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    wordsFiltered = []
    for t in tokenizedWords:
        if t not in listStopword:
            wordsFiltered.append(t)
    wordsFiltered = [stemmer.stem(word) for word in wordsFiltered]
    dictOfWords[index] = [(word,wordsFiltered.count(word)) for word in wordsFiltered]
# print(wordsFiltered)


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
print(normalizedTermFrequency)

#4.IDF ngelu

allDocuments = ''
for sentence in documents:
    allDocuments += sentence + ' '
allDocuments = allDocuments.translate(str.maketrans('', '', string.punctuation))

# print(allDocuments)
tokens = word_tokenize(allDocuments)
listStop = set(stopwords.words('indonesian'))
stemm = StemmerFactory()
stemmer = stemm.create_stemmer()

wordsFilter = []
for t in tokens:
    if t not in listStop:
        wordsFilter.append(t)
wordsFilter = [stemmer.stem(word) for word in wordsFilter]
# print(wordsFilter)

allDocumentsNoDuplicate = []
for word in wordsFilter:
    if word not in allDocumentsNoDuplicate:
        allDocumentsNoDuplicate.append(word)
# print(allDocumentsNoDuplicate)


#Menghitung jumlah dokumen dimana istilah/kata itu muncul (DF)

jumlahDokumenDimanaKataMuncul = {}
for index, voc in enumerate(allDocumentsNoDuplicate):
    count = 0
    for sentence in wordsFilter:
        if voc in sentence:
            count += 1
    jumlahDokumenDimanaKataMuncul[index] = (voc, count)
# print(jumlahDokumenDimanaKataMuncul)

# IDF RUMUS = log(n/df) n= jumlah dokumen df = jumlah dokumen dimana istilah/kata itu muncul
dictOFIDFNoDuplicates = {}
for i in range(0, len(normalizedTermFrequency)):
    listOfIDFCalcs = []
    for word in normalizedTermFrequency[i]:
        for x in range(0, len(jumlahDokumenDimanaKataMuncul)):
            if word[0] == jumlahDokumenDimanaKataMuncul[x][0]:
                listOfIDFCalcs.append((word[0],math.log10(len(documents)/jumlahDokumenDimanaKataMuncul[x][1])))
    dictOFIDFNoDuplicates[i] = listOfIDFCalcs

print(dictOFIDFNoDuplicates)

#Multiply tf by idf for tf-idf

dictOFTF_IDF = {}
for i in range(0,len(normalizedTermFrequency)):
    listOFTF_IDF = []
    TFsentence = normalizedTermFrequency[i]
    # print(TFsentence)
    IDFsentence = dictOFIDFNoDuplicates[i]
    # print(IDFsentence)
    for x in range(0, len(TFsentence)):
        listOFTF_IDF.append((TFsentence[x][0],TFsentence[x][1]*IDFsentence[x][1]))
    dictOFTF_IDF[i] = listOFTF_IDF
    # dictOFTF_IDF = listOFTF_IDF
# print(dictOFTF_IDF)

# print(math.log10(7/5))















    # print(dictOFTF_IDF)
# sql = """INSERT INTO preprocessing_tb (id, preprocessing, news_id) VALUES ('%s', '%s', '%s')"""
      # "SELECT preprocessing_tb.id, preprocessing_tb.preprocessing, preprocessing_tb.news_id FROM news_tb, preprocessing_tb" \
      # "WHERE preprocessing_tb.news_id = news_tb.id"
# for a in range(0, len(dictOFTF_IDF)):
#     print(a)
    #     # mycursor.execute(sql, b)
    #     print(b)
    # mydb.commit()

# for data in dictOFTF_IDF:
#     columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in data.keys())
#     values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in data.values())
    # columns = data.keys()
    # values = data.values()
# sql = "INSERT INTO preprocessing_tb (id, news_id, preprocessing) VALUES(%s, %s, %s,)"
# mycursor.executemany(sql, dictOFTF_IDF.values())
# mydb.commit()
# mycursor.executemany(sql, dictOFTF_IDF)
# mydb.commit()
# from nltk.text import TextCollection
#
# mytexts = TextCollection(['universitas trunojoyo',
#                           'komisi yudisial universitas jalin kerjasama berantas mafia adil',
#                           'sar trunojoyo diklat bumi kemah wisata air terjun mojokerto bantu rektor',
#                           'roadshow speedy trunojoyo seminar internet sehat cangkruk komunitas workshop lomba band',
#                           'perintah kabupaten pamekasan henti program bantu beasiswa mahasiswa pamekasan universitas trunojoyo',
#                           '11 staf universitas trunojoyo magang fakultas teknik industri uii',
#                           'perpus universitas airlangga datang tamu 2 guru tinggi staf perpus universitas trunojoyo staf perpus universitas gunadarma'])
#
# print("NLTK tf_idf")
# print(mytexts.tf_idf('komisi','komisi yudisial universitas jalin kerjasama berantas mafia adil'))

# def test_tf(term, text):
#     newText = text.split(' ')
#     print(text.count(term))
#     print(len(newText))
#
# test_tf('universitas','universitas trunojoyo')