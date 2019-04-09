from flask import Flask, render_template, redirect, url_for, request, flash, \
    get_flashed_messages
import requests as req
from bs4 import BeautifulSoup
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.orm import backref
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from TalaStemm import TalaStemmFactory
import re

import time

app = Flask(__name__)
app.secret_key = b'\x10\xeft\x80\xba\x1f\xb1\xd5\x03\x82}\xf4\xd7\xe2\xb0\xd6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:asdasd@localhost/stki_stemming'
app.config['TEMPLATES_AUTO_RELOAD'] = True
db = SQLAlchemy(app)

# create stemmer
factory = StemmerFactory()
n_a_stemmer = factory.create_stemmer()
tala_stemmer = TalaStemmFactory().getTalaStemmer()
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data/dokumen')
def data_dokumen():
    dokumen = Dokumen.query.all()
    return render_template('data_dokumen.html', dokumen=dokumen)

@app.route('/data/dokumen/scrap')
def hello_world():
    # print(urls)
    # return 'Hello'
    base_url = 'http://rumahginjal.id'
    url = 'http://rumahginjal.id/category/berita'
    print("get url")
    for i in range(1, 11):
        get_data(url + '?page=' + str(i), base_url)
    # urls = HalDepan.query.with_entities(HalDepan.url).all()
    # print("get detail berita")
    # for i in urls:
    #     get_detail_berita(i.url)
    return redirect(url_for('data_dokumen'))

@app.route('/data/term')
def data_term():
    term = Term.query.order_by(Term.term).all()
    return render_template('data_term.html', term=term)

