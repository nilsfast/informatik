import numpy as np  # brauchen wir für multiplikation usw
from egcd import egcd  # pip install egcd ####brauchen wir für die berechnung
import string


# Funktion für Textfeld
def input(name):
    return f'<input id="{name.lower()}" type="text" placeholder="{name}"/>'

# Textarea als Output


def output(name):
    return f'<textarea readonly  id="out" rows="7" >…</textarea>'


def number(name, min):
    return f'<input id="{name.lower()}" min="{min}" type="number" pattern="[0-9]*" placeholder="{name}"/>'


class Caesar:
    # req gibt UI-Elemente zurück
    def req():
        return {
            "inputs": [input("Klartext"), number("ROT", -100)],
            "outputs": [output("Result")]
        }

    # Enthält Code, der ausgeführt werden soll (hier Caesar)
    def encrypt(klartext, rot):
        rot = int(rot)
        clear = klartext.lower().replace(' ', '')
        return "".join([chr((ord(c) + rot-97) % 26 + 97) for c in clear])


class Hill():

    # alphabet = "abcdefghijklmnopqrstuvwxyz"  # ganz normales alphabet

    def matrix_mod_inv(matrix, modulus):
        """
        Wir finden den Matrixmodul invers durch
        Schritt 1) Determinante finden
        Schritt 2) wir suchen den Determinantenwert in einem bestimmten Modul (normalerweise die Länge des Alphabets)
        Schritt 3) danach nehmen wir det_inv mal die det*invertierte Matrix  in Mod 26
        """

        # Schritt 1)   ##muss ein integer sein
        det = int(np.round(np.linalg.det(matrix)))
        det_inv = egcd(det, modulus)[1] % modulus  # Schritt 2)
        return (
            det_inv * np.round(det * np.linalg.inv(matrix)).astype(int) % modulus)

    def verschlüsseln(Nachricht, K):    # verschlüsselung beginnt hier
        alphabet = "abcdefghijklmnopqrstuvwxyz "  # alphabet + leerzeichen
        Buchstabe_zur_Zahl = dict(zip(alphabet, range(len(alphabet))))
        Zahl_zu_Buchstabe = dict(zip(range(len(alphabet)), alphabet))
        verschlüsselt = ""
        # nachricht in nummern für die verschlüsselung in der Matrix ### hier werden sie gespeichert
        nachricht_in_zahlen = []

        for buchstabe in Nachricht:
            nachricht_in_zahlen.append(
                Buchstabe_zur_Zahl[buchstabe])   # zur liste hinzufügen

        aufteilen_P = [    # teilen die größe in die Matrix vom key
            nachricht_in_zahlen[i: i + int(K.shape[0])]  # form
            for i in range(0, len(nachricht_in_zahlen), int(K.shape[0]))
        ]

        for P in aufteilen_P:   # durchläuft jede Nachricht und verschlüsselt sie mit K*N
            # wir wollen es als array haben # wir brauchen es außerdem als column vector # damit es jetzt eine Zeile ist
            P = np.transpose(np.asarray(P))[:, np.newaxis]

            # Matrix darf nict kleiner als 1x1 sein deshalb wenn es eintritt muss z.B. ein x hinzugefügt werden
            while P.shape[0] != K.shape[0]:
                # prüfen ob das so richtig ist wie es soll in der mathematik
                P = np.append(P, Buchstabe_zur_Zahl[" "])[:, np.newaxis]

            zahlen = np.dot(K, P) % len(alphabet)  # Matrix multiplikation
            # Länge der verschlüsselten Nachricht (in Zahlen)
            n = zahlen.shape[0]

            # Map (ruft) den verschlüsselten text ab
            # wir wollen durch jede zahl gehen die sich aus dem resultierenden Vektor gehen
            for idx in range(n):
                nummer = int(zahlen[idx, 0])
                # hinzufügen zu verschlüsselt
                verschlüsselt += Zahl_zu_Buchstabe[nummer]

        return verschlüsselt

    def entschlüsseln(chiffre, Kinv):  # entschlüsselung beginnt hier
        alphabet = "abcdefghijklmnopqrstuvwxyz "  # alphabet + leerzeichen
        Buchstabe_zur_Zahl = dict(zip(alphabet, range(len(alphabet))))
        Zahl_zu_Buchstabe = dict(zip(range(len(alphabet)), alphabet))
        entschlüsselt = ""
        chiffre_in_zahlen = []

        for buchstabe in chiffre:
            # verschlüsselten text in zahlen umwandeln
            chiffre_in_zahlen.append(Buchstabe_zur_Zahl[buchstabe])

        aufteilen_C = [  # hier wieder aufteilen
            chiffre_in_zahlen[i: i + int(Kinv.shape[0])]
            for i in range(0, len(chiffre_in_zahlen), int(Kinv.shape[0]))
        ]

        for C in aufteilen_C:
            C = np.transpose(np.asarray(C))[
                :, np.newaxis]  # wieder angleichen
            zahlen = np.dot(Kinv, C) % len(alphabet)
            n = zahlen.shape[0]

            for idx in range(n):
                nummer = int(zahlen[idx, 0])
                entschlüsselt += Zahl_zu_Buchstabe[nummer]

        return entschlüsselt


