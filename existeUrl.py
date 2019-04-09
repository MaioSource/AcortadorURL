# -*- coding: utf-8 -*-
from app import db, Url
#Si existe la urlCorta en la BD devuelve False
#Si NO existe la urlCorta en la BD devuelve True
def noExiste(urlCorta):
        urlExists = Url.query.filter_by(UrlCorta = urlCorta).first()
        return False if urlExists else True
