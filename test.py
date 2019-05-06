#biar tidak bingung
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user= "root",
    passwd="",
    database="news"
)

mycursor = mydb.cursor()
mycursor.execute("SELECT title FROM news_tb")
documents = mycursor.fetchall()
for x in documents:
    print(x)

# documents = ('the the universe has very many stars'),
#             ('the galaxy contains many stars'),
#             ('the cold breeze of winter made it very cold outside')

#TERM / KATA = 'the', 'universe' dll
#SENTENCE / KALIMAT = 'the the universe has very many stars'

allDocuments = ''
for sentence in documents:
    for x in sentence:
        allDocuments += x + ' '
allDocumentsTokenized = allDocuments.split(' ')
print(allDocumentsTokenized)

# dictOfWords = {}
#
# for index, sentence in enumerate(documents):
#     tokenizedWords = sentence.split(' ')
#     dictOfWords[index] = [(word,tokenizedWords.count(word)) for word in tokenizedWords]
#
# print(dictOfWords)

# mylist = list(documents)
# print(mylist)
