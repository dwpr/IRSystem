from flask import request, jsonify, request
from app import app
from .models import *
from .consts import HttpStatus

@app.route('/api', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print("<Request: {}>".format(request.json))
    return "<h4>Rest API BRO</h4>"

@app.route('/api/gettable/<string:param>')
def gettable(param):
    id_olah = Olah.findBy(param).idd
    construct = {'error': [], 'success': True,'nilai': Relasi.relation(id_olah, "nonall")}
    response = jsonify(construct)
    response.status_code = HttpStatus.OK
    return response

# for tsting only
@app.route('/api/angket', methods=['GET', 'POST'])
def angket():
	# get
    if request.method == 'GET':
        parameter = request.args.get('get', '')
        if parameter=="all":
            construct = {'error': [], 'success': True,'nilai': Dosen.getAll()}
        elif parameter == "all2":
            construct = {'error': [], 'success': True, 'nilai': Matkul.getAll()}
        elif parameter == "all3":
            construct = {'error': [], 'success': True, 'nilai': Olah.getAll()}
        elif parameter == "all4":
            construct = {'error': [], 'success': True, 'nilai': Angket.getAll()}
        elif parameter == "all5":
            construct = {'error': [], 'success': True, 'nilai': Nilai.getAll()}
        elif parameter == "all6":
            construct = {'error': [], 'success': True, 'nilai': Sentimen.getAll()}
        elif parameter == "all7":
            construct = {'error': [], 'success': True,'nilai': Komentar.getAll()}
        elif parameter == "all8":
            construct = {'error': [], 'success': True,'nilai': Relasi.relation(1,"nonall")}
        else:
            construct = {'error': [], 'success': True, 'nilai': Angket.getAll()}
        response = jsonify(construct)
        response.status_code = HttpStatus.OK
	# saving
    elif request.method == 'POST':
        kode_pengampu = None if request.json['body']['kode_pengampu'] is "" else request.json['body']["kode_pengampu"]
        kode_matkul = None if request.json['body']["kode_matkul"] is "" else request.json['body']["kode_matkul"]
        nilai_angket = None if request.json['body']["nilai_angket"] is "" else request.json['body']["nilai_angket"]
        construct = {}
        try:
            an = Angket(kode_pengampu=kode_pengampu, kode_matkul=kode_matkul, nilai_angket=nilai_angket)
            an.save()
            construct['success'] = True
            construct['message'] = 'Data saved'
            response = jsonify(construct)
            response.status_code = HttpStatus.CREATED
            print("<Nama: {}, Nim: {}>".format(name, nim))
        except Exception as e:
            construct['success'] = False
            construct['error'] = str(e)
            response = jsonify(construct)
            response.status_code = HttpStatus.BAD_REQUEST
    return response
