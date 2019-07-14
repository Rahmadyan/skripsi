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
tokenize = lambda doc: doc.lower().split(" ")

# document_0 = "universitas trunojoyo"
# document_1 = "komisi yudisial universitas jalin kerjasama berantas mafia adil"
# document_2 = "sar trunojoyo ada diklat bumi kemah wisata air terjun mojokerto acara buka langsung bantu rektor"
# document_3 = "roadshow speedy trunojoyo isi acara seminar internet sehat cangkrukan komunitas workshop lomba band"
# document_4 = "perintah kabupaten pamekasan henti program bantu pamekasan beasiswa mahasiswa kuliah universitas trunojoyo"
# document_5 = "banyak 11 orang staf universitas trunojoyo magang fakultas teknik industri uii"
# document_6 = "perpus universitas airlangga datang tamu 2 guru tinggi staf perpus universitas trunojoyo staf perpus universitas gunadarma"
# document_7 = "kalimat double test"
document_0 = "universitas trunojoyo"
document_1 = "komisi yudisial universitas jalin kerjasama berantas mafia adil"
document_2 = "sar trunojoyo diklat bumi kemah wisata air terjun mojokerto bantu rektor"
document_3 = "roadshow speedy trunojoyo seminar internet sehat cangkruk komunitas workshop lomba band"
document_4 = "perintah kabupaten pamekasan henti program bantu beasiswa mahasiswa pamekasan universitas trunojoyo"
document_5 = "11 staf universitas trunojoyo magang fakultas teknik industri uii"
document_6 = "perpus universitas airlangga datang tamu 2 guru tinggi staf perpus universitas trunojoyo staf perpus universitas gunadarma"
all_documents = [document_0, document_1, document_2, document_3, document_4, document_5, document_6]

# print(all_documents)

#TF hitung kemunculan kata (tf murni) dalam kalimat
def term_frequency(term, tokenized_document):
    return tokenized_document.count(term)

#tf logaritmik
def sublinear_term_frequency(term, tokenized_document):
    count = tokenized_document.count(term)
    if count == 0:
        return 0
    return 1 + math.log10(count)

#rumus buat TF normalisasi
def augmented_term_frequency(term, tokenized_document):
    max_count = max([term_frequency(t, tokenized_document) for t in tokenized_document])
    return (0.5 + ((0.5 * term_frequency(term, tokenized_document))/max_count))

# IDF RUMUS = log(n/df) n= jumlah dokumen df = jumlah dokumen dimana istilah/kata itu muncul
#masih BUG
def inverse_document_frequencies(tokenized_documents):
    idf_values = {}
    all_tokens_set = set([item for sublist in tokenized_documents for item in sublist])
    # print(all_tokens_set)
    for tkn in all_tokens_set:
        contains_token = map(lambda doc: tkn in doc, tokenized_documents)
        idf_values[tkn] = math.log10(len(tokenized_documents)/(sum(contains_token)))
    # print(idf_values)
    return idf_values

def tfidf(documents):
    tokenized_documents = [tokenize(d) for d in documents]
    print(tokenized_documents)
    idf = inverse_document_frequencies(tokenized_documents)
    print(idf)
    tfidf_documents = []
    for document in tokenized_documents:
        doc_tfidf = []
        for term in idf.keys():
            tf = term_frequency(term, document)
            doc_tfidf.append(tf * idf[term])
        tfidf_documents.append(doc_tfidf)
    return tfidf_documents

from sklearn.feature_extraction.text import TfidfVectorizer

sklearn_tfidf = TfidfVectorizer(norm='l2',min_df=0, use_idf=True, smooth_idf=False, sublinear_tf=True, tokenizer=tokenize)
sklearn_representation = sklearn_tfidf.fit_transform(all_documents)

def cosine_similarity(vector1, vector2):
    dot_product = sum(p*q for p,q in zip(vector1, vector2))
    magnitude = math.sqrt(sum([val**2 for val in vector1])) * math.sqrt(sum([val**2 for val in vector2]))
    if not magnitude:
        return 0
    return dot_product/magnitude

# def get_title_from_index(index):
#     return df[df.index == index]["title"].values[0]
# def get_index_from_title(title):
#     return df[df.title == title]["index"].values[0]

tfidf_representation = tfidf(all_documents)
our_tfidf_comparisons = []
for count_0, doc_0 in enumerate(tfidf_representation):
    for count_1, doc_1 in enumerate(tfidf_representation):
        our_tfidf_comparisons.append((cosine_similarity(doc_0, doc_1), count_0, count_1))
print(our_tfidf_comparisons)

skl_tfidf_comparisons = []
for count_0, doc_0 in enumerate(sklearn_representation.toarray()):
    for count_1, doc_1 in enumerate(sklearn_representation.toarray()):
        skl_tfidf_comparisons.append((cosine_similarity(doc_0, doc_1), count_0, count_1))

# for x in zip(sorted(our_tfidf_comparisons, reverse = True), sorted(skl_tfidf_comparisons, reverse = True)):
    # print (x)
# for x in zip(our_tfidf_comparisons,skl_tfidf_comparisons):
    # print (x)

# print(tfidf_representation)
# print(our_tfidf_comparisons)
# print(our_tfidf_comparisons)
# def jumlah_query():
#     mycursor = mydb.cursor()
#     mycursor.execute("SELECT COUNT(*) FROM news_tb")
#     a = mycursor.fetchone()[0]
#     return a