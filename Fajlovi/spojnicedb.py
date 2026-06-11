import sqlite3

conn = sqlite3.connect("spojnice.db")
cursor = conn.cursor()

#Kreiranje tabele
cursor.execute("""
CREATE TABLE IF NOT EXISTS spojnice (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tema TEXT NOT NULL,

    pojam_1 TEXT, odgovor_1 TEXT,
    pojam_2 TEXT, odgovor_2 TEXT,
    pojam_3 TEXT, odgovor_3 TEXT,
    pojam_4 TEXT, odgovor_4 TEXT,
    pojam_5 TEXT, odgovor_5 TEXT,
    pojam_6 TEXT, odgovor_6 TEXT,
    pojam_7 TEXT, odgovor_7 TEXT,
    pojam_8 TEXT, odgovor_8 TEXT
)
""")

#Podaci za unos
spojnice = [
    (
        "Spojite 8 najvećih država na svijetu sa njihovim površinama (km2):",

        "2.766.890", "Argentina",
        "9.598.077", "Kina",
        "3.287.590", "Indija",
        "17.075.200", "Rusija",
        "8.511.965", "Brazil",
        "7.687.453", "Australija",
        "9.639.810", "SAD",
        "9.976.140", "Kanada"
    ),

    (
        "Spojite staze formule 1 i države u kojima se nalaze:",

        "Sepang", "Malezija",
        "Monca", "Italija",
        "Herez", "Spanija",
        "Jas Marina", "Abu Dabi",
        "Interlagos", "Brazil",
        "Silverston", "Velika Britanija",
        "Suzuka", "Japan",
        "Šakir", "Bahrein"
    ),
    
    (
        "Spojite pjevače i njihove pjesme:",

        "U škripcu", "Kockar",
        "Zabranjeno pušenje", "Zenica bluz",
        "Zdravko Čolić", "April u Beogradu",
        "Električni Orgazam", "Nebo",
        "Šarlo Akrobata", "Zlatni papagaj",
        "Parni valjak", "Zagreb ima isti pozivni",
        "Galija", "Kotor",
        "Riblja Čorba", "Amsterdam"
    ),
    
    (
        "Spojite vojskovođe i bitke koje su izgubili:",

        "Robert Li", "Bitka kod Getizburga",
        "Marko Antonije", "Bitka kod Akcija",
        "Isoroku Jamamoto", "Bitka kod Midveja",
        "Kserks I", "Bitka kod Salamine",
        "Bajazit I", "Bitka kod Angore",
        "Napoleon", "Bitka kod Lajpciga",
        "Vukašin Mrnjavčević", "Marička bitka",
        "Oskar Poćorek", "Kolubarska bitka"
    ),
    
    (
        "Spojite glavne gradove:",

        "Beograd", "Srbija",
        "Minsk", "Belorusija",
        "Kijev", "Ukrajina",
        "Nikozija", "Kipar",
        "Talin", "Estonija",
        "Riga", "Letonija",
        "Dablin", "Irska",
        "Tbilisi", "Gruzija"
    ),
    
    (
        "Spojite planete u Sunčevom sistemu sa njihovim :",

        "Merkur", "Najbliža Suncu",
        "Venera", "Jutarnja zvijezda",
        "Zemlja", "Plava planeta",
        "Mars", "Crvena planeta",
        "Jupiter", "Najveća planeta",
        "Saturn", "Prstenovi",
        "Uran", "Ledeni džin",
        "Neptun", "Najudaljenija planeta"
    ),
    
    (
        "Spojite rimske brojeve sa njihovim vrijednostima:",

        "555", "DLV",
        "1010", "MX",
        "88", "LXXXVIII",
        "997", "CMXCVII",
        "2008", "MMVIII",
        "1111", "MCXI",
        "2222", "MMCCXXII",
        "3333", "MMMCCCXXXIII"
    ),
    
    (
        "Spojite 'Volim te' na evropskim jezicima:",

        "Te quiero", "španski",
        "Ich liebe dich", "njemački",
        "S'ayapo", "grčki",
        "I love you", "engleski",
        "Je t' aime", "franckuski",
        "Ti amo", "italijanski",
        "Eu te amo", "portugalski",
        "Te iubesc", "rumunski"
    ),
    
    (
        "Spojite pjevače i njihove pjesme:",

        "Parni valjak", "Sve još miriše na nju",
        "Plavi orkestar", "Suada",
        "Magazin", "Minus i plus",
        "Crvena jabuka", "Dirlija",
        "Zana", "Vejte snegovi",
        "Idoli", "Malena",
        "Riblja čorba", "Dva dinara druže",
        "U škripcu", "Siđi do reke"
    ),
    
    (
        "Spojite američke države i gradove:",

        "California", "Los Angeles",
        "Ilinois", "Chicago",
        "Florida", "Miami",
        "Colorado", "Denver",
        "Arizona", "Phoenix",
        "Minnesota", "Minneapolis",
        "Texas", "Houston",
        "Oregon", "Portland"
    ),
    
    (
        "Spojite znamenitosti sa gradovima u kojima se nalaze:",

        "Kip Slobode", "Njujork",
        "Karlov Most", "Prag",
        "Crveni trg", "Moskva",
        "Big Ben", "London",
        "Ajfelova kula", "Pariz",
        "Keopsova piramida", "Kairo",
        "Tadž Mahal", "Agra",
        "Krivi Toranj", "Piza"
    ),
    
    (
        "Spojite države i valute:",

        "Japan", "Jen",
        "Švajcarska", "Franak",
        "Velika Britanija", "Funta",
        "Indija", "Rupija",
        "Turska", "Lira",
        "Poljska", "Zlot",
        "Mađarska", "Forinta",
        "Švedska", "Kruna"
    ),
    
    (
        "Spojite knjige i autori:",

        "Na Drini ćuprija", "Ivo Andrić",
        "Rat i mir", "Lav Tolstoj",
        "Zločin i kazna", "Fjodor Dostojevski",
        "Don Kihot", "Migel de Servantes",
        "1984", "Džordž Orvel",
        "Hamlet", "Vilijam Šekspir",
        "Mali princ", "Antoan de Sent Egziperi",
        "Proces", "Franc Kafka"
    ),
    
    (
        "Spojite likove i igre iz kojih dolaze:",

        "Master Chief", "Halo",
        "Geralt od Rivije", "The Witcher",
        "Kratos", "God of War",
        "Arthur Morgan", "Red Dead Redemption 2",
        "Lara Croft", "Tomb Raider",
        "Solid Snake", "Metal Gear Solid",
        "Carl Johnson CJ", "GTA San Andreas",
        "Twitch", "Leauge of Legends"
    ),
    
    (
        "Spojite likove i animee iz kojih dolaze:",

        "Naruto Uzumaki", "Naruto",
        "Monkey D. Luffy", "One Piece",
        "Ichigo Kurosaki", "Bleach",
        "Eren Yeager", "Attack on Titan",
        "Light Yagami", "Death Note",
        "Tanjiro Kamado", "Demon Slayer",
        "07", "Darling in the Franxx",
        "Yuji Itadori", "Jujutsu Kaisen"
    ),
    
    (
        "Spojite likove i serije iz kojih dolaze:",

        "Walter White", "Breaking Bad",
        "Rustin Cohle", "True detective",
        "Dexter Morgan", "Dexter",
        "Rick Grimes", "The Walking Dead",
        "Saul Goodman", "Better Call Saul",
        "Michael Scott", "The Office",
        "Tommy Shelby", "Peaky Blinders",
        "Eleven", "Stranger Things"
    ),
    
    (
        "Spojite simbole i države koje ih koriste:",

        "Javorov list", "Kanada",
        "Cedrovo drvo", "Liban",
        "Dvoglavi orao", "Srbija",
        "Lav", "Holandija",
        "Sunce", "Japan",
        "Zmaj", "Butan",
        "Kornjača", "Sejšeli",
        "Pero", "Novi Zeland"
    ),
    
    (
        "Spojite tehnologije i kompanije:",

        "iPhone", "Apple",
        "Windows", "Microsoft",
        "Android", "Google",
        "PlayStation", "Sony",
        "Linux", "Linus Torvalds",
        "Facebook", "Meta",
        "Tesla automobil", "Tesla Inc.",
        "ChatGPT", "OpenAI"
    ),
    
    (
        "Spojite igre i najpoznatije mape/lokacije:",

        "CS:GO", "Dust II",
        "Valorant", "Haven",
        "Minecraft", "Nether",
        "GTA V", "Los Santos",
        "Fortnite", "Tilted Towers",
        "League of Legends", "Summoner's Rift",
        "PUBG", "Erangel",
        "Call of Duty", "Nuketown"
    ),
    
    (
        "Spojite bendove i države porijekla:",

        "ABBA", "Švedska",
        "Rammstein", "Njemačka",
        "The Beatles", "Engleska",
        "AC/DC", "Australija",
        "Metallica", "SAD",
        "Daft Punk", "Francuska",
        "BTS", "Južna Koreja",
        "Mayhem", "Norveška"
    ),
    
    (
        "Spojite Gaming termine i njihovo značenje:",

        "Respawn", "Ponovno pojavljivanje",
        "Lag", "Kašnjenje",
        "Buff", "Pojačanje",
        "Nerf", "Slabljenje",
        "Loot", "Plijen",
        "Final Boss", "Glavni neprijatelj",
        "Grind", "Dugo igranje",
        "Camp", "Čekanje na jednom mjestu"
    ),
    
    (
        "Spojite automobile i proizvođače:",

        "Golf", "Volkswagen",
        "Mustang", "Ford",
        "Civic", "Honda",
        "Supra", "Toyota",
        "Model S", "Tesla",
        "911", "Porsche",
        "A3", "Audi",
        "C-Class", "Mercedes-Benz"
    ),
    
    (
        "Spojite marke auta i države iz kojih potiču:",

        "Alfa Romeo", "Italija",
        "Dacia", "Rumunija",
        "Škoda", "Češka",
        "Jeep", "SAD",
        "Saab", "Švedska",
        "Subaru", "Japan",
        "Renault", "Francuska",
        "Opel", "Njemačka",
    ),
    
    (
        "Povežite gradove na slovo L sa državama u kojima se nalaze:",

        "Leskovac", "Srbija",
        "Larisa", "Grčka",
        "Lavov", "Ukrajina",
        "Livno", "BiH",
        "Lanjang", "Kina",
        "Liverpul", "Engleska",
        "Lugano", "Švajcarska",
        "Lisabon", "Portugalija"
    ),
    
    (
        "Spojite imena i prezimena domaćih glumaca:",

        "Danilo Bata", "Stojković",
        "Nikola", "Kojo",
        "Dragan", "Bjelogrlić",
        "Sergej", "Trifunović",
        "Nebojša", "Glogovac",
        "Dragan", "Nikolić",
        "Lazar", "Ristovski",
        "Srđan", "Todorović"
    ),
    
    (
        "Spojite popularne američke repere sa njihovim albumima:",

        "Drake", "Views",
        "Kendrick Lamar", "To Pimp A Butterfly",
        "A$AP Rocky", "Live Love A$AP",
        "Don Toliver", "Hardstone Psycho",
        "Future", "DS2",
        "Playboi Carti", "Whole Lotta Red",
        "Travis Scott", "Astroworld",
        "J Cole", "4 Your Eyez Only"
    ),
    

]

cursor.executemany("""
INSERT INTO spojnice (
    tema,

    pojam_1, odgovor_1,
    pojam_2, odgovor_2,
    pojam_3, odgovor_3,
    pojam_4, odgovor_4,
    pojam_5, odgovor_5,
    pojam_6, odgovor_6,
    pojam_7, odgovor_7,
    pojam_8, odgovor_8
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", spojnice)

conn.commit()

cursor.execute("SELECT COUNT(*) FROM spojnice")
broj = cursor.fetchone()[0]

print(f"Ukupno spojnica: {broj}")

conn.close() 