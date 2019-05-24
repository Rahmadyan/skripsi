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
documents = list(itertools.chain(*x))
# print(documents)
def inverse_document_frequencies(tokenized_documents):
    idf_values = {}
    all_tokens_set = set([item for sublist in tokenized_documents for item in sublist])
    for tkn in all_tokens_set:
        contains_token = map(lambda doc: tkn in doc, tokenized_documents)
        idf_values[tkn] = math.log10(len(tokenized_documents)/(sum(contains_token)))
    return idf_values

tokenize = lambda doc: doc.lower().split(" ")
tokenized_documents = [tokenize(d) for d in documents]
print(tokenized_documents)

idf = inverse_document_frequencies(tokenized_documents)

# print(idf)