@app.route('/data/term/generate')
def generate_term():
    dokumen = Dokumen.query.all()

    tanda_baca = ['"', '.', ',', '\'', '“', '”', '(', ')', '/', '?', '!', ';', '-', ':']
    for dok in dokumen:
        # karakter non alphabet
        regex = re.compile('[^a-zA-Z \n]')
        terms = regex.sub('', dok.text)

        # menghapus spasi yang duplikat
        terms = " ".join(terms.split())

        # menghilangkan tanda baca
        # terms = dok.text.translate(str.maketrans('', '', ''.join(tanda_baca)))

        # menyimpan tiap term dalam dokumen ke dalam bentuk array
        terms = terms.split(" ")

        index_term = 1
        for t in terms:
            if (len(t) > 30):
                # Jika karakter melebihi 30 maka dia akan mengenalinya sebagai non kata (bisa berupa url ataupun yang lain)
                continue

            t = t.lower()
            # status
            print("dokumen-{}\tterm-{}".format(dok.id_dokumen, index_term))
            index_term += 1

            term = Term.query.filter_by(term=t).first()

            if (term is None) :
                term = Term(
                    term = t
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
                dt = DokumenTerm.query.filter_by(id_dokumen = dok.id_dokumen, id_term=term.id_term).first()

                # Jika term belum ada atau sudah pernah ada tapi bukan di dokumen ini
                if (dt is None):
                    dt = DokumenTerm(
                        id_dokumen = dok.id_dokumen,
                        id_term = term.id_term
                    )

                else :
                    dt.freq += 1
                term.freq += 1
                db.session.commit()
    '''
    '''
    # n_a_stemmer

    flash(u'Term sukses digenerate !', 'success')
    return redirect(url_for('data_term'))

@app.route('/hasil')
def hasil():
    terms = Term.query.order_by(Term.term).all()
    jml_valid_stem1 = db.session.query(Term).filter_by(status_stem1=1).count()
    jml_valid_stem2 = db.session.query(Term).filter_by(status_stem2=1).count()
    # print(terms[0].hasil_stem1 is None)
    # return 'Hello'
    return render_template('hasil.html', terms=terms, jml_valid_stem1=jml_valid_stem1, jml_valid_stem2=jml_valid_stem2)

@app.route('/hasil/generate')
def generate_hasil():

    kamus = Kamus.query.with_entities(Kamus.katadasar).all()

    # print(kamus.count())
    # return 'test'

    # Mengambil data katadasar dari database
    kamus = [k[0] for k in kamus]
    # a = ('abar')
    # print(a in kamus)
    # print(kamus[1])
    # print(type(kamus[1]))
    # print(type(kamus))
    # return 'hello'
    '''
    result = '<pre>'
    for k in kamus:
        result = result + '\n{}'.format(k.katadasar)
    result = result + '</pre>'
    return result
    '''

    terms = Term.query.all()
    for t in terms:
        t.hasil_stem1, t.waktu_stem1 = stem_nazhief_adriani(t.term)
        t.hasil_stem2, t.waktu_stem2 = stem_tala(t.term)
        t.status_stem1 = t.hasil_stem1 in kamus
        t.status_stem2 = t.hasil_stem2 in kamus
    db.session.commit()
    return redirect(url_for('hasil'))

@app.route('/reset')
def reset():
    return 'reset'

def stem_tala(term):
    start = time.time()
    hasil_stem = tala_stemmer.stem(term)
    waktu = time.time() - start
    return hasil_stem, waktu

def stem_nazhief_adriani(term):
    start = time.time()
    hasil_stem = n_a_stemmer.stem(term)
    waktu = time.time() - start
    return hasil_stem, waktu

def save_berita(judul, content, url):
    data = DetailedNews(
        judul=judul,
        url=url,
        content=content
    )
    data = Dokumen(text = content)
    db.session.add(data)
    db.session.commit()
    return True


def scrapt(url):
    requests = req.get(url).text
    return requests


def sorting_html(url):
    a = scrapt(url)
    bs = BeautifulSoup(a, 'lxml')
    dat = bs.find('section', {'class': 'g-pt-100 g-pb-50'})
    listartikel = dat.find_all('div', {'class': 'col-md-8 align-self-center g-pl-20'})
    return listartikel


def simpan_database_haldepan(url):
    if url is not None:
        hal = HalDepan(url=url)
        db.session.add(hal)
        db.session.commit()
        return True
    return False


def get_data(url, base_url):
    data = sorting_html(url)
    # arr_url = []
    for i in range(len(data)):
        get_detail_berita(base_url + data[i].a['href'])
        simpan_database_haldepan(base_url + data[i].a['href'])
    return "Selesai"


def get_detail_berita_khusus(url):
    mentah = req.get('http://rumahginjal.id/rumah-ginjal-fatma-saifullah-yusuf-anak-difabel-jangan-disembunyikan').text
    bs = BeautifulSoup(mentah, 'lxml')
    artikel = bs.find('div', {'class': 'g-font-size-16 g-line-height-1_8 g-mb-30'})
    artikel1 = artikel.find_all('div')
    judul = bs.find('h2', {'class': 'h1 g-mb-15'}).text
    gabungan_artikel = []
    for i in range(len(artikel1)):
        gabungan_artikel.append(artikel1[i].text.strip())
    content = ' '.join(gabungan_artikel)
    return save_berita(judul, content, url)


def get_detail_berita(url):
    mentah = scrapt(url)
    bs = BeautifulSoup(mentah, 'lxml')
    artikel = bs.find('div', {'class': 'g-font-size-16 g-line-height-1_8 g-mb-30'})
    if url == 'http://rumahginjal.id/rumah-ginjal-fatma-saifullah-yusuf-anak-difabel-jangan-disembunyikan':
        artikel1 = artikel.find_all('div')
    else:
        artikel1 = artikel.find_all('p')
    judul = bs.find('h2', {'class': 'h1 g-mb-15'}).text
    gabungan_artikel = []
    for i in range(len(artikel1)):
        gabungan_artikel.append(artikel1[i].text.strip())
    content = ' '.join(gabungan_artikel)
    return save_berita(judul, content, url)

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

class Kamus(db.Model):
    __tablename__ = 'tb_katadasar'
    id_katadasar = db.Column(db.Integer, primary_key=True, autoincrement=True)
    katadasar = db.Column(db.String(70), nullable=False)
    tipe_katadasar = db.Column(db.String(25), nullable=False)

class HalDepan(db.Model):
    __tablename__ = 'haldepan'
    id_ = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.TEXT)


class DetailedNews(db.Model):
    __tablename__ = 'detail_news'
    iddetail_news = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.TEXT)
    content = db.Column(db.TEXT)
    url = db.Column(db.TEXT)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)