class HillWrapper():
    def req():
        return {
            "inputs": [input("Klartext")],
            "outputs": [output("Result")]
        }

    def encrypt(klartext):
        K = np.matrix([[3, 10, 20], [20, 19, 17], [23, 78, 17]])
        return Hill.verschlüsseln(klartext, K)

    def decrypt(klartext):
        alphabet = "abcdefghijklmnopqrstuvwxyz "  # alphabet + leerzeichen

        K = np.matrix([[3, 10, 20], [20, 19, 17], [23, 78, 17]])
        Kinv = Hill.matrix_mod_inv(K, len(alphabet))
        return Hill.entschlüsseln(klartext, Kinv)  # besteht aus


class Gartenzaun():
    def req():
        return {
            "inputs": [input("Text"), number("Reihen", 2), number("Verschiebung", 0)],
            "outputs": [output("Result")]
        }

    def encrypt(text, reihen, verschiebung):
        reihen = int(reihen)
        verschiebung = int(verschiebung)
        strings = [''] * reihen
        for i, e in enumerate(text, start=0):
            pos = (i + verschiebung) % (reihen * 2 - 2)
            if (pos >= reihen):
                pos = reihen * 2 - 2 - pos
            strings[pos] += e
        return ''.join(strings)

    def decrypt(text, reihen=3, verschiebung=0):
        reihen = int(reihen)
        verschiebung = int(verschiebung)
        lStrings: list[str] = [''] * reihen
        for i, e in enumerate(text, start=0):
            pos: int = (i + verschiebung) % (reihen * 2 - 2)
            if (pos >= reihen):
                pos = reihen * 2 - 2 - pos
            lStrings[pos] += e

        # Seperieren des Geheimstextes in die in der Verschlüsselung verwendeten Reihen
        strings: list[str] = [''] * reihen
        s = list(text)
        for i, e in enumerate(lStrings, start=0):
            for j in range(len(e)):
                strings[i] += s[0]
                s.pop(0)

        # Umgekehrtes Einorden der Verschlüsselung / Umsortieren der Reihen zum Klartext
        res = ''
        for i in range(len(text)):
            pos: int = (i + verschiebung) % (reihen * 2 - 2)
            if (pos >= reihen):
                pos = reihen * 2 - 2 - pos
            res += strings[pos][0]
            strings[pos] = strings[pos][1:]

        return res


class Vigenere:
    def Verschlüsselung(Nachicht, Schlüssel):
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        letter_to_index = dict(zip(alphabet, range(len(alphabet))))
        index_to_letter = dict(zip(range(len(alphabet)), alphabet))

        verschlüsselt = ""
        # die Nachicht muss klein geschrieben werden damit der code funktioniert
        Nachicht = Nachicht.lower()
        Schlüssel = Schlüssel.lower()  # auch der Schlüssel muss klein sein
        split_message = [
            Nachicht[x: x + len(Schlüssel)] for x in range(0, len(Nachicht), len(Schlüssel))
        ]  # Aufteilen der Nachicht auf die Länge des Schlüssels
        for each_split in split_message:
            x = 0
            for letter in each_split:
                # Die Nachicht zu ihrer zugeteilten Nummer umwandeln und die Nummer des dem ensprechendem code hinzufügen
                number = (
                    letter_to_index[letter] + letter_to_index[Schlüssel[x]]) % len(alphabet)
                # Die Nummer wieder in einen Buchstaben umwandeln
                verschlüsselt += index_to_letter[number]
                x += 1
        return verschlüsselt

    def Entschlüsselung(Chiffre, Schlüssel):
        alphabet = "abcdefghijklmnopqrstuvwxyz"

        letter_to_index = dict(zip(alphabet, range(len(alphabet))))
        index_to_letter = dict(zip(range(len(alphabet)), alphabet))

        entschlüsselt = ""
        Schlüssel = Schlüssel.lower()
        split_encrypted = [
            Chiffre[x: x + len(Schlüssel)] for x in range(0, len(Chiffre), len(Schlüssel))
        ]

        for each_split in split_encrypted:
            x = 0
            for letter in each_split:
                number = (
                    letter_to_index[letter] - letter_to_index[Schlüssel[x]]) % len(alphabet)
                entschlüsselt += index_to_letter[number]
                x += 1
            # Entschlüsselung funkrioniert ähnlich wie Verschlüsselung nur das hier der key von dem Angegegben Buschstaben subtrahiert wird anstatt addiert
        return entschlüsselt


"""
def main():
    Nachicht = "Das ist meine Nachicht"
    Schlüssel = "Vigenere"
    verschlüsselte_nachicht = Verschlüsselung(Nachicht, Schlüssel)
    entschlüsselte_nachicht = Entschlüsselung(verschlüsselte_nachicht, Schlüssel)

    print("Origiale Nachicht: " + Nachicht)
    print("Verschlüsselte Nachicht: " + verschlüsselte_nachicht)
    print("Entschlüsselte Nachicht: " + entschlüsselte_nachicht)
"""


class VigenereWrapper:
    def req():
        return {
            "inputs": [input("Klartext"), input("Losungswort")],
            "outputs": [output("Result")]
        }

    def encrypt(klartext, losungswort):
        return Vigenere.Verschlüsselung(klartext, losungswort)

    def decrypt(klartext, losungswort):
        return Vigenere.Entschlüsselung(klartext, losungswort)
