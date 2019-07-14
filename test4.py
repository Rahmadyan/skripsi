import math
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import string
import itertools

document_0 = "Sandiaga Uno dipastikan akan memberikan bantuan hukum kepada seorang saksi ahlinya"
document_1 = "Bantuan hukum itu diberikan jika Beti dipidanakan Tim Hukum Joko Widodo"
document_2 = "dengan tuduhan memberikan keterangan palsu dalam sidang sengketa hasil Pilihan presiden 2019 di Mahkamah Konstitusi"
document_3 = "Ahli kedua yang dihadirkan Tim Hukum Jokowi - Ma'ruf, Heru Widodo berpendapat soal tafsir diskualifikasi dalam putusan Mahkamah"
document_4 = "pemilihan presiden maupun pemilu legislatif selama ini belum ada dalam putusan diskualifikasi oleh Mahkamah Konstitusi"
# document_5 = "11 staf universitas trunojoyo magang fakultas teknik industri uii"
# document_6 = "perpus universitas airlangga datang tamu 2 guru tinggi staf perpus universitas trunojoyo staf perpus universitas gunadarma"
documents = [document_0, document_1, document_2, document_3, document_4]
# print(documents)
#1. tokenizing stopword dan stemming
dictOfWords = {}

for index, sentence in enumerate(documents):
    sentence = sentence.translate(str.maketrans('', '', string.punctuation))
    # print(sentence)
    tokenizedWords = word_tokenize(sentence)

    listStopword = set(stopwords.words('indonesian'))

    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    wordsFiltered = []
    for t in tokenizedWords:
        if t not in listStopword:
            wordsFiltered.append(t)
    wordsFiltered = [stemmer.stem(word) for word in wordsFiltered]
    # print(wordsFiltered)
    dictOfWords[index] = [word for word in wordsFiltered]
# print(dictOfWords)
termFrequency = []
for i in range(0, len(documents)):
    termFrequency.append([])
    for wordFreq in dictOfWords[i]:
        # if wordFreq not in termFrequency[i]:
        termFrequency[i].append(wordFreq)

print(termFrequency)

# all_tokens_set = set([item for sublist in termFrequency for item in sublist])
# print(all_tokens_set)
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
    # print(all_tokens_set)
    for tkn in all_tokens_set:
        contains_token = map(lambda doc: tkn in doc, tokenized_documents)
        idf_values[tkn] = math.log10(len(tokenized_documents)/(sum(contains_token)))
    return idf_values

def tfidf(documents):
    # tokenized_documents = [tokenize(d) for d in documents]
    # print(documents)
    idf = inverse_document_frequencies(documents)
    # print(idf.keys())
    tfidf_documents = []
    for document in documents:
        doc_tfidf = []
        for term in idf.keys():
            tf = term_frequency(term, document)
            doc_tfidf.append(tf * idf[term])
        tfidf_documents.append(doc_tfidf)
    # print(tfidf_documents)
    return tfidf_documents

def cosine_similarity(vector1, vector2):
    dot_product = sum(p*q for p,q in zip(vector1, vector2))
    magnitude = math.sqrt(sum([val**2 for val in vector1])) * math.sqrt(sum([val**2 for val in vector2]))
    if not magnitude:
        return 0
    return dot_product/magnitude

tfidf_representation = tfidf(termFrequency)
our_tfidf_comparisons = []
for count_0, doc_0 in enumerate(tfidf_representation):
    for count_1, doc_1 in enumerate(tfidf_representation):
        our_tfidf_comparisons.append((cosine_similarity(doc_0, doc_1), count_0, count_1))

sorted_similar_movies = sorted(our_tfidf_comparisons,key=lambda x:x[0],reverse=True)

print(our_tfidf_comparisons)