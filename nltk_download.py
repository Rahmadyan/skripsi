from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
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
myresult = mycursor.fetchall()
for a in myresult:
    for b in a:
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        output = stemmer.stem(b)
        output = output.translate(str.maketrans('', '', string.punctuation)).lower()
    tokens = word_tokenize(output)

    listStopword = set(stopwords.words('indonesian'))

    #stem
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    wordsFiltered = []
    for t in tokens:
        if t not in listStopword:
            wordsFiltered.append(t)
    print(wordsFiltered)
# sql = "INSERT INTO preprocessing (content) VALUES (%s)"
# mycursor.execute(sql, output)
#
# mydb.commit()
#
# print(mycursor.rowcount, "record inserted.")


