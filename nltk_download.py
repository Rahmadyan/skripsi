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
# for x in myresult:
#     print(x)

for a in myresult:
    for b in a:
        b = b.translate(str.maketrans('', '', string.punctuation))

    tokens = word_tokenize(b)

    listStopword = set(stopwords.words('indonesian'))

    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    wordsFiltered = []
    for t in tokens:
        if t not in listStopword:
            wordsFiltered.append(t)
    # for w in wordsFiltered:
    #     # katadasar = stemmer.stem(kalimat)
    #     []
    wordsFiltered = [stemmer.stem(word) for word in wordsFiltered]
    print(wordsFiltered)



