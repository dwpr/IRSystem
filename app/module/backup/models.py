from app import db
from sqlalchemy import text

class Angket(db.Model):
    __tablename__ = 'Angket' #Must be defined the table 

    idd = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    id_dosen = db.Column(db.Integer, db.ForeignKey("Dosen.idd"), nullable=False)
    id_matkul = db.Column(db.Integer, db.ForeignKey("Matkul.idd"), nullable=False)
    nilai_angket = db.Column(db.Float, nullable=False)
    id_olah = db.Column(db.Integer, db.ForeignKey("Olah.idd"), nullable=False)

    def __init__(self, id_dosen, id_matkul, nilai_angket, id_olah):
        self.id_dosen = Dosen.findBy(id_dosen).idd
        self.id_matkul = Matkul.findBy(id_matkul).idd
        self.nilai_angket = nilai_angket
        self.id_olah = Olah.findBy(id_olah).idd

    def __repr__(self):
        return "<id_matkul: {}, id_dosen: {}, nilai_angket: {}, id_olah:{}>".format(self.id_matkul, self.id_dosen, self.nilai_angket, self.id_olah)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def getAll():
        var_angket = Angket.query.all()
        result = []
        for value in var_angket:
            obj = {
                'idd': value.idd,
                'id_dosen': value.id_dosen,
                # 'id_dosen': Dosen.getByidd(value.id_dosen), #jika ingnin tampil idnya saja seperti diatas saja, kalau mau detail pakai cara ini
                'id_matkul': value.id_matkul,
                # 'id_matkul': Matkul.getByidd(value.id_matkul), #jika ingnin tampil idnya saja seperti diatas saja, kalau mau detail pakai cara ini
                'nilai_angket': value.nilai_angket,
                'id_olah': value.id_olah,
                # 'id_olah': Olah.getByidd(value.id_olah), #jika ingnin tampil idnya saja seperti diatas saja, kalau mau detail pakai cara ini
            }
            result.append(obj)
        return result

class Nilai(db.Model):
    __tablename__ = 'Nilai' #Must be defined the table 

    idd = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    id_dosen = db.Column(db.Integer, db.ForeignKey("Dosen.idd"), nullable=False)
    id_matkul = db.Column(db.Integer, db.ForeignKey("Matkul.idd"), nullable=False)
    nilai_AB = db.Column(db.Float, nullable=False)
    nilai_CDE = db.Column(db.Float, nullable=False)
    id_olah = db.Column(db.Integer, db.ForeignKey("Olah.idd"), nullable=False)

    def __init__(self, id_matkul, id_dosen, nilai_AB, nilai_CDE, id_olah):
        self.id_matkul = Matkul.findBy(id_matkul).idd
        self.id_dosen = Dosen.findBy(id_dosen).idd
        self.nilai_AB = nilai_AB
        self.nilai_CDE = nilai_CDE
        self.id_olah = Olah.findBy(id_olah).idd

    def __repr__(self):
        return "<id_matkul: {}, id_dosen: {}, nilai_AB: {}, nilai_CDE: {}, id_olah:{}>".format(self.id_matkul, self.id_dosen, self.nilai_AB, self.nilai_CDE, self.id_olah)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def getAll():
        var_nilai = Nilai.query.all()
        result = []
        for value in var_nilai:
            obj = {
                'idd': value.idd,
                'id_dosen': value.id_dosen,
                'id_matkul': value.id_matkul,
                'nilai_AB': value.nilai_AB,
                'nilai_CDE': value.nilai_CDE,
                'id_olah': value.id_olah,
            }
            result.append(obj)
        return result

