import os

from flask import Flask, render_template, request, redirect, url_for, escape
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:////tmp/flask_app.db')

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(app)
FIELDS = 'perfum', 'ilosc', 'atomizer', 'miasto', 'nick', 'klucz'

class Wpis(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  perfum = db.Column(db.String(32), nullable=False)
  ilosc = db.Column(db.Integer, nullable=False)
  atomizer = db.Column(db.Boolean)
  kupie = db.Column(db.Boolean)
  miasto = db.Column(db.String(32))
  nick = db.Column(db.String(32), nullable=False)
  klucz = db.Column(db.String(32))

  def __init__(self, perfum, ilosc, atomizer, kupie, miasto, nick, klucz):
    self.perfum = perfum
    self.ilosc = ilosc
    self.atomizer = atomizer
    self.kupie = kupie
    self.miasto = miasto
    self.nick = nick
    self.klucz = klucz

@app.route('/', methods=['GET'])
def index():
  db.create_all()
  return render_template('index.html', wpisy=Wpis.query.all())

# basic_sanitize
def bs(item):
  if len(item)>32:
    item = item[:32]
  return escape(item)
def bsi(item):
  try:
    i = int(item)
  except:
    return 0
  if i > 256 or i < 0:
    return 0
  return i
def bso(it):
  return 1 if it == "on" else 0

@app.route('/wpis', methods=['POST'])
def wpis():
  

  atomizer = bso(request.form.get('atomizer', 0))
  kupie = bso(request.form.get('kupie', 0))

  w = Wpis(bs(request.form['perfum']), bsi(request.form['ilosc']), 
           atomizer, kupie, bs(request.form['miasto']), 
           bs(request.form['nick']), bs(request.form['klucz']))
  
  db.session.add(w)
  db.session.commit()
  return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete():
  nr = bsi(request.form['number'])
  x = Wpis.query.get_or_404(nr, f"Wpis {nr} nie istnieje.")
  if x and bs(request.form['klucz']) and bs(request.form['klucz']) == x.klucz:
    db.session.delete(x)
    db.session.commit()
  # else unauthorized, which should be communicated to user...
  return redirect(url_for('index'))
  
if __name__ == '__main__':
  db.create_all()
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
