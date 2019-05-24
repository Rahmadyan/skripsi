import math
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import string
import itertools
import mysql.connector
tokenize = lambda doc: doc.lower().split(" ")

document_0 = "universitas trunojoyo"
document_1 = "komisi yudisial universitas jalin kerjasama berantas mafia adil"
document_2 = "sar trunojoyo diklat bumi kemah wisata air terjun mojokerto bantu rektor"
document_3 = "roadshow speedy trunojoyo seminar internet sehat cangkruk komunitas workshop lomba band"
document_4 = "perintah kabupaten pamekasan henti program bantu beasiswa mahasiswa pamekasan universitas trunojoyo"
document_5 = "11 staf universitas trunojoyo magang fakultas teknik industri uii"
document_6 = "perpus universitas airlangga datang tamu 2 guru tinggi staf perpus trunojoyo staf perpus gunadarma"
document_7 = ""
all_documents = [document_0, document_1, document_2, document_3, document_4, document_5, document_6]

print(all_documents)

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
def inverse_document_frequencies(tokenized_documents):
    idf_values = {}
    all_tokens_set = set([item for sublist in tokenized_documents for item in sublist])
    for tkn in all_tokens_set:
        contains_token = map(lambda doc: tkn in doc, tokenized_documents)
        idf_values[tkn] = math.log10(len(tokenized_documents)/(sum(contains_token)))
    return idf_values

def tfidf(documents):
    tokenized_documents = [tokenize(d) for d in documents]
    idf = inverse_document_frequencies(tokenized_documents)
    tfidf_documents = []
    for document in tokenized_documents:
        doc_tfidf = []
        for term in idf.keys():
            tf = term_frequency(term, document)
            doc_tfidf.append(tf * idf[term])
        tfidf_documents.append(doc_tfidf)
    return tfidf_documents

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
    # print(doc_0)
    for count_1, doc_1 in enumerate(tfidf_representation):
        our_tfidf_comparisons.append((cosine_similarity(doc_0, doc_1), count_0, count_1))

# for x in zip(sorted(our_tfidf_comparisons, reverse = True), sorted(skl_tfidf_comparisons, reverse = True)):
#     print (x)
# print(our_tfidf_comparisons)
print(our_tfidf_comparisons)