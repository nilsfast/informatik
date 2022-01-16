import string


#Funktion für Textfeld
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


class Rotor:
    def __init__(self, name, start, rotoratright=None):
        if name == 1: # Typ-I-Rotor
            self.d_wiring = dict(zip(string.ascii_lowercase, "ekmflgdqvzntowyhxuspaibrcj")) # Abbildung interner Verbindungen
            self.r_wiring = dict(zip("ekmflgdqvzntowyhxuspaibrcj", string.ascii_lowercase)) # umgekehrt abgebildet
            self.turnover = "q" # von q bis r
        elif name == 2: # Typ-II-Rotor
            self.d_wiring = dict(zip(string.ascii_lowercase, "ajdksiruxblhwtmcqgznpyfvoe"))
            self.r_wiring = dict(zip("ajdksiruxblhwtmcqgznpyfvoe", string.ascii_lowercase))
            self.turnover = "e" # von e bis f
        elif name == 3: # Rotor vom Typ III
            self.d_wiring = dict(zip(string.ascii_lowercase, "bdfhjlcprtxvznyeiwgakmusqo"))
            self.r_wiring = dict(zip("bdfhjlcprtxvznyeiwgakmusqo", string.ascii_lowercase))
            self.turnover = "v" # von v bis w
        
        self.type = name
        self.position = start
        self.rotated = False
        self.rightrotor = rotoratright # der Rotor dreht sich nach rechts, wenn er keine hat


    def __str__(self):
        return "Rotor type {}, pos = {}".format(self.type, self.position)
            

    def rotate(self):
        if(self.rightrotor != None and self.position == self.turnover): #!!
            

            self.position = chr((ord(self.position)-ord("a")+1)%len(string.ascii_lowercase) + ord("a"))
            self.rotated = True
            
            return
        else:
            self.rotated = False
            
        if(self.rightrotor == None):
            # Wenn sich rechts kein Rotor befindet, dreht er sich jedes Mal, wenn ein Buchstabe verschlüsselt wird

            self.position = chr((ord(self.position)-ord("a")+1)%len(string.ascii_lowercase) + ord("a"))
            self.rotated = True
            
        elif(self.rightrotor.position == chr(ord(self.rightrotor.turnover)+1) and self.rightrotor.rotated):
            # Wenn es einen Rotor auf der rechten Seite gibt, dreht sich dieser Rotor, wenn der Rotor auf der rechten Seite eine Drehung macht (wenn seine Position gleich seinem Drehwert ist).
            # macht eine Drehung (wenn seine Position gleich seinem 'turnover' ist).

            self.position = chr((ord(self.position)-ord("a")+1)%len(string.ascii_lowercase) + ord("a"))
            self.rotated = True
            
        else:
            self.rotated = False
            

    def d_encrypt(self, char): # direkte Verschlüsselung, von rechts nach links
        self.rotate()
        char = chr((ord(char)-ord("a")+ord(self.position)-ord("a"))%len(string.ascii_lowercase) + ord("a"))
        char = self.d_wiring.get(char)
        char = chr((ord(char)-ord("a")-ord(self.position)+ord("a"))%len(string.ascii_lowercase) + ord("a"))
        return char

    def r_encrypt(self, char): # umgekehrte Verschlüsselung, denn wenn sie bereits den Spiegel passiert hat
        char = chr((ord(char)-ord("a")+ord(self.position)-ord("a"))%len(string.ascii_lowercase) + ord("a"))
        char = self.r_wiring.get(char)
        char = chr((ord(char)-ord("a")-ord(self.position)+ord("a"))%len(string.ascii_lowercase) + ord("a"))
        return char        

