# def Articles():
#     articles = [
#         {
#             'id':1,
#             'title': 'Article One',
#             'body':'auwhdiyagwiydhdwhiahwdhawudhawihd ihawih uiahwidh ihauihawhdu huiawhdih uah ',
#             'author':'oawkdo',
#             'creade_date':'09-89-0'
#
#         },
#         {
#             'id': 2,
#             'title': 'Article Twu',
#             'body': 'auwhdiyagwiydhdwhiahwdhawudhawihd ihawih uiahwidh ihauihawhdu huiawhdih uah ',
#             'author': 'oawkdo',
#             'creade_date': '09-89-0'
#
#         },
#         {
#             'id': 3,
#             'title': 'Article Three',
#             'body': 'auwhdiyagwiydhdwhiahwdhawudhawihd ihawih uiahwidh ihauihawhdu huiawhdih uah ',
#             'author': 'oawkdo',
#             'creade_date': '09-89-0'
#
#         }
#     ]


#     return articles



import mysql.connector
from datetime import datetime

mydb = mysql.connector.connect(
    host="localhost",
    user= "root",
    passwd="",
    database="news"
)


mycursor = mydb.cursor()
mycursor.execute("select * from news_tb")
time = mycursor.fetchall()

# print(time)


# time.sort(key = lambda date: datetime.strptime(date, "%A %d %B %Y %H:%M"))
# print(time)


a = [{'checksum': 'e58baa427226bbdd1c03ab051250b374', 'path':'full/a4a7125419cc25d49f22971818810d18b49a0383.jpg','url': 'https://cdn.sindonews.net/dyn/620/content/2019/07/28/12/1424553/gerindra-bergabung-soliditas-koalisi-jokowi-ma-ruf-diyakini-terganggu-6Z0.jpg'}]
print(a[0]['path'])