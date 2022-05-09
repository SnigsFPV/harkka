from flask import Flask, render_template, request
import json
import sqlite3

app = Flask(__name__)

Tuotteet = [{'':''}]

viikonpaivat = ['Maanantai', 'Tiistai', 'Keskiviikko', 'Torstai', 'Perjantai', 'Lauantai', 'Sunnuntai']

con = sqlite3.connect("lampotilat.db3")
cur = con.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS lampotilat (id INTEGER PRIMARY KEY, paiva INTEGER, asteet INTEGER)')
con.commit()
con.close()

@app.route('/lampotilat', methods=['GET'])
def result():
    return render_template('lampotilat.html', result = lampotilat)

@app.route('/lampotilalista', methods=['GET'])
def lista_result():
    return render_template('lampotilat_lista.html', taulukko = lampotilat, paivat = viikonpaivat)

@app.route('/paivita/<int:id>&<int:tmp>', methods=['GET'])
def update(id, tmp):
    t = {'x':id, 'y':tmp}
    lampotilat[id-1] = t
    return render_template('lampotilat.html', result = lampotilat)

@app.route('/api/listaan/', methods=['POST'])
def add_json():
    print(request.data) #Post pyynnössä tulee request ja sen data-kentässä json viesti
    tmp = json.loads(request.data, strict=False) #Muutetaan json sanakirja tietorakenteeksi
    print(tmp)
    x = tmp["x"]-1 # haetaan sanakirjasta avaimella "x" arvo
    lampotilat[x] = tmp

    return {"message" : 'success'}


@app.route('/api/tietokantaan/', methods=['POST'])
def add_db():
    tmp = json.loads(request.data, strict=False) #Muutetaan json sanakirja tietorakenteeksi

    con = sqlite3.connect("lampotilat.db3")
    cur = con.cursor()
    cur.execute("INSERT INTO lampotilat (paiva, asteet) VALUES (?, ?)", [tmp["x"],tmp["y"]])
    con.commit()
    con.close()

    return {"message" : 'success'}


if __name__ == '__main__':
    app.run(debug=True)