class Enigma:
# Dieses Enigma HAT KEIN 'Plugboard' das würde den Rahmen sprengen
# Wir müssen auch Methoden hinzufügen, um die Maschine zurückzusetzen oder zu setzen
# in der gewünschten Konfiguration...
    def __init__(self):
        self.r1 = Rotor(1, "a", None)
        self.r2 = Rotor(2, "a", self.r1)
        self.r3 = Rotor(3, "a", self.r2)
        self.reflector = dict(zip(string.ascii_lowercase, "yruhqsldpxngokmiebfzcwvjat"))
    def encrypt(self, s):
        out = []
        for c in s.lower():   #alle Buchstaben auf eine "Größe"
            if c not in string.ascii_lowercase:
                out.append(c)
                continue
            c = self.r1.d_encrypt(c)
            c = self.r2.d_encrypt(c)
            c = self.r3.d_encrypt(c)

            c = self.reflector.get(c)

            c = self.r3.r_encrypt(c)
            c = self.r2.r_encrypt(c)
            c = self.r1.r_encrypt(c)

            out.append(c)
            
        return "".join(out)

class EnigmaWrapper:
    def req():
        return {"inputs": [input("Klartext")],
        "outputs": [output("Result")]}
    def encrypt(klartext):
        e = Enigma()
        return e.encrypt(klartext) 

class Gartenzaun():
    def req():
        return {
            "inputs": [input("Text"), number("Reihen", 2), number("Verschiebung", 0)],
            "outputs": [output("Result")]
        }
    def encrypt(text, reihen, verschiebung ):
        reihen = int(reihen)
        verschiebung = int(verschiebung)
        strings = [''] * reihen
        for i, e in enumerate(text, start = 0):
            pos = (i + verschiebung) % (reihen * 2 - 2)
            if (pos >= reihen): 
                pos = reihen * 2 - 2 - pos
            strings[pos] += e
        return ''.join(strings)

    def decrypt(text, reihen = 3, verschiebung = 0):
        reihen = int(reihen)
        verschiebung = int(verschiebung)
        lStrings: list[str] = [''] * reihen
        for i, e in enumerate(text, start = 0):
            pos: int = (i + verschiebung) % (reihen * 2 - 2)
            if (pos >= reihen): 
                pos = reihen * 2 - 2 - pos
            lStrings[pos] += e

        ### Seperieren des Geheimstextes in die in der Verschlüsselung verwendeten Reihen
        strings: list[str] = [''] * reihen
        s = list(text)
        for i, e in enumerate(lStrings, start = 0):
            for j in range(len(e)):
                strings[i] += s[0]
                s.pop(0)

        ### Umgekehrtes Einorden der Verschlüsselung / Umsortieren der Reihen zum Klartext
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
        Nachicht = Nachicht.lower()#die Nachicht muss klein geschrieben werden damit der code funktioniert
        Schlüssel = Schlüssel.lower()#auch der Schlüssel muss klein sein
        split_message = [
            Nachicht[x : x + len(Schlüssel)] for x in range(0, len(Nachicht), len(Schlüssel))
        ] # Aufteilen der Nachicht auf die Länge des Schlüssels
        for each_split in split_message:
            x = 0
            for letter in each_split:
                number = (letter_to_index[letter] + letter_to_index[Schlüssel[x]]) % len(alphabet)#Die Nachicht zu ihrer zugeteilten Nummer umwandeln und die Nummer des dem ensprechendem code hinzufügen
                verschlüsselt += index_to_letter[number]# Die Nummer wieder in einen Buchstaben umwandeln
                x += 1
        return verschlüsselt

    def Entschlüsselung(Chiffre, Schlüssel):
        alphabet = "abcdefghijklmnopqrstuvwxyz"

        letter_to_index = dict(zip(alphabet, range(len(alphabet))))
        index_to_letter = dict(zip(range(len(alphabet)), alphabet))

        entschlüsselt = ""
        Schlüssel = Schlüssel.lower()
        split_encrypted = [
            Chiffre[x : x + len(Schlüssel)] for x in range(0, len(Chiffre), len(Schlüssel))
        ]

        for each_split in split_encrypted:
            x = 0
            for letter in each_split:
                number = (letter_to_index[letter] - letter_to_index[Schlüssel[x]]) % len(alphabet)
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
    def encrypt( klartext, losungswort):
        return Vigenere.Verschlüsselung(klartext, losungswort)

    def decrypt( klartext, losungswort):
        return Vigenere.Entschlüsselung(klartext, losungswort)

