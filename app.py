from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:asdasd@localhost/stki_stemming'
db = SQLAlchemy(app)

@app.route('/')
def index():
    dokumen = Dokumen.query.all()
    # for i in dokumen[0].text.split(" "):
    #     print(i)
    # return 'Hello, World!'
    return render_template('index.html', dokumen=dokumen)

@app.route('/result/<id_dokumen>')
def result(id_dokumen=None):
    dts = DokumenTerm.query.filter_by(id_dokumen=id_dokumen)

    return render_template('result.html', dts=dts)

@app.route('/generate')
def generate_result():
    dokumen = Dokumen.query.all()
    for dok in dokumen:
        terms = dok.text.split(" ")
        index_term = 1
        for t in terms:
            if (len(t) > 30):
                continue

            # status
            print("dokumen-{}\tterm-{}".format(dok.id_dokumen, index_term))
            index_term += 1

            term = Term.query.filter_by(term=t).all()

            if (len(term) == 0) :
                hasil_stem1, waktu_stem1 = stem_nazhief_adriani(t)
                term = Term(
                    term = t,
                    hasil_stem1 = hasil_stem1,
                    hasil_stem2 = hasil_stem1,
                    waktu_stem1 = waktu_stem1,
                    waktu_stem2 = waktu_stem1+4,
                )
                db.session.add(term)
                db.session.commit()
                dt = DokumenTerm(
                    id_dokumen = dok.id_dokumen,
                    id_term = term.id_term
                )
                db.session.add(dt)
                db.session.commit()
            else :
                term = term[0]
                dt = DokumenTerm.query.filter_by(id_dokumen = dok.id_dokumen, id_term=term.id_term).all()
                if (len(dt) == 0) :
                    dt = DokumenTerm(
                        id_dokumen = dok.id_dokumen,
                        id_term = term.id_term
                    )
                else :
                    dt = dt[0]
                    dt.freq += 1
                term.freq += 1
                db.session.commit()
    # n_a_stemmer
    return 'sukses'

@app.route('/reset')
def reset():
    return 'reset'

def stem_nazhief_adriani(term):
    # create stemmer
    factory = StemmerFactory()
    n_a_stemmer = factory.create_stemmer()

    start = time.time()
    hasil_stem = n_a_stemmer.stem(term)
    waktu = time.time() - start

    return hasil_stem, waktu

class Dokumen(db.Model):
    __tablename__ = 'dokumen'
    id_dokumen = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(65535), nullable=False)

    # relasi
    terms = db.relationship("Term", secondary="dokumen_term")

class Term(db.Model):
    __tablename__ = 'term'
    id_term = db.Column(db.Integer, primary_key=True, autoincrement=True)
    term = db.Column(db.String(30), nullable=False)
    hasil_stem1 = db.Column(db.String(30), nullable=False)
    hasil_stem2 = db.Column(db.String(30), nullable=False)
    waktu_stem1 = db.Column(db.Float, nullable=False)
    waktu_stem2 = db.Column(db.Float, nullable=False)
    status_stem1 = db.Column(db.Integer, nullable=True)
    status_stem2 = db.Column(db.Integer, nullable=True)
    freq = db.Column(db.Integer, nullable=False, default=1)

    # relasi
    documents = db.relationship("Dokumen", secondary="dokumen_term")

class DokumenTerm(db.Model):
    __tablename__ = 'dokumen_term'
    id_dokumen = db.Column(db.Integer, db.ForeignKey('dokumen.id_dokumen'), primary_key=True)
    id_term = db.Column(db.Integer, db.ForeignKey('term.id_term'), primary_key=True)
    freq = db.Column(db.Integer, nullable=False, default=1)

    # relasi
    dokumen = db.relationship(Dokumen, backref=backref('dokumen_term', cascade="all, delete-orphan"))
    term = db.relationship(Term, backref=backref('dokumen_term', cascade="all, delete-orphan"))

if __name__ == '__main__':
    app.run()