class Sentimen(db.Model):
    __tablename__ = 'Sentimen' #Must be defined the table 

    idd = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)  

    id_dosen = db.Column(db.Integer, db.ForeignKey("Dosen.idd"), nullable=False)
    id_matkul = db.Column(db.Integer, db.ForeignKey("Matkul.idd"), nullable=False)
    pos = db.Column(db.Float, nullable=False)
    net = db.Column(db.Float, nullable=False)
    neg = db.Column(db.Float, nullable=False)
    id_olah = db.Column(db.Integer, db.ForeignKey("Olah.idd"), nullable=False)

    def __init__(self, id_matkul, id_dosen, pos, net, neg, id_olah):
        self.id_matkul = Matkul.findBy(id_matkul).idd
        self.id_dosen = Dosen.findBy(id_dosen).idd
        self.pos = pos
        self.net = net
        self.neg = neg
        self.id_olah = Olah.findBy(id_olah).idd

    def __repr__(self):
        return "<id_matkul: {}, id_dosen: {}, pos: {}, net: {}, neg: {}, id_olah: {}>".format(self.id_matkul, self.id_dosen, self.pos, self.net, self.neg, self.id_olah)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def getAll():
        var_sentimen = Sentimen.query.all()
        result = []
        for value in var_sentimen:
            obj = {
                'idd': value.idd,
                'id_dosen': value.id_dosen,
                'id_matkul': value.id_matkul,
                'pos': value.pos,
                'net': value.net,
                'neg': value.neg,
                'id_olah': value.id_olah,
            }
            result.append(obj)
        return result

class Komentar(db.Model):
    __tablename__ = 'Komentar'  # Must be defined the table

    idd = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    komentar = db.Column(db.String, nullable=False)
    id_olah = db.Column(db.Integer, db.ForeignKey("Olah.idd"), nullable=False)

    def __init__(self, komentar, id_olah):
        self.komentar = komentar
        self.id_olah = Olah.findBy(id_olah).idd

    def __repr__(self):
        return "<komentar: {}, id_olah:{}>".format(self.komentar, self.id_olah)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def getAll():
        var_komentar = Komentar.query.all()
        result = []
        for value in var_komentar:
            obj = {
                'idd': value.idd,
                'komentar': value.komentar,
                'id_olah': value.id_olah,
            }
            result.append(obj)
        return result

    def getOn(param):
        komentar = db.session.query(Komentar).filter(Komentar.id_olah==param).all()
        result = []
        for value in komentar:
            obj = {
                'idd': value.idd,
                'komentar': value.komentar,
                'id_olah': value.id_olah,
            }
            result.append(obj)
        return result

class Olah(db.Model):
    __tablename__ = 'Olah'  # Must be defined the table

    idd = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    tahun_ajar = db.Column(db.String, nullable=False)
    olah_nilai = db.relationship('Nilai', backref='Olah', lazy='dynamic')
    olah_sentimen = db.relationship('Sentimen', backref='Olah', lazy='dynamic')
    olah_angket = db.relationship('Angket', backref='Olah', lazy='dynamic')
    olah_komentar = db.relationship('Komentar', backref='Olah', lazy='dynamic')

    def __init__(self, tahun_ajar):
        self.tahun_ajar = tahun_ajar

    def __repr__(self):
        return "tahun_ajar:{}>".format(self.tahun_ajar)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def getAll():
        var_olah = Olah.query.all()
        result = []
        for value in var_olah:
            obj = {
                'idd': value.idd,
                'tahun_ajar': value.tahun_ajar,
            }
            result.append(obj)
        return result

    @staticmethod
    def getByidd(idd):
        olah = Olah.findByidd(idd)
        result = {
            "idd": olah.idd,
            "tahun_ajar": olah.tahun_ajar,
        }
        return result

    @staticmethod
    def findByidd(idd):
        return Olah.query.filter_by(idd=idd).first()

    @staticmethod
    def findBy(tahun_ajar):
        return Olah.query.filter_by(tahun_ajar=tahun_ajar).first()

class Dosen(db.Model):
    __tablename__ = 'Dosen'  # Must be defined the table

    idd = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    kode_dosen = db.Column(db.String, nullable=False)
    nama_dosen = db.Column(db.String, nullable=False)
    picture = db.Column(db.String, nullable=False)
    dosen_nilai = db.relationship('Nilai', backref='Dosen', lazy='dynamic')
    dosen_sentimen = db.relationship('Sentimen', backref='Dosen', lazy='dynamic')
    dosen_angket = db.relationship('Angket', backref='Dosen', lazy='dynamic')

    def __init__(self, kode_dosen, nama_dosen, picture):
        self.kode_dosen = kode_dosen
        self.nama_dosen = nama_dosen
        self.picture = picture

    def __repr__(self):
        return "<kode_dosen: {}, nama_dosen:{}, picture:{}>".format(self.kode_dosen, self.nama_dosen, self.picture)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def getAll():
        var_dosen = Dosen.query.all()
        result = []
        for value in var_dosen:
            obj = {
                'idd': value.idd,
                'kode_dosen': value.kode_dosen,
                'nama_dosen': value.nama_dosen,
                'picture': value.picture,
            }
            result.append(obj)
        return result

    @staticmethod
    def getByidd(idd):
        dosen = Dosen.findByidd(idd)
        result = {
            "idd": dosen.idd,
            "kode_dosen": dosen.kode_dosen,
            "nama_dosen": dosen.nama_dosen,
            "picture": dosen.picture
        }
        return result
        
    @staticmethod
    def findByidd(idd):
        return Dosen.query.filter_by(idd=idd).first()

    @staticmethod
    def findBy(kode_dosen):
        return Dosen.query.filter_by(kode_dosen=kode_dosen).first()

