# -*- coding: utf-8 -*-
from flask import request, redirect, render_template, Flask
import os
import string

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

host="https://agustinmaio.cf/" 
dev_info = ["https://github.com/MaioSource","Agustín Maio".decode('utf-8')]
source_code = "https://github.com/MaioSource/AcortadorURL"
app.secret_key=os.urandom(24)
app.config.from_pyfile('config.cfg')

db = SQLAlchemy(app)


class Url(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        UrlLarga = db.Column(db.String(512))
        UrlCorta = db.Column(db.String(512))
db.create_all()

import existeUrl

@app.route('/', methods=['GET', 'POST'])
def home():
        if request.method == 'POST':
                urlOriginal = request.form.get('URLLargo')
                if "http://" in urlOriginal or "https://" in urlOriginal:
                        url=urlOriginal
                else:
                        url="http://" + urlOriginal
                url_personalizada = host + request.form.get('URLCorto')
                
                if (existeUrl.noExiste(url_personalizada)==True):
                        newUrl = Url(UrlLarga = url, UrlCorta = url_personalizada)
                        db.session.add(newUrl)
                        db.session.commit()
                else:
                        return render_template('index.html', host=host, yaUsado="URL personalizada ya se encuentra en uso.")
                return render_template('index.html', host=host, urlCorto=url_personalizada, dev_info=dev_info, source_code=source_code)

        return render_template('index.html', host=host, dev_info=dev_info, source_code=source_code)

@app.route('/<urlCorta>', methods=['GET', 'POST'])
def redireccionar(urlCorta):
        urlCorta=host+urlCorta
        urlExists = Url.query.with_entities(Url.UrlLarga).filter_by(UrlCorta = urlCorta).first()
        try:
                return redirect(urlExists.UrlLarga)
        except Exception as e:
                return redirect(host)


if __name__ == '__main__':
        app.run(host='0.0.0.0')
