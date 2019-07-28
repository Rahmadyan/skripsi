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

# mycursor = mydb.cursor()
# mycursor.execute("SELECT content FROM news_tb")
# x = mycursor.fetchall()
# print(x)
# print(x)
# documents = list(itertools.chain(*x))
# print(documents)

# documents = [list(x) for x in b]
# print(documents)

#1. tokenizing stopword dan stemming
# dictOfWords = {}
#
# for index, sentence in enumerate(documents):
#     sentence = sentence.translate(str.maketrans('', '', string.punctuation))
#     # print(sentence)
#     tokenizedWords = word_tokenize(sentence)
#
#     listStopword = set(stopwords.words('indonesian'))
#
#     factory = StemmerFactory()
#     stemmer = factory.create_stemmer()
#
#     wordsFiltered = []
#     for t in tokenizedWords:
#         if t not in listStopword:
#             wordsFiltered.append(t)
#     wordsFiltered = [stemmer.stem(word) for word in wordsFiltered]
    # print(wordsFiltered)
    # dictOfWords[index] = [word for word in wordsFiltered]

# mycursor.execute("SELECT * FROM news_tb")
# a = mycursor.fetchall()
# print(a)

# b = []
# for i in range(0, len(a)):
#     for c in a[i]:
#         print(c)






def results(a):
    print("Ini adalah real id")
    print(a)

    mycursor = mydb.cursor()
    mycursor.execute("SELECT id FROM news_tb")
    all = mycursor.fetchall()
    list_id = list(itertools.chain(*all))
    list_id_real_id = []
    for i in enumerate(list_id):
        list_id_real_id.append(i)
    print("Ini adalah data real id dan id dokumen")
    print(list_id_real_id)

    hasil_deteksi = []
    for i in list_id_real_id:
        if i[1] == a:
            hasil_deteksi.append(i[0])
    hasil_deteksi = " ".join(str(x) for x in hasil_deteksi)
    print("Ini adalah hasil deteksi real_id ada pada artikel urutan berapa")
    print(hasil_deteksi)

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM result_tb WHERE id_query = %s", [hasil_deteksi])
    articles = mycursor.fetchall()
    print("mengambil data sesuai real id")
    print(articles)

    hasil = []
    for i in articles:
        for x in list_id_real_id:
            if i[2] == x[0]:
                hasil.append(x[1])
    print("mengambil real id sesuai dengan kesamaan/urutan terbesar")
    print(hasil)

    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM news_tb where id IN ({})".format(",".join([str(i) for i in hasil])))
    myresult = mycursor.fetchall()
    # print(myresult)
    results = sorted(myresult, key=lambda x: hasil.index(x[0]))

    mycursor.execute("TRUNCATE TABLE show_data")
    sql = "INSERT INTO show_data (id, url, title, author, time, crawl_time, imagelink, content) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    mycursor.executemany(sql, results)
    mydb.commit()

# print (results(453))
