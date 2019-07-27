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

import time, datetime

t = "Sunday, 18 hanuary 2019 - 16:38"
t = time.strptime(' '.join(t.rsplit(' ',5)[0:4]), "%A, %B %d, %Y")
print(t)
a=datetime.datetime(*t[:6])
print(a)
