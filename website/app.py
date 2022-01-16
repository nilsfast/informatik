from flask import Flask, render_template, request, redirect, send_from_directory, abort
from functions import *  # functions.py : dort sind alle Klassen für die Algorithmen
import json

# Konfiguration für Flask
app = Flask(__name__,
            static_folder="static",
            static_url_path="/static",
            )

# assoz. Liste für die Seiten
pages = {
      "gartenzaun": {
        "class": Gartenzaun,
        "name": "Gartenzaun",
        "by": "Rishab Garg",
        "code": "gartenzaun.txt",
        "decrypt": True
    },
    "hill": {  # Name in der URL
        "class": HillWrapper,  # Klasse
        "name": "Hill Cipher",  # Anzeigename
        "by": "Maximilian Nobis",
        "code": "hill.txt",  # Datei mit code als txt
        "decrypt": True
    },
    "caesar": {
        "class": Caesar,
        "name": "Caesar",
        "by": "Nils Fast",
        "code": "caesar.txt",
        "decrypt": False
    },
  
    "vigenere": {
        "class": VigenereWrapper,
        "name": "Vigenere",
        "by": "Mattis Schucher",
        "code": "vigenere.txt",
        "decrypt": True
    }
}


#
@app.route("/")
def index():
    return redirect("/gartenzaun", code=302)

# Funktion für alle Anfragen nach Schema /*/


@app.route("/<page>/")
def page(page):

    if page not in pages:
        abort(404)

    # UI-Bedingungen auslesen
    fields = pages[page]["class"].req()

    # Code Datei -> Variable
    codefile = open("code/"+pages[page]["code"], "r")
    code = codefile.read()

    # Vorlage rendern mir Code, Autor, Inputs etc.
    return render_template('base.html', fields=fields, this=page, by=pages[page]["by"], pages=pages, code=code, decrypt=pages[page]["decrypt"])

# Schnittstelle für die Ausführung des Codes über POST


@app.route("/<page>/encrypt", methods=["POST"])
def encrypt(page):
    if page not in pages:
        abort(404)
    # Nutzer-Eingaben aus Request Header laden
    data = json.loads(request.headers["Data"])

    # Funktion ausführen mit Eingaben und zurückgeben als String
    try:
        return pages[page]["class"].encrypt(**data)
    except:
        return "Ein Fehler ist aufgetreten"

# Schnittstelle für die Entschlüsselung des Codes über POST


@app.route("/<page>/decrypt", methods=["POST"])
def decrypt(page):
    if page not in pages:
        abort(404)
    # Nutzer-Eingaben aus Request Header laden
    data = json.loads(request.headers["Data"])

    # Funktion ausführen mit Eingaben und zurückgeben als String
    try:
        return pages[page]["class"].decrypt(**data)
    except:
        return "Ein Fehler ist aufgetreten"


app.run(debug=False, host="0.0.0.0")  # Startet die Flask-App
