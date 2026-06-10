import sqlite3

conn = sqlite3.connect('ko_zna_zna.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS pitanja (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pitanje TEXT NOT NULL,
    tacan TEXT NOT NULL,
    netacno1 TEXT NOT NULL,
    netacno2 TEXT NOT NULL,
    netacno3 TEXT NOT NULL
)
''')

pitanja = [
    ("Kada je otkriven penicilin?", "1929.", "1932.", "1956.", "1920."),
    ("Kojeg datuma je dan zaljubljenih?", "14. Februara", "13. Januara", "14. Marta", "9. Juna"),
    ("Ko je napisao dramu 'Antigona'?", "Sofokle", "Homer", "Tukidid", "Euripid"),
    ("Koja država ima najveći broj vremenskih zona?", "Francuska", "Rusija", "SAD", "Kanada"),
    ("Ko je bio prvi čovjek u svemiru?", "Jurij Gagarin", "Alan Shepard", "Baz Aldrin", "Nil Armstrong"),
    ("Koji kontinent ima najviše država?", "Afrika", "Južna Amerika", "Azija", "Evropa"),
    ("Koji je najmanji prost broj?", "2", "1", "3", "0"),
    ("Koji je glavni grad Novog Zelanda?", "Velington", "Okland", "Sidnej", "Melburn"),
    ("Kako se nazivaju bela krvna zrnca?", "Leukociti", "Trombociti", "Limfociti", "Eritrociti"),
    ("Kako se zove poznata igračka oblika kocke?", "Rubikova", "Cezareva", "Rubinova", "Robinova"),
    ("Kada je kapitulacijom Japana završen II svjetski rat?", "2. septembra 1945. godine", "28. juna 1945. godine", "13. maja 1945. godine", "28. septembra 1945. godine"),
    ("Kako se zove lažno zlato?", "Pirit", "Opal", "Ametist", "Topaz"),
    ("Sa koliko vrsta figura se može odigrati prvi potez u šahu?", "2", "1", "4", "3"),
    ("Jedinica za silu je:", "Njutn", "Om", "Bar", "Va"),
    ("Reka Neva protiče kroz:", "Sankt Peterburg", "Bukurešt", "Beč", "Berlin"),
    ("Koliko je film 'Titanik' dobio Oskara?", "11", "3", "17", "9"),
    ("Adoptirati znači:", "Usvojiti", "Pokloniti", "Presuditi", "Preudesiti"),
    ("Koji organ u tijelu proizvodi insulin?", "Pankreas", "Jetra", "Srce", "Želudac"),
    ("Koji proces biljke koriste za stvaranje hrane?", "Fotosinteza", "Fermentacija", "Respiracija", "Oksidacija"),
    ("Koji uređaj mjeri temperaturu?", "Termometar", "Barometar", "Dinamometar", "Ampermetar"),
    ("Pravo ime Dositeja Obradovića?", "Dimitrije", "Milan", "Petar", "Jovan"),
    ("Kako nazivamo oboljevanje velikog broja ljudi od iste bolesti?", "Epidemija", "Grip", "Malarija", "Pandemija"),
    ("Šta je osnovna jedinica života?", "Ćelija", "Atom", "Tkivo", "Organ"),
    ("Koji instrument mjeri jačinu struje?", "Ampermetar", "Voltmetar", "Barometar", "Ohmmetar"),
    ("Koja krvna grupa je univerzalni donor?", "0 (nulta)", "A", "B", "AB"),
    ("Kako se zove planinski lanac u sjeverozapadnoj Africi?", "Atlas", "Šestar", "Tabla", "Okrug"),
    ("Koliko brzo može da trči gepard?", "oko 110 km/h", "oko 90 km/h", "oko 100 km/h", "oko 70 km/h"),
    ("Koliko kostiju ima odraslo ljudsko tijelo?", "206", "186", "216", "256"),
    ("Koja je osnovna jedinica za električni napon?", "Volt", "Vat", "Amper", "Om"),
    ("Koji organ prvo reaguje na alkohol?", "Mozak", "Jetra", "Srce", "Bubrezi"),
    ("Koliko hromozoma ima čovjek?", "46", "43", "23", "48"),
    ("Kolika je visina koša na košarkaškim terenima?", "3,05 m", "3,20 m", "2,80 m", "2,95 m"),
    ("Peloponeski rat se vodio između?", "Atine i Sparte", "Atine i Persije", "Grčke i Makedonije", "Sparte i Persije"),
    ("Ko je izumio telefon?", "Aleksandar Graham Bel", "Nikola Tesla", "Tomas Edison", "Marconi"),
    ("Koji gas je najzastupljeniji u atmosferi?", "Azot", "Kiseonik", "Ugljen-dioksid", "Helijum"),
    ("Koja supstanca je osnova DNK?", "Nukleotidi", "Aminokiseline", "Lipidi", "Glukoza"),
    ("Koji grad u Kini nazivaju 'Las Vegas'?", "Macau", "Peking", "Šangai", "Vuhan"),
    ("Kako se zove operativni sistem koji je razvio Google?", "Android", "Linux", "Simbian", "Windows"),
    ("Prevod latinske izreke 'Amicus certus in re incerta cernitur' je?", "Pravi prijatelj se u nevolji poznaje", "Sreća prati hrabre", "Vrijeme liječi sve rane", "Prijatelj je uvijek potreban"),
    ("Kopakabana je:", "Plaža u Rio de Žaneiru", "Vulkan na Andima", "Južnoamerički ples", "Grad u Brazilu"),
    ("Berlinski zid je simbol:", "Hladnog rata", "Njemačke moći", "Pruskog nacionalizma", "Evropske unije"),
    ("Kad je bila invazija na Panamu?", "20. decembar 1989. godine", "10. decembar 1989. godine", "20. decembar 1987. godine", "1. decembar 1987. godine"),
    ("U kom vijeku je konstruisana prva evropska štamparska mašina?", "15.", "16.", "14.", "13."),
    ("Koja je stara prijestolnica Japana?", "Kjoto", "Osaka", "Tokyo", "Nara"),
    ("Kad je nastala Evropska Unija?", "1. novembra 1993. godine", "10. novembra 1996. godine", "3. novembra 1990. godine", "1. novembra 1990. godine"),
    ("Kojim sportom se bavio Dirk Novicki?", "Košarkom", "Odbojkom", "Tenisom", "Skijanjem"),
    ("Koji grad u SAD ima nadimak 'grad vetrova'?", "Čikago", "Boston", "Detroit", "New York"),
    ("Najjača ruka u pokeru je:", "Rojal fleš", "Triling", "Skala", "Full house"),
    ("Ko je bio Ayrton Senna?", "Vozač F1", "Košarkaš", "Šahista", "Teniser"),
    ("Koliko krvi približno sadrži telo odraslog čovjeka?", "5-6 litara", "2,5-3 litara", "10-12 litara", "6-7 litara"),
    ("Koja je najduža rijeka na svijetu?", "Nil", "Amazon", "Jangce", "Misisipi"),
    ("Ko je bio prvi predsjednik SAD?", "Džordž Vašington", "Tomas Džeferson", "Abraham Linkoln", "Džon Adams"),
    ("Koja je najgušće naseljena zemlja na svijetu (po površini)?", "Monako", "Bangladeš", "Singapur", "Indija"),
    ("Ko je bio poslednji car Rusije?", "Nikolaj II", "Aleksandar III", "Petar Veliki", "Ivan Grozni"),
    ("Šta znači kratica 'WWW'?", "World Wide Web", "World Wide Wire", "Wide World Web", "Web Wide World"),
    ("Ko je osnivač teorije evolucije?", "Čarls Darvin", "Gregor Mendel", "Luis Paster", "Karl Linne"),
    ("U kojoj zemlji je izmišljena čokolada?", "Meksiko", "Belgija", "Švajcarska", "Španija"),
    ("Koja zemlja ima najviše jezera na svijetu?", "Kanada", "Rusija", "Finska", "SAD"),
    ("Koja je najstarija religija na svijetu?", "Hinduizam", "Budizam", "Hrišćanstvo", "Islam"),
    ("Koja je jedina planeta koja se okreće u suprotnom smjeru od ostalih?", "Venera", "Mars", "Uran", "Neptun"),
    ("U kojoj zemlji je izmišljen šah?", "Indija", "Kina", "Persija", "Grčka"),
    ("Koliko srca ima hobotnica?", "3", "1", "2", "5"),
    ("Koja zemlja ima najviše vulkana?", "Indonezija", "Japan", "SAD", "Island"),
    ("Izraelska obavještajna služba zove se:", "Mosad", "Džeruza", "Hanam", "Amana"),
    ("Venov dijagram služi za predstavljanje:", "Skupova", "Znakova", "Brojeva", "Proizvoda"),
    ("Koje godine je pod tursku vlast pao Carigrad?", "1453", "1659", "1341", "1504"),
    ("Ko je napisao knjigu 'Ispod zmajevih krila'?", "Branko Ćopić", "Dobrica Erić", "Dobrica Ćosić", "Miloš Crnjanski"),
    ("Prema Bibliji koliko godina je živio Adam?", "930", "1000", "900", "953"),
    ("Grupa Linkin Park svira koju vrstu muzike?", "Nu metal", "Rock", "Rap", "Tehno"),
    ("Koje godine je poginuo košarkaški as Dražen Petrović?", "1993", "1999", "1995", "1991"),
    ("Kako se zove glavni put groma?", "Lider", "Munja", "Luk", "Strijela"),
    ("Ko se smatra osnivačem sociologije?", "Ogist Kont", "Emil Dirkem", "Maks Veber", "Karl Marks"),
    ("Vodopad Iguasu je na granici:", "Brazila i Argentine", "Brazila i Čilea", "Argentine i Urugvaja", "Perua i Bolivije"),
    ("Čulo ravnoteže kod čovjeka nalazi se u:", "Unutrašnjem uhu", "Malom mozgu", "Velikom mozgu", "Kičmenoj moždini"),
    ("Iz koje zemlje je prvi čovjek koji se popeo na Mont Everest?", "Novi Zeland", "Velika Britanija", "Nepal", "Australija"),
    ("Koliko približno iznosi brzina zvuka u vazduhu?", "oko 340 m/s", "oko 150 m/s", "oko 500 m/s", "oko 1000 m/s"),
    ("Koliko je godina živio Petar II Petrović Njegoš?", "38", "41", "92", "29"),
    ("Ime košarkaškog trenera Žeravice je?", "Ranko", "Darko", "Radivoje", "Radomir"),
    ("Najduža Francuska rijeka je:", "Loara", "Sena", "Rona", "Garona"),
    ("Entoni Hopkins igrao je Hanibala Lektora u filmu:", "Kad jaganjci utihnu", "Vrisak", "Sedam", "Isijavanje"),
    ("Koji tim je rekorder po broju osvojenih NBA titula?", "Boston Celtics", "Los Angeles Lakers", "Chicago Bulls", "Golden State Warriors"),
    ("U kom gradu je rođen Bora Stanković?", "U Vranju", "U Kruševcu", "U Zaječaru", "U Prištini"),
    ("Najosetljivije čulo sluha ima:", "Slijepi miš", "Sova", "Zec", "Delfin"),
    ("Hoang Ho se prevodi kao...?", "Žuta rijeka", "Rijeka smrti", "Bijela rijeka", "Rijeka života"),
    ("Ilegalna rasistička organizacija u SAD zove se:", "Kju Kluks Klan", "Anti negro", "Crni Panteri", "NAACP"),
    ("Košarku je izmislio...?", "Džejms Nejsmit", "Dušan Korać", "Dejvid Štern", "Džoni Meri"),
    ("Kada se pojavio prvi iPhone?", "2007", "2004", "2009", "2006"),
    ("Riječ 'katarakta' u grčkom jeziku označava?", "Vodopad", "Glečer", "Ostrvo", "Zamućenje"),
    ("Šta u prevodu znači titula 'dalaj lama'?", "Okean mudrosti", "Duhovni vođa", "Mudra glava", "Poglavica duhova"),
    ("Fudbalski derbi Liverpula igraju: Liverpul i ...", "Everton", "Arsenal", "West Ham", "Totenhem"),
    ("Koji pojam nije politička teorija?", "Šovinizam", "Liberalizam", "Konzervatizam", "Socijalizam"),
    ("Kad se desilo samoubistvo Hitlera i Eve Braun?", "1945", "1946", "1947", "1944"),
    ("Ko nije mačak?", "Duško Dugouško", "Tom", "Garfild", "Silvester"),
    ("Automobilska marka Škoda porijeklom je iz?", "Češke", "Njemačke", "Austrije", "SAD"),
    ("Adolescencija je:", "Mladalačko doba", "Zrelo doba", "Period detinjstva", "Starost"),
    ("Koliko ima moćnih rendžera?", "6", "4", "8", "5"),
    ("Kad su održane prve zimske Olimpijske igre?", "1924", "1940", "1932", "1929"),
    ("Ptica feniks je simbol:", "Besmrtnosti", "Mudrosti", "Pustošenja", "Smrti"),
    ("Kad je umro Elvis Prisli?", "1977. godine", "1969. godine", "1983. godine", "1990. godine"),
    ("Ko pjeva pjesmu 'Alal vera'?", "Beogradski sindikat", "Riblja Čorba", "Psihoaktiv trip", "Ana Nikolić"),
]

cursor.executemany('''
INSERT INTO pitanja (pitanje, tacan, netacno1, netacno2, netacno3)
VALUES (?, ?, ?, ?, ?)
''', pitanja)

conn.commit()

# Provjera
cursor.execute("SELECT COUNT(*) FROM pitanja")
count = cursor.fetchone()[0]
print(f"Baza uspješno kreirana! Ukupno pitanja: {count}")

conn.close()