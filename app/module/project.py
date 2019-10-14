from flask import render_template, request, redirect, url_for, jsonify
from app import app
import pandas as pd
import nltk
import string
import random
import time
import numpy as np
from nltk.corpus import stopwords  # nltk stopwords list bahasa inggris
from nltk.stem import PorterStemmer #nltk stemming
from sklearn.feature_extraction.text import TfidfVectorizer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory #sastrawi stemming
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory #sastrawi stopword
from sklearn.metrics.pairwise import cosine_similarity
stemmer = StemmerFactory().create_stemmer()
remover = StopWordRemoverFactory().create_stop_word_remover()
katabaku = pd.read_csv("app/data/vocab_katabaku.csv")
data_training = pd.read_csv("app/data/finalPrerapi.csv")
author = list(dict.fromkeys([str(x) for x in data_training["Author"]]))
lembaga = list(dict.fromkeys([str(x)for x in data_training["Lembaga"]]))
baku = [x for x in katabaku["kata_baku"]]
translator = str.maketrans('', '', string.punctuation)

def stemmerEN(text):
    porter = PorterStemmer()  # mendeklarasikan porter untuk memanggil kelas PorterStemmer
    # mendeklarasikan stop untuk proses filtering bahasa inggris
    stop = set(stopwords.words('english')) #stopword english
    # proses tekenizing
    text = [i for i in text.split() if i not in stop]
    text = ' '.join(text)
    # proses menerjemahkan dan stemming bahasa inggris
    preprocessed_text = text.translate(translator)
    text_stem = porter.stem(preprocessed_text)
    return text_stem

def preProcess(query):
    remove_number = ''.join(filter(lambda s: not str(s).isdigit(), query))
    lowercase = remove_number.lower()  # kecilkan semua teks
    stemEn = stemmerEN(lowercase)
    textStemmed = stemmer.stem(stemEn)  # stemming teks indonesia
    textClean = remover.remove(textStemmed)  # teks stopword remover
    # harus string dikasih koma atau tanda baca lain untuk mengatasi entering dan setiap kalimat
    convert_to_string = "".join(textClean)
    # split string yang sudah dikonversi kedalam token
    word = nltk.word_tokenize(convert_to_string)
    tampung = []
    for teks_conv in word:  # check one by one word (token)
        n = 0
        for j in katabaku["vocabulary"]:
            if teks_conv == j:
                teks_conv = baku[n]
            n = n+1
        # tampung setia string kedalam list (list string)
        tampung.append(teks_conv)
    pre_process = " ".join(tampung)  # join setiap list string dengan spasi
    return pre_process


def hexCodeColor():
    a = hex(random.randrange(0, 256))
    b = hex(random.randrange(0, 256))
    c = hex(random.randrange(0, 256))
    a = a[2:]
    b = b[2:]
    c = c[2:]
    if len(a) < 2:
        a = "0" + a
    if len(b) < 2:
        b = "2" + b
    if len(c) < 2:
        c = "4" + c
    z = a + b + c
    return "#" + z.upper()

def groupingAut(data_numpy):
    sortGroupCos = []
    for x in author:
        # group by author and sort by cosine >0
        selectRowNumpy = data_numpy[np.where((data_numpy[:,4] == str(x))*(data_numpy[:,6]>0))] # 4 is columns index for author and 6 is for cosine column (you can check this column in pandas view, berfore to_numpy)
        if(len(selectRowNumpy) != 0):
            sortGroupCos.append(selectRowNumpy)
    return sortGroupCos

