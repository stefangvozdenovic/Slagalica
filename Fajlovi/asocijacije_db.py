import sqlite3

conn = sqlite3.connect('asocijacije.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS asocijacije (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    konacno_rjesenje TEXT NOT NULL,
    a1 TEXT NOT NULL,
    a2 TEXT NOT NULL,
    a3 TEXT NOT NULL,
    a4 TEXT NOT NULL,
    rjesenje_a TEXT NOT NULL,
    b1 TEXT NOT NULL,
    b2 TEXT NOT NULL,
    b3 TEXT NOT NULL,
    b4 TEXT NOT NULL,
    rjesenje_b TEXT NOT NULL,
    c1 TEXT NOT NULL,
    c2 TEXT NOT NULL,
    c3 TEXT NOT NULL,
    c4 TEXT NOT NULL,
    rjesenje_c TEXT NOT NULL,
    d1 TEXT NOT NULL,
    d2 TEXT NOT NULL,
    d3 TEXT NOT NULL,
    d4 TEXT NOT NULL,
    rjesenje_d TEXT NOT NULL
)
''')

asocijacije = [
    (
        "PROFIL",
        "Rat", "Test", "Pritisak", "Poremećaj",
        "PSIHOLOŠKI.PSIHOLOSKI.PSIHO",
        "Ram", "Platno", "Pasoš", "1000 riječi",
        "SLIKA.SLIKE",
        "Lagan", "Metal", "Folija", "Felna",
        "ALUMINIJUM",
        "Slike", "Prijatelji", "Ćaskanje", "Povezivanje",
        "FEJSBUK.FACEBOOK"
    ),
    (
        "APOTEKA",
        "Ford", "Kuća", "Motor", "Fabrika",
        "AUTO.AUTOMOBIL",
        "Bolest", "Sirup", "Tableta", "Prirodni",
        "LIJEK.LEK",
        "Škola", "Lična", "Stvar", "Svojina",
        "PRIVATNA.PRIVATNI.PRIVATNO",
        "Ratarstvo", "Institut", "Mehanizacija", "Zemljoradnja",
        "POLJOPRIVREDA"
    ),
    (
        "LJUBAV",
        "Mlijeko", "Briga", "Jevrosima", "Tereza",
        "MAJKA.MAMA",
        "Grčka", "Pazova", "Garda", "Škola",
        "STARA",
        "Čarape", "Rukavice", "Ples", "Sudija",
        "PAR",
        "Volja", "Saglasnost", "Biser", "Mediji",
        "IZJAVA"
    ),
    (
        "TEKSAS",
        "Zima", "Perje", "Vijetnam", "Koža",
        "JAKNA",
        "Trejsi", "Batler", "Paures", "Džejn",
        "OSTIN",
        "Problem", "Rakete", "Vitni", "Andželika",
        "HJUSTON",
        "Asteci", "Tekila", "Talas", "Kartel",
        "MEKSIKO"
    ),
    (
        "ČAJ.CAJ",
        "Mlijeko", "Sjekira", "Tegla", "Mesec",
        "MED",
        "Šef", "Sunđer", "Pločice", "Restoran",
        "KUHINJA",
        "Drška", "Keramika", "Gledanje", "Petri",
        "ŠOLJA.SOLJA",
        "Kriket", "Mumbaj", "Joga", "Čenaj",
        "INDIJA"
    ),
    (
        "RIM",
        "Glas", "Sistem", "Lijek", "Norma",
        "PRAVO",
        "Torba", "Srećan", "Auto", "Osiguranje",
        "PUT",
        "Firenca", "Pasta", "Moda", "Čizma",
        "ITALIJA",
        "Para", "Bojler", "Tuš", "Ogledalo",
        "KUPATILO"
    ),
    (
     "SREBRNA.SREBRNO.SREBRO.SREBRNI",
     "Dunav", "Cigare", "Kutija", "Zdravko Čolić",
     "TABAKERA",
     "Kum", "Muzika", "Ceremonij", "Deveruše",
     "SVADBA",
     "Odličje", "Sport", "Hrabrost", "Grudi",
     "MEDALJA",
     "Anđeo", "Guska", "Avion", "Vrata",
     "KRILA.KRILO"
    ),
    (
     "CIJEV.CEV",
     "Otpad", "Vode", "Pacovi", "Gradska",
     "KANALIZACIJA",
     "Zenica", "Švedska", "Legura", "Gvožđe",
     "ČELIK.CELIK",
     "Šporet", "Upaljač", "Bojler", "Boca",
     "PLIN",
     "Metak", "Maksim", "Gatling", "Šarac",
     "MITRALJEZ.MITRALJEZI"
    ),
    (
     "KOLONA",
     "Motor", "Osiguranje", "Teret", "Pratnja",
     "VOZILO.VOZILA.AUTO.AUTA.AUTOMOBILI.AUTOMOBIL",
     "Bela", "Novine", "Mozaik", "Rešavanje",
     "UKRŠTENICA.UKRSTENICA",
     "Špica", "Džingl", "Obaveštenje", "Program",
     "NAJAVA",
     "Broj", "Odličan", "Element", "Čaj",
     "PET.5.PETICA"
    ),
    (
     "MJERA.MJERE.MERA.MERE",
     "Sunce", "Nerv", "Koordinata", "Loto",
     "SISTEM.SITEMI",
     "Kći", "Novac", "Vojska", "Ocjena",
     "JEDINICA",
     "Fizika", "Pravilo", "Član", "Rupa",
     "ZAKON.ZAKONI",
     "Nauka", "Komisija", "Atletika", "Sparta",
     "DISCIPLINA.DISCIPLINE"
    ),
    (
     "ČUVAR.ČUVARI.CUVAR.CUVARI",
     "Nova Godina", "Prevoz", "Bdenje", "Veštica",
     "NOĆ.NOC",
     "Društvo", "Komarac", "Računar", "Tenis",
     "MREŽA.MREZA",
     "Vodič", "Rasa", "More", "Šetnja",
     "PAS.PSI",
     "Šljunak", "Pesak", "Suncobran", "Ležaljka",
     "PLAŽA.PLAZA"
    ),
    (
     "IRSKA",
     "Crno", "Belo", "Struja", "Talas",
     "MORE",
     "Kola", "Burbon", "Flaša", "Led",
     "VISKI",
     "Ragina Glava", "Pivo", "Pikado", "Kviz",
     "PAB",
     "Krf", "Uskrs", "Reka", "Kipar",
     "OSTRVO.OSTRVA"
    ),
]

cursor.executemany('''
INSERT INTO asocijacije (
    konacno_rjesenje,
    a1, a2, a3, a4, rjesenje_a,
    b1, b2, b3, b4, rjesenje_b,
    c1, c2, c3, c4, rjesenje_c,
    d1, d2, d3, d4, rjesenje_d
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', asocijacije)

conn.commit()

cursor.execute("SELECT COUNT(*) FROM asocijacije")
count = cursor.fetchone()[0]
print(f"Baza uspješno kreirana! Ukupno asocijacija: {count}")

conn.close()
