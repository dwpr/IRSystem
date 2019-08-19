from flask import render_template, request, redirect, url_for, jsonify
from app import app
import pandas as pd
import nltk
import string
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import fuzz
stemmer = StemmerFactory().create_stemmer()
remover = StopWordRemoverFactory().create_stop_word_remover()
katabaku = pd.read_csv("app/data/vocab_katabaku.csv")
data_training = pd.read_csv("app/data/finalPrerapi.csv")
baku = [x for x in katabaku["kata_baku"]]


def preProcess(query):
    remove_number = ''.join(filter(lambda s: not str(s).isdigit(), query))
    lowercase = remove_number.lower()  # kecilkan semua teks
    textStemmed = stemmer.stem(lowercase)  # stemming teks
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
        b = "0" + b
    if len(c) < 2:
        c = "0" + c
    z = a + b + c
    return "#" + z.upper()

#get json
def showJSON(save,choice):
    scat = []
    param = len(save)
    pilih = choice
    for x in range(param):
        kordX = int(random.randint(0, param))  # random for plot only
        aut = str(list(dict.fromkeys(save[x]["Author"]))[0])
        if(pilih=="fuzzy"):
            nilai = save[x]["TSR"].sum(axis=0)
            size = len(save[x]["TSR"])*10
            kordY = float(round(nilai))
        elif(pilih=="cosine"):
            nilai = save[x]["Cosine"].sum(axis=0)
            size = len(save[x]["Cosine"])*10
            kordY = float(round(nilai,2))
        else:
            return "maaf module lain belum ada"
        isi = {
            "color": hexCodeColor(),
            "label": aut,
            "y": kordY,
            "x": kordX,
            # biar kelihatan kali 10 atau terserah
            # "size": round(nilai_cosim, 2)*100
            # "size": random.uniform(0, round(nilai_cosim)*100)
            "size": size
        }
        scat.append(isi)  # save node
    return scat

@app.route("/", methods=["GET", "POST"])
def Index():
    return render_template("index.html")


@app.route("/olah", methods=["GET", "POST"])
def olah():
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
            dfFinalResult = pd.concat([data_training,dfCosime],axis=1) # and concat add to train dtaframe (limit to 50 cause many)
            # for fuzzy method
            saveFuzzy = []
            queryFuzzy = str(tesData)
            for j in range(len(trainData)):
                # karena dicocokkan dengan yang sudah ke pre-proces, sebenarnya tidak dipre-process tidak apa-apa cuma biar lebih clean saja :D
                tokenSetRatio = fuzz.token_set_ratio(queryFuzzy, str(trainData[j]))
                saveFuzzy.append([str(data_training["Judul"][j]), str(data_training["Author"][j]), tokenSetRatio])
            dfTSR = pd.DataFrame(saveFuzzy, columns=["Judul", "Author", "TSR"])  # Token Set Ratio
            # sort cosime and tsr for group by author in node
            author = list(dict.fromkeys([str(x) for x in data_training["Author"]]))
            sortGroupCos = []
            sortGroupFuzz = []
            for x in range(len(author)):
                groupBy = dfFinalResult.loc[dfFinalResult["Author"].isin([str(author[x])])]
                groupBy2 = dfTSR.loc[dfTSR["Author"].isin([str(author[x])])]
                # select only have cosine value range 0-1
                sortBy = groupBy.loc[(groupBy["Cosine"] > 0) & (groupBy["Cosine"] < 1)] #all cosine except 0, maybe this can
                sortBy2 = groupBy2.loc[groupBy2["TSR"]>40] #value want to use similiar match string grater tahn 50%
                if(len(sortBy) != 0):  # if sortBy exist, greater than 0
                    sortGroupCos.append(sortBy.reset_index(drop=True))  # save
                if(len(sortBy2) != 0):
                    sortGroupFuzz.append(sortBy2.reset_index(drop=True))
            # decrypt json
            isi_scatterCos = [{
                "name": sc["label"],
                "type": "scatter",
                "data": [[sc["x"], sc["y"]]],
                "symbolSize": sc["size"],
                "label": {
                    "show":"true",
                    "position":"top",
                    "formatter":"{a}"
                },
                "itemStyle": {
                    "opacity": 0.4,
                    "normal": {"color": sc["color"]}
                }
            } for sc in showJSON(sortGroupCos,"cosine")] # 0 is cosine

            isi_scatterFuzz = [{
                "name": sc["label"],
                "type": "scatter",
                "data": [[sc["x"],sc["y"]]],
                "symbolSize": sc["size"],
                "label": {
                    "show": "true",
                    "position": "top",
                    "formatter": "{a}"
                },
                "itemStyle": {
                    "opacity": 0.4,
                    "normal": {"color": sc["color"]}
                }
            } for sc in showJSON(sortGroupFuzz,"fuzzy")]  # 1 or grater is tsr
            print(len(isi_scatterCos))
            print(len(isi_scatterFuzz))
            return jsonify({"error":False,"scatterCos":isi_scatterCos,"scatterFuzz":isi_scatterFuzz})
        else:
            return jsonify({"error":True,"scatterCos":[],"scatterFuzz":[]})
    else:
        msg = ["maaf request anda tidak dapat kami penuhi"]
        return render_template("page_errorhandling.html", message=msg), 302
@app.route("/index", methods=["GET", "POST"])
def Indeks():
    return redirect(url_for("Index"))

@app.errorhandler(404)
def page_not_found(error):
    msg = ["maaf halaman yang anda minta tidak dapat terpenuhi / tidak ada"]
    return render_template("page_errorhandling.html",message=msg), 404