#get json
def showJSON(save):
    scat = []
    param = len(save)
    color = [hexCodeColor() for x in range(len(lembaga))]
    for x in range(param):
        kordX = int(random.randint(0, param))  # random for plot only
        # grouping per lembaga
        for y in range(len(lembaga)):
            groupLem = pd.DataFrame(save[x][np.where(save[x][:,2] == str(lembaga[y]))]) # and convert to pandas
            if(len(groupLem)!=0): #dont process empty dataframe
                title = [i for i in groupLem[0]]
                inst = str(list(set(groupLem[1]))[0]) #instansi column number 1
                lemb = str(list(set(groupLem[2]))[0])
                aut = str(list(set(groupLem[4]))[0]) # aturhor column number 4
                nilai = groupLem[6].sum(axis=0)
                size = len(groupLem[6])
                kordY = float(round(nilai,2))
                isi = {
                    "color": color[y],
                    "label": lemb,
                    "author": aut,
                    "instansi":inst,
                    "y": kordY,
                    "x": kordX,
                    "size": size*10,
                    "count":size,
                    "title":title,
                }
                scat.append(isi)  # save node
    return scat

@app.route("/", methods=["GET", "POST"])
def Index():
    return render_template("index.html")

@app.route("/cosine", methods=["GET", "POST"])
def cosine():
    start_time = time.time()
    if request.method == "GET":
        msg = ["maaf halaman yang anda minta tidak dapat terpenuhi / tidak ada"]
        return render_template("page_errorhandling.html",message=msg), 512       
    elif request.method == "POST":
        query = str(request.form["query"]) #if use form
        if(len(query)>0):
            # query = str(request.json["query"]) #if use other like ajax json
            tesData = [preProcess(query)]
            trainData = [x for x in data_training["PreProcess"]]
            # join test and train data to count cosim
            newData = tesData+trainData
            # TF.IDF vector
            vector=TfidfVectorizer(smooth_idf=False, norm=None)
            # limit biar gak kelihatan banyak banget
            tfidf_matrix=vector.fit_transform(newData)
            # cosine similiarity
            cosim=cosine_similarity(tfidf_matrix, tfidf_matrix[0:1])
            # save to dataframe
            dfCosime = pd.DataFrame(cosim[1:],columns=["Cosine"]) # get cosim that not include self (1)
            dfFinalResult = pd.concat([data_training,dfCosime],axis=1).to_numpy() # and concat add to train dtaframe and convert to_numpy for or to_dict for better performance
            # sort cosime and tsr for group by author in node
            print("--- %s seconds ---" % (time.time() - start_time))
            hasilgroup = groupingAut(dfFinalResult)
            print("--- %s seconds ---" % (time.time() - start_time))
            # decrypt json
            isi_scatterCos = [{
                "name": sc["label"],
                "type": "scatter",
                "data": [[sc["x"], sc["y"], sc["count"], sc["title"], sc["instansi"], sc["author"]]],
                "symbolSize": sc["size"],
                "label": {
                    "show":"true",
                    "position":"top",
                    "formatter": "{b}{@[5]}"
                },
                "itemStyle": {
                    "opacity": 0.4,
                    "normal": {"color": sc["color"]}
                }
            } for sc in showJSON(hasilgroup)]  # cosine
            print("--- %s seconds ---" % (time.time() - start_time)) #execution time, please enable to track how long your code while execute
            return jsonify({"error":False,"scatter":isi_scatterCos, "lgd":lembaga, "type":"Cosine"})
        else:
            return jsonify({"error":True,"scatter":[],"type":[]})
    else:
        msg = ["maaf request anda tidak dapat kami penuhi"]
        return render_template("page_errorhandling.html", message=msg), 302

@app.route("/index", methods=["GET", "POST"])
def Indeks():
    return redirect(url_for("Index"))

@app.route("/makedb", methods=["GET", "POST"])
def makedb():
    for x in range(len(daftar_dosen)):
        ds = Dosen(judul=daftar_dosen[x][0], nama_dosen=daftar_dosen[x][1], picture=daftar_dosen[x][2])
        ds.save()
    

@app.errorhandler(404)
def page_not_found(error):
    msg = ["maaf halaman yang anda minta tidak dapat terpenuhi / tidak ada"]
    return render_template("page_errorhandling.html",message=msg), 404