class Matkul(db.Model):
    __tablename__ = 'Matkul'  # Must be defined the table

    idd = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    kode_matkul = db.Column(db.String, nullable=False)
    nama_matkul = db.Column(db.String, nullable=True)
    matkul_nilai = db.relationship('Nilai', backref='Matkul', lazy='dynamic')
    matkul_sentimen = db.relationship('Sentimen', backref='Matkul', lazy='dynamic')
    matkul_angket = db.relationship('Angket', backref='Matkul', lazy='dynamic')

    def __init__(self, kode_matkul, nama_matkul):
        self.kode_matkul = kode_matkul
        self.nama_matkul = nama_matkul

    def __repr__(self):
        return "kode_matkul:{}, nama_matkul:{}>".format(self.kode_matkul, self.nama_matkul)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def getAll():
        var_matkul = Matkul.query.all()
        result = []
        for value in var_matkul:
            obj = {
                'idd': value.idd,
                'kode_matkul': value.kode_matkul,
                'nama_matkul': value.nama_matkul,
            }
            result.append(obj)
        return result

    @staticmethod
    def getByidd(idd):
        matkul = Matkul.findByidd(idd)
        result = {
            "idd": matkul.idd,
            "kode_matkul": matkul.kode_matkul,
            "nama_matkul": matkul.nama_matkul
        }
        return result

    @staticmethod
    def findByidd(idd):
        return Matkul.query.filter_by(idd=idd).first()

    @staticmethod
    def findBy(kode_matkul):
        return Matkul.query.filter_by(kode_matkul=kode_matkul).first()

#get and show relation on 3 table (Angket, Nilai, Sentimen)
class Relasi():
    def relation(param,param2):
        if(param2=="all"):
            rel = db.session.query(Angket, Nilai, Sentimen).from_statement(text("SELECT * from Angket, Nilai, Sentimen where Angket.id_dosen=Nilai.id_dosen and Angket.id_dosen=Sentimen.id_dosen and Nilai.id_dosen=Sentimen.id_dosen")).all()
        else:
            rel = db.session.query(Angket, Nilai, Sentimen).from_statement(text("SELECT * from Angket, Nilai, Sentimen where Angket.id_dosen=Nilai.id_dosen and Angket.id_dosen=Sentimen.id_dosen and Nilai.id_dosen=Sentimen.id_dosen and Angket.id_olah=:search and Sentimen.id_olah=:search and Nilai.id_olah=:search")).params(search=param).all()
        result = []
        for value in rel:
            jumlah_nilai_angket = float(value[0].nilai_angket)
            jumlah_nilai_komentar = float(float(value[2].pos))
            jumlah_nilai_nilai = float(float(value[1].nilai_AB))
            jumlah = round(float(jumlah_nilai_angket + jumlah_nilai_komentar+jumlah_nilai_nilai), 2)
            if jumlah >= 0 and jumlah <= 75:
                status = "Gagal"
            elif jumlah >= 76 and jumlah <= 150:
                status = "Kurang Berhasil"
            elif jumlah >= 151 and jumlah <= 225:
                status = "Cukup Berhasil"
            elif jumlah >= 226 and jumlah <= 300:
                status = "Berhasil"
            obj = {
                "kode_matkul": Matkul.findByidd(value[0].id_matkul).kode_matkul,
                "kode_dosen": Dosen.findByidd(value[0].id_dosen).kode_dosen,
                "nilai_angket": value[0].nilai_angket,
                "nilai_AB": value[1].nilai_AB,
                "nilai_CDE": value[1].nilai_CDE,
                "sent_pos": value[2].pos,
                "sent_net": value[2].net,
                "sent_neg": value[2].neg,
                "jumlah": jumlah,
                "status": status,
            }
            result.append(obj)
        return result
