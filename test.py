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

# mycursor = mydb.cursor(buffered=True)
mycursor = mydb.cursor()
mycursor.execute("SELECT content FROM news_tb")
myresult = mycursor.fetchall()
# for a in myresult:
#      print(a)

for x in myresult:
     for y in x:
          kalimat = y.translate(str.maketrans('', '', string.punctuation))

          tokens = word_tokenize(kalimat)
          listStopword = set(stopwords.words('indonesian'))

          factory = StemmerFactory()
          stemmer = factory.create_stemmer()

          wordsFilterd = []
          for t in tokens:
               if t not in listStopword:
                    wordsFilterd.append(t)
          wordsFilterd = [stemmer.stem(word) for word in wordsFilterd]
          wordsFilterd = tuple(wordsFilterd)
     # print(wordsFilterd)
     # break
     # wordsFilterd = ' '.join(wordsFilterd)
     print(wordsFilterd)
     sql = "INSERT INTO `preprocessing_tb` (`id`, `preprocessing`, `news_id`) VALUES (NULL, 'kokojjij', '252');"