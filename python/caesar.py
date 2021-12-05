# Anfangs-Code
def caesar_mr(klartext, schluessel):
    geheimtext = ""
    for zeichen in klartext:
        zahl = ord(zeichen)  # variable nicht deskriptiv
        neueZahl = zahl + schluessel  # unnötig, nicht deskriptiv
        # was wenn zahl + schluessel > 26 oder < 0
        neuesZeichen = chr(neueZahl)  # snake_case benutzen
        geheimtext = geheimtext + neuesZeichen  # += operator nutzen
    return geheimtext


print(caesar_mr("a", 5))  # -> f
print(caesar_mr("a", 100))  # -> Å
print(caesar_mr("a", -99))  # -> ValueError


# Verbesserung
def caesar_nf(clear: str, rot: int):
    clear = clear.lower().replace(' ', '')
    return "".join([chr((ord(c) + rot-97) % 26 + 97) for c in clear])


print(caesar_nf("a", 5))  # -> f
print(caesar_nf("hallo", 29))  # -> kdoor
