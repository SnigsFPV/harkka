from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import json
import sqlite3

app = Flask(__name__)

tuotteet_tmp = []

@app.route('/testi', methods=['GET'])
def result():
    tuotteet_tmp = []
    con = sqlite3.connect("kauppalista.db3")
    cur = con.cursor()
    cur.execute("SELECT * from tuotteet")

    tiedot = cur.fetchall()
    print(tiedot)

    for tuote in tiedot:
        tmp = dict(id=tuote[0], nimi=tuote[1], maara=tuote[2])
        print(tmp)
        tuotteet_tmp.append(tmp)
       
        
    con.commit()
    con.close()

    return render_template('testi.html', tuotelista = tuotteet_tmp)
    

if __name__ == '__main__':
    app.run(debug=True)
    #socketio.run(app)
