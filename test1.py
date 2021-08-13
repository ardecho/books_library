# -*- coding: utf-8 -*-
from flask import Flask,g
import os
import sqlite3
from flask import render_template

app = Flask(__name__)


# konfiguracja aplikacji
app.config.update(dict(
    # nieznany nikomu sekret dla mechanizmu sesji
    SECRET_KEY = 'jobinterview',
    # polozenie naszej bazy
    DATABASE = os.path.join(app.root_path, 'db.sqlite'),
    # nazwa aplikacji
    SITE_NAME = 'Books Liblary'
))

def connect_db():
    """Nawiazywanie połaczenia z bazą danych określoną w konfiguracji."""
    """http://flask.pocoo.org/docs/0.10/patterns/sqlite3/"""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Funkcja pomocnicza, ktora tworzy połączenia z bazą przy pierwszym
    wywołaniu i umieszcza ja w kontekście aplikacji (obiekt g). W kolejnych
    wywołaniach zwraca połączenie z kontekstu."""
    if not hasattr(g, 'db'):
        g.db = connect_db() # jezeli kontekst nie zawiera informacji o polaczeniu to je tworzymy
    return g.db # zwracamy polaczenie z baza

# dekorator wykonujacy funkcje po wyslaniu odpowiedzi do klienta
@app.teardown_request
def close_db(error):
    """Zamykanie polaczenia z baza."""
    if hasattr(g, 'db'):
        g.db.close()




# DEKORATORY
@app.route('/')
def index():
    return render_template('index.html')



@app.route('/books-list')
def bookList():
    db = get_db() # laczymy sie z baza
    # pobieramy wszystkie wpisy z bazy:
    cur = db.execute('select id, author, title, publication_date, ISBN, pages, cover, lang from books order by id desc;')
    entries = cur.fetchall()
    # renderujemy tempaltke i zwracamy ja do klienta
    return render_template('results.html', entries=entries)


@app.route('/book-input')
def bookInput():
    db = get_db() # laczymy sie z baza
    # pobieramy wszystkie wpisy z bazy:
    cur = db.execute('select id, author, title, publication_date, ISBN, pages, cover, lang from books order by id desc;')
    entries = cur.fetchall()
    # renderujemy tempaltke i zwracamy ja do klienta
    return render_template('results.html', entries=entries)





# # dekorator laczacy adres glowny z widokiem index
# @app.route('/')
# def index():
#     return 'Witaj na moim serwerze!'


@app.route('/dupa')
def dupa():
    return 'chuj dupa cycki'


if __name__ == '__main__':
    app.run(debug=True)