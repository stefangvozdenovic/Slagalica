""" SLAGALICA
=====================================
Klase:
  - Slagalica    : sva logika igre slova (abeceda, težine, rječnik, highscore, unos, provjera)
  - MojBroj      : logika igre brojeva (odabir, izraz, evaluacija, solver, bodovanje)
  - Skocko       : Logika igre kombinacije (dobitna kombinacija, bodovanje)
  - Ko zna zna   : Logika igre kviza (izbor pitanja, odgovori, shuffle)
  - Spojnice     : Logika igre Spojnice (izbor teme spojnice, shuffle, povezivanje odgovora sa pojmom)
  - Igra         : praćenje bodova
  - MainScreen   : početni ekran, highscore, navigacija
  - SlagalicaApp : glavni GUI, orkestrator ekrana"""

import tkinter as tk
from tkinter import font as tkfont
import random
import os
import itertools
import operator
import threading

try:
    from docx import Document as DocxDocument
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

# ─────────────────────────────────────────────
#  Globalne konstante izgleda
# ─────────────────────────────────────────────
BG_TAMNA        = "#0A0E1A"
BG_PANEL        = "#111827"
BG_KARTICA      = "#1E2A3A"
ZLATNA          = "#F5C518"
ZLATNA_TAMNA    = "#C9A30E"
BIJELA          = "#F0F4FF"
SIVA_SVIJETLA   = "#8899AA"
ZELENA          = "#22C55E"
CRVENA          = "#EF4444"
PLAVA_AKCENT    = "#3B82F6"
FIKSIRANO_BG    = "#1A3A5C"
FIKSIRANO_FG    = "#7DD3FC"
BTN_POTVRDI_BG  = "#2563EB"
BTN_POTVRDI_HOV = "#1D4ED8"
BTN_OBRISI_BG   = "#6B2D2D"
NARANCASTA      = "#F97316"

# ─────────────────────────────────────────────
#  Klasa  MAIN SCREEN
# ─────────────────────────────────────────────
class MainScreen:
    def __init__(self, parent_frame: tk.Frame, highscore: int,
                 on_igraj, on_izlaz,
                 f_bodovi, f_gumb, f_maly, f_status):
        self.frame     = tk.Frame(parent_frame, bg=BG_TAMNA)
        self.highscore = highscore
        self.on_igraj  = on_igraj
        self.on_izlaz  = on_izlaz
        self._build(f_bodovi, f_gumb, f_maly, f_status)

    def _build(self, f_bodovi, f_gumb, f_maly, f_status):
        center = tk.Frame(self.frame, bg=BG_TAMNA)
        center.place(relx=0.5, rely=0.5, anchor="center")

        hs_frame = tk.Frame(center, bg=BG_PANEL, padx=60, pady=20)
        hs_frame.pack(pady=(0, 40))

        tk.Label(hs_frame, text="HIGHSCORE",
                 bg=BG_PANEL, fg=SIVA_SVIJETLA,
                 font=f_maly).pack()

        self.lbl_hs = tk.Label(hs_frame, text=str(self.highscore),
                               bg=BG_PANEL, fg=ZLATNA,
                               font=f_bodovi)
        self.lbl_hs.pack()

        btn_frame = tk.Frame(center, bg=BG_TAMNA)
        btn_frame.pack()

        tk.Button(
            btn_frame, text="▶  IGRAJ",
            command=self.on_igraj,
            bg="#16A34A", fg=BIJELA,
            activebackground="#15803D", activeforeground=BIJELA,
            font=f_gumb, relief="flat", bd=0,
            cursor="hand2", padx=60, pady=18
        ).pack(side="left", padx=16)

        tk.Button(
            btn_frame, text="✕  IZLAZ",
            command=self.on_izlaz,
            bg="#374151", fg=BIJELA,
            activebackground="#1F2937", activeforeground=BIJELA,
            font=f_gumb, relief="flat", bd=0,
            cursor="hand2", padx=40, pady=18
        ).pack(side="left", padx=16)

    def azuriraj_highscore(self, novi: int):
        self.highscore = novi
        self.lbl_hs.config(text=str(novi))

    def show(self):
        self.frame.place(relx=0, rely=0.08, relwidth=1, relheight=0.92)

    def hide(self):
        self.frame.place_forget()

# ─────────────────────────────────────────────
#  Klasa  IGRA
# ─────────────────────────────────────────────
class Igra:
    def __init__(self):
        self.bodovi: int  = 0
    
    def dodaj_bodove(self, bodovi: int):
        self.bodovi += bodovi

    def reset(self):
        self.bodovi = 0

# ─────────────────────────────────────────────
#  Klasa  SLAGALICA
# ─────────────────────────────────────────────
class Slagalica:

    def __init__(self, rjecnik: set):
        self.AZBUKA = [
            'A', 'B', 'C', 'Č', 'Ć', 'D', 'Dž', 'Đ', 'E', 'F',
            'G', 'H', 'I', 'J', 'K', 'L', 'Lj', 'M', 'N', 'Nj',
            'O', 'P', 'R', 'S', 'Š', 'T', 'U', 'V', 'Z', 'Ž'
        ]
        self.SAMOGLASNICI = {'A', 'E', 'I', 'O', 'U'}
        self.RIJETKA      = {'Dž', 'Đ', 'Lj', 'Nj', 'Ć', 'Ž', 'F'}
        self.TEZINE       = [self._tezina(s) for s in self.AZBUKA]

        self.rjecnik:            set  = rjecnik
        self.fiksirana_slova:    list = [None] * 12
        self.unos:               list = []
        self.odabrana_slova:     list = []
        self._animacija_aktivna: bool = False
        self.animacija_slova:    list = self._random_slova()

    def _tezina(self, slovo: str) -> float:
        if slovo in self.SAMOGLASNICI:
            return 10.0
        elif slovo in self.RIJETKA:
            return 1.5
        return 5

    def _random_slova(self, k: int = 12) -> list:
        return random.choices(self.AZBUKA, weights=self.TEZINE, k=k)

    def random_jedno(self) -> str:
        return random.choices(self.AZBUKA, weights=self.TEZINE, k=1)[0]

    def fiksiraj_slovo(self, index: int):
        if self.fiksirana_slova[index] is not None:
            return None
        slovo = self.animacija_slova[index]
        self.fiksirana_slova[index] = slovo
        self.odabrana_slova.append(slovo)
        return slovo

    def sva_fiksirana(self) -> bool:
        return all(s is not None for s in self.fiksirana_slova)

    def dodaj_slovo_u_unos(self, slovo: str) -> bool:
        dostupna = list(self.odabrana_slova)
        za_provjeru = self.unos + [slovo]
        for s in za_provjeru:
            if s in dostupna:
                dostupna.remove(s)
            else:
                return False
        self.unos.append(slovo)
        return True

    def obrisi_zadnje(self):
        if self.unos:
            self.unos.pop()

    def ocisti_unos(self):
        self.unos = []

    def provjeri_unos(self) -> bool:
        return "".join(self.unos).upper() in self.rjecnik

    def provjeri_rijec(self, rijec: str) -> bool:
        return rijec.upper() in self.rjecnik

    @staticmethod
    def ucitaj_rjecnik(putanja: str) -> set:
        rijeci = set()
        if not putanja or not os.path.exists(putanja):
            return rijeci
        try:
            if DOCX_AVAILABLE and putanja.lower().endswith('.docx'):
                doc = DocxDocument(putanja)
                for para in doc.paragraphs:
                    word = para.text.strip().upper()
                    if word:
                        rijeci.add(word)
            else:
                with open(putanja, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        word = line.strip().upper()
                        if word:
                            rijeci.add(word)
        except Exception as e:
            print(f"Greška pri čitanju rječnika: {e}")
        return rijeci

    @staticmethod
    def ucitaj_highscore(putanja: str) -> int:
        if not putanja or not os.path.exists(putanja):
            return 0
        try:
            with open(putanja, 'r', encoding='utf-8') as f:
                return int(f.read().strip())
        except Exception:
            return 0

    @staticmethod
    def spremi_highscore(putanja: str, bodovi: int):
        try:
            os.makedirs(os.path.dirname(putanja), exist_ok=True)
            with open(putanja, 'w', encoding='utf-8') as f:
                f.write(str(bodovi))
        except Exception as e:
            print(f"Greška pri spremanju highscore-a: {e}")

    def reset(self):
        self.fiksirana_slova    = [None] * 12
        self.odabrana_slova     = []
        self.unos               = []
        self.animacija_slova    = self._random_slova()
        self._animacija_aktivna = False
        
    def potvrdi_rijec(self, rijec_lista: list) -> int:
        rijec_str = "".join(rijec_lista)
        if self.provjeri_rijec(rijec_str):
            zaradjeno = len(rijec_lista) * 2
            return zaradjeno
        return 0


# ─────────────────────────────────────────────
#  Klasa  MOJ BROJ
# ─────────────────────────────────────────────
class MojBroj:
    MALI_BROJEVI    = list(range(1, 10))
    SREDNJI_BROJEVI = [10, 15, 20]
    VELIKI_BROJEVI  = [25, 50, 75, 100]
    OPS             = [operator.add, operator.sub, operator.mul, operator.truediv]
    OP_SIMBOLI      = ['+', '-', '*', '/']

    def __init__(self):
        # 6 slotova: indeksi 0-3 = mali, 4 = srednji, 5 = veliki
        self.odabrani_brojevi: list = [0] * 6
        self.potroseni: list = [False] * 6

        self.ciljni_broj: int = 0
        self.cilj_fiksiran: bool = False

        self.tokeni: list = []
        self.token_indeksi: list = []

        self.najblizi_rezultat: int | None = None
        self.najblizi_izraz: str | None = None   # NOVO: izraz računara
        self.solver_gotov: bool = False
        self._solver_thread: threading.Thread | None = None

        # animacija — svaki od 6 slotova
        self.animacija_vrijednosti: list = [
            random.randint(1, 9),   # mali 0
            random.randint(1, 9),   # mali 1
            random.randint(1, 9),   # mali 2
            random.randint(1, 9),   # mali 3
            random.choice(self.SREDNJI_BROJEVI),  # srednji
            random.choice(self.VELIKI_BROJEVI),   # veliki
        ]
        self.animacija_cilj: int = random.randint(1, 999)

        # Je li svaki slot fikisan
        self.fiksirani: list = [False] * 6
        self.svi_fiksirani: bool = False

    # ── Tip slota ────────────────────────────────────────────────
    def _novi_random(self, slot: int) -> int:
        if slot < 4:
            return random.randint(1, 9)
        elif slot == 4:
            return random.choice(self.SREDNJI_BROJEVI)
        else:
            return random.choice(self.VELIKI_BROJEVI)

    # ── Fiksiraj ────────────────────────────────────────────────
    def fiksiraj_slot(self, slot: int) -> int | None:
        if self.fiksirani[slot]:
            return None
        val = self.animacija_vrijednosti[slot]
        self.fiksirani[slot] = True
        self.odabrani_brojevi[slot] = val
        self.potroseni[slot] = False
        if all(self.fiksirani):
            self.svi_fiksirani = True
            self._pokreni_solver()
        return val

    def fiksiraj_cilj(self) -> int:
        self.ciljni_broj = self.animacija_cilj
        self.cilj_fiksiran = True
        if self.svi_fiksirani:
            self._pokreni_solver()
        return self.ciljni_broj

    # ── Unos izraza ─────────────────────────────────────────────
    def zadnji_token(self) -> str | None:
        return self.tokeni[-1] if self.tokeni else None

    def zadnji_je_operator(self) -> bool:
        return self.zadnji_token() in ('+', '-', '*', '/')

    def zadnji_je_otvorena_zagrada(self) -> bool:
        return self.zadnji_token() == '('

    def zadnji_je_zatvorena_zagrada(self) -> bool:
        return self.zadnji_token() == ')'

    def zadnji_je_broj(self) -> bool:
        t = self.zadnji_token()
        if t is None:
            return False
        try:
            int(t)
            return True
        except (ValueError, TypeError):
            return False

    def broj_otvorenih_zagrada(self) -> int:
        return self.tokeni.count('(') - self.tokeni.count(')')

    def dodaj_broj(self, broj_idx: int) -> bool:
        if self.potroseni[broj_idx]:
            return False
        t = self.zadnji_token()
        if t is not None and (self.zadnji_je_broj() or self.zadnji_je_zatvorena_zagrada()):
            return False
        val = str(self.odabrani_brojevi[broj_idx])
        self.tokeni.append(val)
        self.token_indeksi.append(broj_idx)
        self.potroseni[broj_idx] = True
        return True

    def dodaj_operator(self, op: str) -> bool:
        if self.zadnji_je_operator():
            return False
        t = self.zadnji_token()
        if t is None or t == '(':
            return False
        self.tokeni.append(op)
        self.token_indeksi.append(None)
        return True

    def dodaj_otvorenu_zagradu(self) -> bool:
        t = self.zadnji_token()
        if t is not None and (self.zadnji_je_broj() or self.zadnji_je_zatvorena_zagrada()):
            return False
        self.tokeni.append('(')
        self.token_indeksi.append(None)
        return True

    def dodaj_zatvorenu_zagradu(self) -> bool:
        if self.broj_otvorenih_zagrada() <= 0:
            return False
        if not (self.zadnji_je_broj() or self.zadnji_je_zatvorena_zagrada()):
            return False
        self.tokeni.append(')')
        self.token_indeksi.append(None)
        return True

    def obrisi_zadnji(self) -> int | None:
        if not self.tokeni:
            return None
        self.tokeni.pop()
        idx = self.token_indeksi.pop()
        if idx is not None:
            self.potroseni[idx] = False
        return idx

    def ocisti_izraz(self):
        self.tokeni.clear()
        self.token_indeksi.clear()
        for i in range(len(self.potroseni)):
            self.potroseni[i] = False

    def izraz_string(self) -> str:
        return " ".join(self.tokeni)

    # ── Evaluacija ──────────────────────────────────────────────
    def evaluiraj_izraz(self) -> int | None:
        if not self.tokeni:
            return None
        if self.broj_otvorenih_zagrada() != 0:
            return None
        if self.zadnji_je_operator():
            return None
        expr = "".join(self.tokeni)
        try:
            result = eval(expr, {"__builtins__": {}})
            if not isinstance(result, (int, float)):
                return None
            if isinstance(result, float):
                if not result.is_integer():
                    return None
                result = int(result)
            if result < 0:
                return None
            return result
        except Exception:
            return None

    # ── Solver ──────────────────────────────────────────────────
    def _pokreni_solver(self):
        if not self.cilj_fiksiran or not self.svi_fiksirani:
            return
        self.solver_gotov = False
        self.najblizi_rezultat = None
        self.najblizi_izraz = None
        t = threading.Thread(target=self._solver_worker, daemon=True)
        self._solver_thread = t
        t.start()

    def _solver_worker(self):
        brojevi = self.odabrani_brojevi[:]
        cilj    = self.ciljni_broj
        best    = None
        best_d  = float('inf')
        best_expr = None

        ops      = [operator.add, operator.sub, operator.mul, operator.truediv]
        op_syms  = {operator.add: '+', operator.sub: '-',
                    operator.mul: '*', operator.truediv: '/'}

        for r in range(1, len(brojevi) + 1):
            for combo in itertools.combinations(range(len(brojevi)), r):
                perm_nums = [brojevi[i] for i in combo]
                for perm in itertools.permutations(perm_nums):
                    for ops_combo in itertools.product(ops, repeat=r - 1):
                        results = self._evalutaj_kombos(list(perm), list(ops_combo), op_syms)
                        for res, expr in results:
                            if res is None:
                                continue
                            d = abs(res - cilj)
                            if d < best_d or (d == best_d and best is None):
                                best_d    = d
                                best      = res
                                best_expr = expr
                            if best_d == 0:
                                break
                    if best_d == 0:
                        break
                if best_d == 0:
                    break
            if best_d == 0:
                break

        self.najblizi_rezultat = best
        self.najblizi_izraz    = best_expr
        self.solver_gotov      = True

    def _evalutaj_kombos(self, nums: list, ops_list: list, op_syms: dict) -> list:
        if len(nums) == 1:
            return [(nums[0], str(nums[0]))]
        results = []
        try:
            val  = nums[0]
            expr = str(nums[0])
            for i, op in enumerate(ops_list):
                b = nums[i + 1]
                sym = op_syms[op]
                if op == operator.truediv:
                    if b == 0 or val % b != 0:
                        val = None
                        break
                val  = op(val, b) if val is not None else None
                expr = f"({expr} {sym} {b})"
            if val is not None and isinstance(val, (int, float)):
                if isinstance(val, float) and val.is_integer():
                    val = int(val)
                if isinstance(val, int) and val > 0:
                    results.append((val, expr))
        except Exception:
            pass
        return results

    # ── Bodovanje ────────────────────────────────────────────────
    def izracunaj_bodove(self, korisnikov_rezultat: int | None) -> int:
        if korisnikov_rezultat is None:
            return 0
        cilj = self.ciljni_broj
        if korisnikov_rezultat == 0:
            return 0
        racunar = self.najblizi_rezultat
        if racunar is None:
            racunar = cilj
        razlika_korisnik = abs(korisnikov_rezultat - cilj)
        razlika_racunar  = abs(racunar - cilj)
        if razlika_korisnik > razlika_racunar and razlika_korisnik > 5:
            return 0
        if razlika_korisnik == 0:
            return 20
        elif razlika_korisnik == 1:
            return 15
        elif razlika_korisnik == 2:
            return 10
        elif razlika_korisnik <= 5:
            return 5
        else:
            return 0

    def reset(self):
        self.odabrani_brojevi.clear()
        self.potroseni.clear()
        self.tokeni.clear()
        self.token_indeksi.clear()
        self.ciljni_broj       = 0
        self.cilj_fiksiran     = False
        self.najblizi_rezultat = None
        self.najblizi_izraz    = None
        self.solver_gotov      = False
        self.svi_fiksirani     = False
        self.fiksirani         = [False] * 6
        self.animacija_vrijednosti = [
            random.randint(1, 9),
            random.randint(1, 9),
            random.randint(1, 9),
            random.randint(1, 9),
            random.choice(self.SREDNJI_BROJEVI),
            random.choice(self.VELIKI_BROJEVI),
        ]
        self.animacija_cilj = random.randint(1, 999)

# ─────────────────────────────────────────────
#  Klasa  SKOCKO
# ─────────────────────────────────────────────
class Skocko:
    ZNAKOVI = ['skocko', 'tref', 'pik', 'herc', 'karo', 'zvijezda']
    MAX_POKUSAJA = 6
    DUZINA = 4
 
    def __init__(self):
        self.kombinacija: list = self._generiraj_kombinaciju()
        self.pokusaji: list    = []          # lista lista (svaki pokusaj = 4 znaka)
        self.trenutni_unos: list = []
        self.gotovo: bool      = False
        self.pobjeda: bool     = False
 
    def _generiraj_kombinaciju(self) -> list:
        while True:
            kombinacija = [random.choice(self.ZNAKOVI) for _ in range(self.DUZINA)]
            # ne smiju sva četiri biti ista
            if len(set(kombinacija)) == 1:
                continue
            return kombinacija
 
    def dodaj_znak(self, znak: str) -> bool:
        if len(self.trenutni_unos) >= self.DUZINA:
            return False
        self.trenutni_unos.append(znak)
        return True
 
    def obrisi_zadnji(self):
        if self.trenutni_unos:
            self.trenutni_unos.pop()
 
    def unos_potpun(self) -> bool:
        return len(self.trenutni_unos) == self.DUZINA
 
    def potvrdi_pokusaj(self) -> list:
        """
        Vraća listu od 4 boje: 'crvena', 'zuta', ili None (ne postoji).
        Redoslijed: prvo crveni, zatim žuti, zatim None.
        """
        if not self.unos_potpun():
            return []
 
        unos    = list(self.trenutni_unos)
        cilj    = list(self.kombinacija)
        rezultat = [None] * self.DUZINA
 
        # Prolaz 1: tačne pozicije (crvena)
        preostali_cilj  = []
        preostali_unos  = []
        for i in range(self.DUZINA):
            if unos[i] == cilj[i]:
                rezultat[i] = 'crvena'
            else:
                preostali_cilj.append(cilj[i])
                preostali_unos.append((i, unos[i]))
 
        # Prolaz 2: pogrešna pozicija (žuta)
        for (idx, znak) in preostali_unos:
            if znak in preostali_cilj:
                rezultat[idx] = 'zuta'
                preostali_cilj.remove(znak)
 
        # Sortiraj: crveni, žuti, None
        sortirani = (
            [r for r in rezultat if r == 'crvena'] +
            [r for r in rezultat if r == 'zuta']   +
            [r for r in rezultat if r is None]
        )
 
        self.pokusaji.append(list(unos))
        self.trenutni_unos = []
 
        if all(r == 'crvena' for r in sortirani):
            self.gotovo  = True
            self.pobjeda = True
        elif len(self.pokusaji) >= self.MAX_POKUSAJA:
            self.gotovo = True
 
        return sortirani
 
    def bodovi_za_pokusaj(self) -> int:
        """Vraća bodove na osnovu rednog broja pokusaja kojim je pogodjena kombinacija."""
        n = len(self.pokusaji)
        if n == self.MAX_POKUSAJA:       # 6. pokusaj
            return 10
        elif n == self.MAX_POKUSAJA - 1:  # 5. pokusaj
            return 15
        else:
            return 20
 
    def reset(self):
        self.kombinacija     = self._generiraj_kombinaciju()
        self.pokusaji        = []
        self.trenutni_unos   = []
        self.gotovo          = False
        self.pobjeda         = False

# ─────────────────────────────────────────────
#  Klasa  KO ZNA ZNA
# ─────────────────────────────────────────────
import sqlite3

class KoZnaZna:

    def __init__(self, putanja_db: str):
        self.BODOVI_TACAN  =  6
        self.BODOVI_GRESKA = -3
        self.BODOVI_SKIP   =  0
        self.BROJ_PITANJA  = 10
        
        self.putanja_db = putanja_db
        self.pitanja:    list = []
        self.trenutni_idx: int = 0
        self.bodovi: int = 0
        self._ucitaj_pitanja()

    def _ucitaj_pitanja(self):
        self.pitanja = []
        try:
            conn = sqlite3.connect(self.putanja_db)
            cur  = conn.cursor()
            cur.execute("SELECT pitanje, tacan, netacno1, netacno2, netacno3 FROM pitanja ORDER BY RANDOM() LIMIT ?",
                        (self.BROJ_PITANJA,))
            redovi = cur.fetchall()
            conn.close()
        except Exception as e:
            print(f"Greška pri čitanju baze: {e}")
            redovi = []

        for red in redovi:
            pitanje, tacan, n1, n2, n3 = red
            odgovori = [tacan, n1, n2, n3]
            random.shuffle(odgovori)
            self.pitanja.append({
                "pitanje":  pitanje,
                "odgovori": odgovori,
                "tacan":    tacan,
            })

    def trenutno_pitanje(self) -> dict | None:
        if self.trenutni_idx < len(self.pitanja):
            return self.pitanja[self.trenutni_idx]
        return None

    def odgovori(self, odgovor: str) -> int:
        pit = self.trenutno_pitanje()
        if pit is None:
            return 0
        if odgovor == pit["tacan"]:
            zaradjeno = self.BODOVI_TACAN
        else:
            zaradjeno = self.BODOVI_GRESKA
        self.bodovi += zaradjeno
        self.trenutni_idx += 1
        return zaradjeno

    def preskoči(self) -> int:
        self.trenutni_idx += 1
        return self.BODOVI_SKIP

    def gotovo(self) -> bool:
        return self.trenutni_idx >= len(self.pitanja)

    def ukupno(self) -> int:
        return len(self.pitanja)

# ─────────────────────────────────────────────
#  Klasa  SPOJNICE
# ─────────────────────────────────────────────
class Spojnice:
    BODOVI_TACNO  = 3
    BODOVI_GRESKA = 0
    BROJ_PAROVA   = 8

    def __init__(self, putanja_db: str):
        self.putanja_db = putanja_db
        self.tema:    str  = ""
        self.parovi:  dict = {}   # {pojam: odgovor}
        self.spojeno: dict = {}   # {pojam: odgovor} – uspješno spojeni parovi
        self.pogresno: set = set()  # pojmovi koji su pogrešno spojeni (privremeno)
        self.bodovi:  int  = 0
        self.odabrani_pojam: str | None = None
        self._ucitaj_red()

    def _ucitaj_red(self):
        try:
            conn = sqlite3.connect(self.putanja_db)
            cur  = conn.cursor()
            cur.execute("""
                SELECT tema,
                       pojam_1, odgovor_1, pojam_2, odgovor_2,
                       pojam_3, odgovor_3, pojam_4, odgovor_4,
                       pojam_5, odgovor_5, pojam_6, odgovor_6,
                       pojam_7, odgovor_7, pojam_8, odgovor_8
                FROM spojnice ORDER BY RANDOM() LIMIT 1
            """)
            red = cur.fetchone()
            conn.close()
        except Exception as e:
            print(f"Greška pri čitanju spojnica: {e}")
            red = None

        if red:
            self.tema = red[0]
            self.parovi = {}
            for i in range(self.BROJ_PAROVA):
                pojam    = red[1 + i * 2]
                odgovor  = red[2 + i * 2]
                if pojam and odgovor:
                    self.parovi[pojam] = odgovor
        else:
            self.tema   = "Nema podataka"
            self.parovi = {}

    def selektuj_pojam(self, pojam: str):
        """Selektuje ili deselektuje pojam s lijeve strane."""
        if self.odabrani_pojam == pojam:
            self.odabrani_pojam = None
        else:
            self.odabrani_pojam = pojam

    def pokusaj_spajanje(self, odgovor: str) -> bool | None:
        """
        Pokušava spojiti odabrani pojam s odgovorom.
        Vraća True (tačno), False (pogrešno), None (nema odabranog pojma).
        """
        if self.odabrani_pojam is None:
            return None
        pojam = self.odabrani_pojam
        self.odabrani_pojam = None
        if self.parovi.get(pojam) == odgovor:
            self.spojeno[pojam] = odgovor
            self.bodovi += self.BODOVI_TACNO
            return True
        else:
            return False

    def reset(self):
        self.spojeno        = {}
        self.pogresno       = set()
        self.bodovi         = 0
        self.odabrani_pojam = None
        self._ucitaj_red()

# ─────────────────────────────────────────────
#  Glavni GUI  –  SlagalicaApp
# ─────────────────────────────────────────────
class SlagalicaApp:
 
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("SLAGALICA")
        self.root.geometry("1920x1080")
        self.root.configure(bg=BG_TAMNA)
        self.root.resizable(True, True)
 
        _base = os.path.dirname(os.path.abspath(__file__))
        self._putanja_rjecnika  = os.path.join(_base, "Fajlovi", "serbian-words-latin.txt")
        self._putanja_highscore = os.path.join(_base, "Fajlovi", "highscore.txt")
        self._putanja_ikonica   = os.path.join(_base, "Fajlovi", "Icons")
 
        self._rjecnik:   set = Slagalica.ucitaj_rjecnik(self._putanja_rjecnika)
        self._highscore: int = Slagalica.ucitaj_highscore(self._putanja_highscore)
 
        self.igra      = Igra()
        self.slagalica: Slagalica = None
        self.moj_broj:  MojBroj   = None
        self.skocko:    Skocko    = None
 
        self._igra_aktivna      = False
        self._unos_aktivan      = False
        self._animacija_aktivna = False
        self._animacija_id      = None
        self._timer_id          = None
        self._vrati_id          = None
        self.preostalo_vrijeme  = 60
 
        self._mb_animacija_id    = None
        self._mb_timer_id        = None
        self._mb_vrati_id        = None
        self._mb_timer_vrijede   = 90
        self._mb_unos_aktivan    = False
        self._mb_solver_check_id = None
 
        self._sk_vrati_id = None
        self._sk_timer_id  = None
        self._sk_vrijede   = 120
 
        # Učitaj ikonice
        self._sk_ikone = {}
        self._ucitaj_ikone()
 
        self._def_fontovi()
        self._build_ui()
        
        self.ko_zna_zna: KoZnaZna = None
        self._kzz_timer_id = None
        self._kzz_vrijede  = 10
        self._kzz_vrati_id = None
        self._putanja_db = os.path.join(_base, "Fajlovi", "ko_zna_zna.db")
        
        self.spojnice: Spojnice = None
        self._sp_timer_id  = None
        self._sp_vrijede   = 90
        self._sp_vrati_id  = None

        self._putanja_spojnice_db = os.path.join(_base, "Fajlovi", "spojnice.db")

        # Interni state za GUI spojnica
        self._sp_pojam_dugmad:   dict = {}   # pojam  -> Button
        self._sp_odgovor_dugmad: dict = {}   # odgovor -> Button
        self._sp_odabrani_pojam: str | None = None
        self._sp_anim_running:   bool = False
 
    # ══════════════════════════════════════════
    #  Učitavanje ikonica
    # ══════════════════════════════════════════
    def _ucitaj_ikone(self):
        try:
            from PIL import Image, ImageTk
            self._pil_dostupan = True
        except ImportError:
            self._pil_dostupan = False
            return
 
        velicina = (72, 72)
        mala     = (56, 56)
        for naziv in Skocko.ZNAKOVI:
            putanja = os.path.join(self._putanja_ikonica, f"{naziv}.png")
            if os.path.exists(putanja):
                try:
                    img  = Image.open(putanja).resize(velicina, Image.LANCZOS)
                    img_m= Image.open(putanja).resize(mala, Image.LANCZOS)
                    self._sk_ikone[naziv]          = ImageTk.PhotoImage(img)
                    self._sk_ikone[naziv + "_mala"] = ImageTk.PhotoImage(img_m)
                except Exception as e:
                    print(f"Greška pri učitavanju ikonice {naziv}: {e}")
                    
        try:
            putanja_sat = os.path.join("Fajlovi", "sat.png")
            img_sat = Image.open(putanja_sat).resize((48, 48), Image.LANCZOS)
            self._ikona_sat = ImageTk.PhotoImage(img_sat)
        except Exception:
            self._ikona_sat = None
 
    def _ikona(self, naziv: str):
        return self._sk_ikone.get(naziv)
 
    def _ikona_mala(self, naziv: str):
        return self._sk_ikone.get(naziv + "_mala")
 
    # ══════════════════════════════════════════
    #  Fontovi
    # ══════════════════════════════════════════
    def _def_fontovi(self):
        self.f_naslov   = tkfont.Font(family="Helvetica", size=42, weight="bold")
        self.f_slovo    = tkfont.Font(family="Courier New", size=28, weight="bold")
        self.f_unos     = tkfont.Font(family="Courier New", size=28, weight="bold")
        self.f_status   = tkfont.Font(family="Helvetica", size=20)
        self.f_bodovi   = tkfont.Font(family="Helvetica", size=36, weight="bold")
        self.f_gumb     = tkfont.Font(family="Helvetica", size=18, weight="bold")
        self.f_maly     = tkfont.Font(family="Helvetica", size=14)
        self.f_rezultat = tkfont.Font(family="Helvetica", size=22, weight="bold")
        self.f_timer    = tkfont.Font(family="Courier New", size=38, weight="bold")
        self.f_mb_broj  = tkfont.Font(family="Courier New", size=24, weight="bold")
        self.f_mb_op    = tkfont.Font(family="Helvetica", size=22, weight="bold")
        self.f_mb_cilj  = tkfont.Font(family="Courier New", size=32, weight="bold")
        self.f_mb_izraz = tkfont.Font(family="Courier New", size=22, weight="bold")
        self.f_sk_gumb  = tkfont.Font(family="Helvetica", size=13, weight="bold")
 
    # ══════════════════════════════════════════
    #  Izgradnja UI
    # ══════════════════════════════════════════
    def _build_ui(self):
        self.header_frame = tk.Frame(self.root, bg=BG_TAMNA, height=90)
        self.header_frame.pack(fill="x", pady=(4, 0))
        self.header_frame.pack_propagate(False)
 
        tk.Label(self.header_frame,
                 text="S  L  A  G  A  L  I  C  A",
                 bg=BG_TAMNA, fg=ZLATNA,
                 font=self.f_naslov).pack(expand=True)
 
        self.container = tk.Frame(self.root, bg=BG_TAMNA)
        self.container.pack(fill="both", expand=True)
 
        self.main_screen = MainScreen(
            self.container,
            highscore=self._highscore,
            on_igraj=self._start_slag,
            on_izlaz=self.root.destroy,
            f_bodovi=self.f_bodovi,
            f_gumb=self.f_gumb,
            f_maly=self.f_maly,
            f_status=self.f_status
        )
 
        self.slag_frame = tk.Frame(self.container, bg=BG_TAMNA)
        self._build_slag_ekran()
 
        self.mb_frame = tk.Frame(self.container, bg=BG_TAMNA)
        self._build_mb_ekran()
 
        self.sk_frame = tk.Frame(self.container, bg=BG_TAMNA)
        self._build_sk_ekran()
        
        self.kzz_frame = tk.Frame(self.container, bg=BG_TAMNA)
        self._build_kzz_ekran()
        
        self.sp_frame = tk.Frame(self.container, bg=BG_TAMNA)
        self._build_sp_ekran()
 
        self.main_screen.show()
 
    # ══════════════════════════════════════════
    #  Navigacija
    # ══════════════════════════════════════════
    def _show_main_screen(self):
        self.slag_frame.place_forget()
        self.mb_frame.place_forget()
        self.sk_frame.place_forget()
        self.kzz_frame.place_forget()
        self.sp_frame.place_forget()
        self.main_screen.show()
 
    def _show_igra_ekran(self):
        self.main_screen.hide()
        self.mb_frame.place_forget()
        self.sk_frame.place_forget()
        self.kzz_frame.place_forget()
        self.sp_frame.place_forget()
        self.slag_frame.place(relx=0, rely=0.08, relwidth=1, relheight=0.92)
 
    def _show_mb_ekran(self):
        self.slag_frame.place_forget()
        self.sk_frame.place_forget()
        self.kzz_frame.place_forget()
        self.sp_frame.place_forget()
        self.mb_frame.place(relx=0, rely=0.08, relwidth=1, relheight=0.92)
 
    def _show_sk_ekran(self):
        self.mb_frame.place_forget()
        self.slag_frame.place_forget()
        self.kzz_frame.place_forget()
        self.sp_frame.place_forget()
        self.sk_frame.place(relx=0, rely=0.08, relwidth=1, relheight=0.92)
    
    def _show_kzz_ekran(self):
        self.slag_frame.place_forget()
        self.mb_frame.place_forget()
        self.sk_frame.place_forget()
        self.sp_frame.place_forget()
        self.kzz_frame.place(relx=0, rely=0.08, relwidth=1, relheight=0.92)
    
    def _show_sp_ekran(self):
        self.slag_frame.place_forget()
        self.mb_frame.place_forget()
        self.sk_frame.place_forget()
        self.kzz_frame.place_forget()
        self.sp_frame.place(relx=0, rely=0.08, relwidth=1, relheight=0.92)
        
    # ══════════════════════════════════════════
    #  Slagalica UI
    # ══════════════════════════════════════════
    def _build_slag_ekran(self):
        f = self.slag_frame
 
        timer_frame = tk.Frame(f, bg=BG_TAMNA)
        timer_frame.pack(pady=(8, 4))
        if self._ikona_sat:
            self.lbl_sat = tk.Label(timer_frame, image=self._ikona_sat, bg=BG_TAMNA)
            self.lbl_sat.pack(side="left", padx=(0, 6))
        else:
            self.lbl_sat = None
        self.lbl_timer = tk.Label(timer_frame, text="60", bg=BG_TAMNA, fg=ZLATNA, font=self.f_timer)
        self.lbl_timer.pack(side="left")
 
        self.lbl_status = tk.Label(f, text="", bg=BG_TAMNA, fg=BIJELA,
                                   font=self.f_status, justify="center", wraplength=1400)
        self.lbl_status.pack(pady=(0, 4))
 
        unos_outer = tk.Frame(f, bg=BG_KARTICA, bd=0)
        unos_outer.pack(fill="x", padx=80, pady=(0, 10), ipady=12)
 
        self.lbl_unos = tk.Label(unos_outer, text="",
                                 bg=BG_KARTICA, fg=ZLATNA,
                                 font=self.f_unos, anchor="w")
        self.lbl_unos.pack(side="left", padx=40)
 
        self.lbl_rjecnik_status = tk.Label(unos_outer, text="",
                                           bg=BG_KARTICA, fg=ZELENA,
                                           font=self.f_status, anchor="e")
        self.lbl_rjecnik_status.pack(side="right", padx=40)
 
        self.slova_outer = tk.Frame(f, bg=BG_TAMNA)
        self.slova_outer.pack(pady=(0, 14))
 
        self.dugmad:    list = []
        self.var_slova: list = []
 
        for red in range(2):
            row_frame = tk.Frame(self.slova_outer, bg=BG_TAMNA)
            row_frame.pack()
            for kol in range(6):
                idx = red * 6 + kol
                var = tk.StringVar(value="?")
                self.var_slova.append(var)
                btn = tk.Button(row_frame, textvariable=var, width=4, height=2,
                                bg=BG_KARTICA, fg=ZLATNA, activebackground=ZLATNA_TAMNA,
                                activeforeground=BG_TAMNA, font=self.f_slovo,
                                relief="flat", bd=0, cursor="hand2",
                                state="disabled", command=lambda i=idx: self._slag_klik_slovo(i))
                btn.pack(side="left", padx=5, pady=5)
                self._dodaj_hover(btn, BG_KARTICA, "#2D3F55")
                self.dugmad.append(btn)
 
        self.kontrole_frame = tk.Frame(f, bg=BG_TAMNA)
        self.kontrole_frame.pack(pady=(0, 10))
 
        self.btn_potvrdi = tk.Button(self.kontrole_frame, text="✔  POTVRDI",
                                     command=self._slag_klik_potvrdi, bg=BTN_POTVRDI_BG, fg=BIJELA,
                                     activebackground=BTN_POTVRDI_HOV, activeforeground=BIJELA,
                                     font=self.f_gumb, relief="flat", bd=0,
                                     cursor="hand2", padx=40, pady=14, state="disabled")
        self.btn_potvrdi.pack(side="left", padx=12)
 
        self.btn_obrisi = tk.Button(self.kontrole_frame, text="⌫  OBRIŠI",
                                    command=self._slag_klik_obrisi, bg=BTN_OBRISI_BG, fg=BIJELA,
                                    activebackground="#8B3A3A", activeforeground=BIJELA,
                                    font=self.f_gumb, relief="flat", bd=0,
                                    cursor="hand2", padx=30, pady=14, state="disabled")
        self.btn_obrisi.pack(side="left", padx=12)
 
        self.rezultat_frame = tk.Frame(f, bg=BG_TAMNA)
 
    # ══════════════════════════════════════════
    #  Start igre (Slagalica)
    # ══════════════════════════════════════════
    def _start_slag(self):
        if self._vrati_id:
            self.root.after_cancel(self._vrati_id)
            self._vrati_id = None
        self.igra.reset()
        self._show_igra_ekran()
        self._reset_slag_ekran()
        self._nova_runda()
 
    def _reset_slag_ekran(self):
        self.lbl_status.config(text="", fg=BIJELA)
        self.lbl_unos.config(text="", fg=ZLATNA)
        self.lbl_rjecnik_status.config(text="")
        if self.lbl_sat:
            self.lbl_sat.pack(side="left", padx=(0, 6))
        self.lbl_timer.config(text="60", fg=ZLATNA)
        self.btn_potvrdi.config(state="disabled")
        self.btn_obrisi.config(state="disabled")
 
        self.rezultat_frame.pack_forget()
        self.slova_outer.pack(pady=(0, 14))
        self.kontrole_frame.pack(pady=(0, 10))
        self._potrosena_dugmad = set()
 
        for i, btn in enumerate(self.dugmad):
            btn.config(state="disabled", bg=BG_KARTICA, fg=ZLATNA)
            self.var_slova[i].set("?")
 
    def _nova_runda(self):
        self._slag_zaustavi_animaciju()
        self.slagalica        = Slagalica(self._rjecnik)
        self._igra_aktivna    = True
        self._unos_aktivan    = False
        self.preostalo_vrijeme = 60
        self.lbl_timer.config(text="60", fg=ZLATNA)
 
        for btn in self.dugmad:
            btn.config(state="normal", bg=BG_KARTICA, fg=ZLATNA)
 
        self.btn_potvrdi.config(state="disabled")
        self.btn_obrisi.config(state="disabled")
        self.lbl_status.config(
            text="Kliknite na dugmad da fiksirate slova!", fg=BIJELA)
 
        self._slag_pokreni_animaciju()
 
    # ══════════════════════════════════════════
    #  Animacija (Slagalica)
    # ══════════════════════════════════════════
    def _slag_pokreni_animaciju(self):
        self._animacija_aktivna = True
        self._slag_animiraj()
 
    def _slag_animiraj(self):
        if not self._animacija_aktivna or self.slagalica is None:
            return
        if self.slagalica.sva_fiksirana():
            return
        for i in range(12):
            if self.slagalica.fiksirana_slova[i] is None:
                self.slagalica.animacija_slova[i] = self.slagalica.random_jedno()
        self._slag_osvjezi_slova(list(self.slagalica.animacija_slova))
        self._animacija_id = self.root.after(80, self._slag_animiraj)
 
    def _slag_zaustavi_animaciju(self):
        self._animacija_aktivna = False
        if self._animacija_id:
            self.root.after_cancel(self._animacija_id)
            self._animacija_id = None
        self._igra_aktivna = False
        if self._timer_id:
            self.root.after_cancel(self._timer_id)
            self._timer_id = None
 
    def _slag_osvjezi_slova(self, slova: list):
        for i, s in enumerate(slova):
            if self.slagalica and self.slagalica.fiksirana_slova[i] is None:
                self.var_slova[i].set(s)
 
    # ══════════════════════════════════════════
    #  Klik na slovo (Slagalica)
    # ══════════════════════════════════════════
    def _slag_klik_slovo(self, idx: int):
        if not self._igra_aktivna or self.slagalica is None:
            return

        if not self._unos_aktivan:
            fiksirano = self.slagalica.fiksiraj_slovo(idx)
            if fiksirano:
                self.dugmad[idx].config(bg=FIKSIRANO_BG, fg=FIKSIRANO_FG)
                self.var_slova[idx].set(fiksirano)

            if self.slagalica.sva_fiksirana():
                self._slag_zaustavi_animaciju()
                self._igra_aktivna = True
                self._unos_aktivan = True
                for i, btn in enumerate(self.dugmad):
                    btn.config(bg=BG_KARTICA, fg=ZLATNA, cursor="hand2", state="normal")
                    self.var_slova[i].set(self.slagalica.fiksirana_slova[i])
                self.btn_potvrdi.config(state="normal")
                self.btn_obrisi.config(state="normal")
                self.lbl_status.config(text="Kliknite slova da složite riječ, zatim POTVRDI", fg=ZLATNA)
                self.preostalo_vrijeme = 60
                self.lbl_timer.config(text="60", fg=ZLATNA)
                self._pokreni_slag_timer()
        else:
            slovo = self.slagalica.fiksirana_slova[idx]
            if slovo is None:
                return
            if self.slagalica.dodaj_slovo_u_unos(slovo):
                self.dugmad[idx].config(state="disabled", bg="#0F2030", fg="#334455")
                self._potrosena_dugmad.add(idx)  # ← SAMO OVO DODAJEŠ
                self.slag_osvjezi_unos()
 
    # ══════════════════════════════════════════
    #  Unos (Slagalica)
    # ══════════════════════════════════════════
    def slag_osvjezi_unos(self):
        if not self.slagalica:
            return
        unos_lista = self.slagalica.unos
        unos_str   = "".join(unos_lista)
        prikaz     = " ".join(unos_lista) if unos_lista else ""
        self.lbl_unos.config(text=prikaz, fg=ZLATNA)
 
        if len(unos_lista) >= 2:
            if self.slagalica.provjeri_unos():
                self.lbl_rjecnik_status.config(
                    text=f"✔ '{unos_str}' postoji u rječniku!", fg=ZELENA)
            else:
                self.lbl_rjecnik_status.config(
                    text=f"✘ '{unos_str}' nije pronađena...", fg=CRVENA)
        else:
            self.lbl_rjecnik_status.config(text="")
 
    def _slag_klik_obrisi(self):
        if not self.slagalica or not self._unos_aktivan:
            return
        if not self.slagalica.unos:
            return
        zadnje = self.slagalica.unos[-1]
        self.slagalica.obrisi_zadnje()
        for i, btn in enumerate(self.dugmad):
            if (i in self._potrosena_dugmad and self.slagalica.fiksirana_slova[i] == zadnje):
                self._potrosena_dugmad.discard(i)
                self.dugmad[i].config(state="normal", bg=BG_KARTICA, fg=ZLATNA)
                break
        self.slag_osvjezi_unos()
 
    # ══════════════════════════════════════════
    #  Potvrdi (Slagalica)
    # ══════════════════════════════════════════
    def _slag_klik_potvrdi(self):
        if not self.slagalica or not self._unos_aktivan:
            return
        unos_lista = self.slagalica.unos
        unos_str   = "".join(unos_lista)
 
        if self._timer_id:
            self.root.after_cancel(self._timer_id)
            self._timer_id = None
        self.lbl_timer.config(text="")
        if self.lbl_sat:
            self.lbl_sat.pack_forget()
 
        zaradjeno = self.slagalica.potvrdi_rijec(unos_lista)
        self.igra.dodaj_bodove(zaradjeno)
 
        self._unos_aktivan = False
        self._igra_aktivna = False
 
        self.slova_outer.pack_forget()
        self.kontrole_frame.pack_forget()
        self.lbl_status.config(text="")
        self.lbl_rjecnik_status.config(text="")
 
        self._prikazi_rezultate_slagalica(unos_str, zaradjeno)
 
    # ══════════════════════════════════════════
    #  Rezultati Slagalice → prelaz na Moj Broj
    # ══════════════════════════════════════════
    def _prikazi_rezultate_slagalica(self, unos: str, zaradjeno: int):
        for widget in self.rezultat_frame.winfo_children():
            widget.destroy()
 
        self.rezultat_frame.pack(fill="both", expand=True, pady=20)
 
        center = tk.Frame(self.rezultat_frame, bg=BG_TAMNA)
        center.place(relx=0.5, rely=0.5, anchor="center")
 
        tk.Label(center, text="REZULTAT  –  SLAGALICA",
                 bg=BG_TAMNA, fg=SIVA_SVIJETLA,
                 font=self.f_maly).pack(pady=(0, 10))
 
        tvoja_frame = tk.Frame(center, bg=BG_PANEL, padx=50, pady=20)
        tvoja_frame.pack(pady=(0, 24), fill="x")
 
        tk.Label(tvoja_frame, text="Tvoja riječ:",
                 bg=BG_PANEL, fg=SIVA_SVIJETLA,
                 font=self.f_maly).pack(side="left", padx=(0, 20))
 
        boja = ZELENA if zaradjeno > 0 else CRVENA
        tk.Label(tvoja_frame,
                 text=unos.upper() if unos else "—",
                 bg=BG_PANEL, fg=boja,
                 font=self.f_rezultat).pack(side="left")
 
        poruka_bodovi = f"+{zaradjeno} bodova" if zaradjeno > 0 else "+0 bodova"
        tk.Label(tvoja_frame,
                 text=poruka_bodovi,
                 bg=BG_PANEL, fg=boja,
                 font=self.f_rezultat).pack(side="right", padx=(20, 0))
 
        ukupno_frame = tk.Frame(center, bg=BG_KARTICA, padx=40, pady=16)
        ukupno_frame.pack(pady=(0, 20), fill="x")
 
        tk.Label(ukupno_frame, text="Ukupni bodovi:",
                 bg=BG_KARTICA, fg=SIVA_SVIJETLA,
                 font=self.f_status).pack(side="left")
        tk.Label(ukupno_frame, text=str(self.igra.bodovi),
                 bg=BG_KARTICA, fg=ZLATNA,
                 font=self.f_bodovi).pack(side="left", padx=(16, 0))
 
        tk.Label(center,
                 text="Sljedeće: MOJ BROJ",
                 bg=BG_TAMNA, fg=NARANCASTA,
                 font=self.f_status).pack(pady=(10, 0))
 
        self.lbl_status.config(text="", fg=BIJELA)
        self._vrati_id = self.root.after(5000, self._start_moj_broj)
 
    # ══════════════════════════════════════════
    #  Timer (Slagalica)
    # ══════════════════════════════════════════
    def _pokreni_slag_timer(self):
        self._slag_odbrojavaj()
 
    def _slag_odbrojavaj(self):
        self.lbl_timer.config(text=f"{self.preostalo_vrijeme}")
        self.lbl_timer.config(fg=CRVENA if self.preostalo_vrijeme <= 10 else ZLATNA)
 
        if self.preostalo_vrijeme <= 0:
            self._slag_vrijeme_isteklo()
            return
 
        self.preostalo_vrijeme -= 1
        self._timer_id = self.root.after(1000, self._slag_odbrojavaj)
 
    def _slag_vrijeme_isteklo(self):
        self.lbl_timer.config(text="0", fg=CRVENA)
        self.root.after(500, self._slag_klik_potvrdi)
        self.lbl_status.config(text="Vrijeme je isteklo! Automatska provjera...", fg=ZLATNA)
        self.root.after(500, self._slag_klik_potvrdi)
            
    # ══════════════════════════════════════════
    #  Moj Broj UI
    # ══════════════════════════════════════════
    def _build_mb_ekran(self):
        f = self.mb_frame
 
        mb_timer_frame = tk.Frame(f, bg=BG_TAMNA)
        mb_timer_frame.pack(pady=(6, 2))
        if self._ikona_sat:
            self.mb_lbl_sat = tk.Label(mb_timer_frame, image=self._ikona_sat, bg=BG_TAMNA)
            self.mb_lbl_sat.pack(side="left", padx=(0, 6))
        else:
            self.mb_lbl_sat = None
        self.mb_lbl_timer = tk.Label(mb_timer_frame, text="90", bg=BG_TAMNA, fg=ZLATNA, font=self.f_timer)
        self.mb_lbl_timer.pack(side="left")
 
        self.mb_lbl_status = tk.Label(f, text="",
                                      bg=BG_TAMNA, fg=BIJELA,
                                      font=self.f_status,
                                      justify="center", wraplength=1400)
        self.mb_lbl_status.pack(pady=(0, 4))
 
        izraz_outer = tk.Frame(f, bg=BG_KARTICA)
        izraz_outer.pack(fill="x", padx=80, pady=(0, 8), ipady=10)
 
        self.mb_lbl_izraz = tk.Label(izraz_outer, text="",
                                     bg=BG_KARTICA, fg=ZLATNA,
                                     font=self.f_mb_izraz, anchor="w")
        self.mb_lbl_izraz.pack(side="left", padx=30)
 
        self.mb_lbl_eval = tk.Label(izraz_outer, text="",
                                    bg=BG_KARTICA, fg=ZELENA,
                                    font=self.f_status, anchor="e")
        self.mb_lbl_eval.pack(side="right", padx=30)
 
        top_row = tk.Frame(f, bg=BG_TAMNA)
        top_row.pack(pady=(0, 6))
 
        cilj_frame = tk.Frame(top_row, bg=BG_PANEL, padx=30, pady=10)
        cilj_frame.pack(side="left", padx=20)
 
        tk.Label(cilj_frame, text="CILJNI BROJ",
                 bg=BG_PANEL, fg=SIVA_SVIJETLA,
                 font=self.f_maly).pack()
 
        self.mb_var_cilj = tk.StringVar(value="???")
        self.mb_btn_cilj = tk.Button(
            cilj_frame,
            textvariable=self.mb_var_cilj,
            bg=BG_PANEL, fg=NARANCASTA,
            activebackground=BG_PANEL, activeforeground=ZLATNA,
            font=self.f_mb_cilj, relief="flat", bd=0,
            cursor="hand2", padx=10,
            command=self._mb_klik_cilj
        )
        self.mb_btn_cilj.pack()
 
        bodovi_frame = tk.Frame(top_row, bg=BG_PANEL, padx=30, pady=10)
        bodovi_frame.pack(side="left", padx=20)
 
        tk.Label(bodovi_frame, text="UKUPNI BODOVI",
                 bg=BG_PANEL, fg=SIVA_SVIJETLA,
                 font=self.f_maly).pack()
 
        self.mb_lbl_bodovi = tk.Label(bodovi_frame, text="0",
                                      bg=BG_PANEL, fg=ZLATNA,
                                      font=self.f_bodovi)
        self.mb_lbl_bodovi.pack()
 
        self.mb_slot_frame = tk.Frame(f, bg=BG_TAMNA)
        self.mb_slot_frame.pack(pady=(0, 8))
 
        self.mb_var_slot  = [tk.StringVar(value="?") for _ in range(6)]
        self.mb_btn_slot  = []
 
        self._mb_slot_fg = [ZLATNA, ZLATNA, ZLATNA, ZLATNA, PLAVA_AKCENT, NARANCASTA]
 
        for i in range(6):
            btn = tk.Button(self.mb_slot_frame, textvariable=self.mb_var_slot[i],
                            width=5, height=2, bg=BG_KARTICA, fg=self._mb_slot_fg[i],
                            activebackground=ZLATNA_TAMNA, activeforeground=BG_TAMNA,
                            font=self.f_mb_broj, relief="flat", bd=0, cursor="hand2", state="disabled",
                            command=lambda idx=i: self._mb_klik_slot(idx))
            btn.pack(side="left", padx=6)
            self._dodaj_hover(btn, BG_KARTICA, "#2D3F55")
            self.mb_btn_slot.append(btn)
 
        self.mb_op_frame = tk.Frame(f, bg=BG_TAMNA)
        self.mb_op_frame.pack(pady=(0, 6))
 
        self.mb_btn_ops: list = []
        for op_sym in ['+', '−', '×', '÷', '(', ')']:
            real_op = {'+': '+', '−': '-', '×': '*', '÷': '/', '(': '(', ')': ')'}[op_sym]
            btn = tk.Button(self.mb_op_frame, text=op_sym,
                            width=3, height=1, bg="#1C3050", fg=BIJELA,
                            activebackground="#2A4A70", activeforeground=BIJELA,
                            font=self.f_mb_op, relief="flat", bd=0,
                            cursor="hand2", state="disabled",
                            command=lambda op=real_op: self._mb_klik_op(op))
            btn.pack(side="left", padx=6, pady=4)
            self._dodaj_hover(btn, "#1C3050", "#2A4A70")
            self.mb_btn_ops.append(btn)
 
        self.mb_kontrole_frame = tk.Frame(f, bg=BG_TAMNA)
        self.mb_kontrole_frame.pack(pady=(0, 6))
 
        self.mb_btn_potvrdi = tk.Button(self.mb_kontrole_frame, text="✔  POTVRDI",
                                        command=self._mb_slag_klik_potvrdi,
                                        bg=BTN_POTVRDI_BG, fg=BIJELA,
                                        activebackground=BTN_POTVRDI_HOV, activeforeground=BIJELA,
                                        font=self.f_gumb, relief="flat", bd=0,
                                        cursor="hand2", padx=40, pady=12, state="disabled")
        self.mb_btn_potvrdi.pack(side="left", padx=12)
 
        self.mb_btn_obrisi = tk.Button(self.mb_kontrole_frame, text="⌫  OBRIŠI",
                                       command=self._mb_slag_klik_obrisi,
                                       bg=BTN_OBRISI_BG, fg=BIJELA,
                                       activebackground="#8B3A3A", activeforeground=BIJELA,
                                       font=self.f_gumb, relief="flat", bd=0,
                                       cursor="hand2", padx=30, pady=12, state="disabled")
        self.mb_btn_obrisi.pack(side="left", padx=12)
 
        self.mb_rezultat_frame = tk.Frame(f, bg=BG_TAMNA)
 
    # ══════════════════════════════════════════
    #  MOJ BROJ – start
    # ══════════════════════════════════════════
    def _start_moj_broj(self):
        if self._vrati_id:
            self.root.after_cancel(self._vrati_id)
            self._vrati_id = None
 
        self.moj_broj = MojBroj()
        self._mb_unos_aktivan  = False
        self._mb_timer_vrijede = 90
 
        self._mb_reset_ekran()
        self._show_mb_ekran()
        self._mb_pokreni_animacije()
 
    def _mb_reset_ekran(self):
        self.mb_lbl_timer.config(text="90", fg=ZLATNA)
        if self.mb_lbl_sat:
            self.mb_lbl_sat.pack(side="left", padx=(0, 6))
        self.mb_lbl_status.config(
            text="Kliknite dugmad da odaberete brojeve!", fg=BIJELA)
        self.mb_lbl_izraz.config(text="")
        self.mb_lbl_eval.config(text="")
        self.mb_var_cilj.set("???")
        self.mb_lbl_bodovi.config(text=str(self.igra.bodovi))
 
        for i in range(6):
            self.mb_var_slot[i].set("?")
            self.mb_btn_slot[i].config(
                state="disabled",
                bg=BG_KARTICA,
                fg=self._mb_slot_fg[i])
 
        self.mb_btn_cilj.config(state="normal", bg=BG_PANEL, fg=NARANCASTA)
 
        for btn in self.mb_btn_ops:
            btn.config(state="disabled")
 
        self.mb_btn_potvrdi.config(state="disabled")
        self.mb_btn_obrisi.config(state="disabled")
 
        self.mb_rezultat_frame.pack_forget()
        self.mb_slot_frame.pack(pady=(0, 8))
        self.mb_op_frame.pack(pady=(0, 6))
        self.mb_kontrole_frame.pack(pady=(0, 6))
 
    # ══════════════════════════════════════════
    #  MOJ BROJ – animacija slotova
    # ══════════════════════════════════════════
    def _mb_pokreni_animacije(self):
        self._mb_slag_animiraj()
 
    def _mb_slag_animiraj(self):
        if self.moj_broj is None:
            return
        mb = self.moj_broj
        sve_fiksirane = all(mb.fiksirani)
        if sve_fiksirane and mb.cilj_fiksiran:
            return
 
        for i in range(6):
            if not mb.fiksirani[i]:
                mb.animacija_vrijednosti[i] = mb._novi_random(i)
                self.mb_var_slot[i].set(str(mb.animacija_vrijednosti[i]))
 
        if not mb.cilj_fiksiran:
            mb.animacija_cilj = random.randint(1, 999)
            self.mb_var_cilj.set(str(mb.animacija_cilj))
 
        self._mb_animacija_id = self.root.after(80, self._mb_slag_animiraj)
 
    def _mb_slag_zaustavi_animaciju(self):
        if self._mb_animacija_id:
            self.root.after_cancel(self._mb_animacija_id)
            self._mb_animacija_id = None
 
    # ══════════════════════════════════════════
    #  MOJ BROJ – klik na slot
    # ══════════════════════════════════════════
    def _mb_klik_slot(self, slot: int):
        if self.moj_broj is None:
            return
        
        if not self.moj_broj.cilj_fiksiran and not self._mb_unos_aktivan:
            self.mb_lbl_status.config(text="Prvo kliknite ciljni broj!", fg=CRVENA)
            return
        
        if not self._mb_unos_aktivan:
            val = self.moj_broj.fiksiraj_slot(slot)
            if val is None:
                return
            self.mb_var_slot[slot].set(str(val))
            self.mb_btn_slot[slot].config(bg=FIKSIRANO_BG, fg=FIKSIRANO_FG)
 
            if self.moj_broj.svi_fiksirani:
                self._mb_slag_zaustavi_animaciju()
                self._mb_aktiviraj_unos()
        else:
            if self.moj_broj.dodaj_broj(slot):
                self.mb_btn_slot[slot].config(
                    state="disabled", bg="#0F2030", fg="#334455")
                self._mb_osvjezi_izraz()
 
    def _mb_aktiviraj_unos(self):
        for i in range(6):
            val = self.moj_broj.odabrani_brojevi[i]
            self.mb_var_slot[i].set(str(val))
            self.mb_btn_slot[i].config(bg=BG_KARTICA, fg=self._mb_slot_fg[i],
                                       state="normal", cursor="hand2")
 
        for btn in self.mb_btn_ops:
            btn.config(state="normal")
        self.mb_btn_potvrdi.config(state="normal")
        self.mb_btn_obrisi.config(state="normal")
 
        self._mb_unos_aktivan = True
        self.mb_lbl_status.config(
            text="Složite matematički izraz i kliknite POTVRDI", fg=ZLATNA)
 
        self._mb_pokreni_slag_timer()
 
        if self.moj_broj.cilj_fiksiran:
            self.moj_broj._pokreni_solver()
 
    # ══════════════════════════════════════════
    #  MOJ BROJ – klik operatora
    # ══════════════════════════════════════════
    def _mb_klik_op(self, op: str):
        if not self._mb_unos_aktivan or self.moj_broj is None:
            return
        if op in ('+', '-', '*', '/'):
            self.moj_broj.dodaj_operator(op)
        elif op == '(':
            self.moj_broj.dodaj_otvorenu_zagradu()
        elif op == ')':
            self.moj_broj.dodaj_zatvorenu_zagradu()
        self._mb_osvjezi_izraz()
 
    # ══════════════════════════════════════════
    #  MOJ BROJ – obriši
    # ══════════════════════════════════════════
    def _mb_slag_klik_obrisi(self):
        if not self._mb_unos_aktivan or self.moj_broj is None:
            return
        idx = self.moj_broj.obrisi_zadnji()
        if idx is not None:
            if idx < len(self.mb_btn_slot):
                self.mb_btn_slot[idx].config(
                    state="normal",
                    bg=BG_KARTICA,
                    fg=self._mb_slot_fg[idx]
                )
        self._mb_osvjezi_izraz()
 
    # ══════════════════════════════════════════
    #  MOJ BROJ – klik ciljnog broja
    # ══════════════════════════════════════════
    def _mb_klik_cilj(self):
        if self.moj_broj is None or self.moj_broj.cilj_fiksiran:
            return
        val = self.moj_broj.fiksiraj_cilj()
        self.mb_var_cilj.set(str(val))
        self.mb_btn_cilj.config(state="disabled", bg=BG_PANEL, fg=ZLATNA)
        
        for i in range(6):
            self.mb_btn_slot[i].config(state="normal")
        self.mb_lbl_status.config(text="Kliknite dugmad da odaberete brojeve!", fg=BIJELA)
 
    # ══════════════════════════════════════════
    #  MOJ BROJ – osvježi izraz
    # ══════════════════════════════════════════
    def _mb_osvjezi_izraz(self):
        if self.moj_broj is None:
            return
        izraz = self.moj_broj.izraz_string()
        self.mb_lbl_izraz.config(text=izraz)
 
        res = self.moj_broj.evaluiraj_izraz()
        if res is not None:
            cilj = self.moj_broj.ciljni_broj
            if res == cilj:
                self.mb_lbl_eval.config(text=f"= {res}", fg=ZELENA)
            else:
                self.mb_lbl_eval.config(text=f"= {res}", fg=ZLATNA)
        else:
            self.mb_lbl_eval.config(text="")
 
    # ══════════════════════════════════════════
    #  MOJ BROJ – potvrdi
    # ══════════════════════════════════════════
    def _mb_slag_klik_potvrdi(self):
        if not self._mb_unos_aktivan or self.moj_broj is None:
            return
 
        if self._mb_timer_id:
            self.root.after_cancel(self._mb_timer_id)
            self._mb_timer_id = None
        self.mb_lbl_timer.config(text="")
        if self.mb_lbl_sat:
            self.mb_lbl_sat.pack_forget()
        self._mb_unos_aktivan = False
 
        korisnikov_rezultat = self.moj_broj.evaluiraj_izraz()
 
        if self.moj_broj.solver_gotov:
            self._mb_finaliziraj(korisnikov_rezultat)
        else:
            self.mb_lbl_status.config(
                text="Molimo sačekajte, tražim optimalno rješenje...",
                fg=ZLATNA)
            self._mb_cekaj_solver(korisnikov_rezultat)
 
    def _mb_cekaj_solver(self, korisnikov_rezultat):
        if self.moj_broj.solver_gotov:
            self.mb_lbl_status.config(text="")
            self._mb_finaliziraj(korisnikov_rezultat)
        else:
            self._mb_solver_check_id = self.root.after(
                200, lambda: self._mb_cekaj_solver(korisnikov_rezultat))
 
    def _mb_finaliziraj(self, korisnikov_rezultat: int | None):
        zaradjeno = self.moj_broj.izracunaj_bodove(korisnikov_rezultat)
        self.igra.dodaj_bodove(zaradjeno)
 
        if self.igra.bodovi > self._highscore:
            self._highscore = self.igra.bodovi
            Slagalica.spremi_highscore(self._putanja_highscore, self._highscore)
            self.main_screen.azuriraj_highscore(self._highscore)
 
        self._mb_prikazi_rezultate(korisnikov_rezultat, zaradjeno)
 
    # ══════════════════════════════════════════
    #  MOJ BROJ – prikaz rezultata → prelaz na SKOČKO
    # ══════════════════════════════════════════
    def _mb_prikazi_rezultate(self, korisnikov_rezultat: int | None, zaradjeno: int):
        self.mb_slot_frame.pack_forget()
        self.mb_op_frame.pack_forget()
        self.mb_kontrole_frame.pack_forget()
        self.mb_lbl_status.config(text="")
 
        for widget in self.mb_rezultat_frame.winfo_children():
            widget.destroy()
        self.mb_rezultat_frame.pack(fill="both", expand=True, pady=10)
 
        center = tk.Frame(self.mb_rezultat_frame, bg=BG_TAMNA)
        center.place(relx=0.5, rely=0.5, anchor="center")
 
        tk.Label(center, text="REZULTAT  –  MOJ BROJ",
                 bg=BG_TAMNA, fg=SIVA_SVIJETLA,
                 font=self.f_maly).pack(pady=(0, 14))
 
        cilj_frame = tk.Frame(center, bg=BG_PANEL, padx=50, pady=14)
        cilj_frame.pack(pady=(0, 10), fill="x")
        tk.Label(cilj_frame, text="Ciljni broj:",
                 bg=BG_PANEL, fg=SIVA_SVIJETLA, font=self.f_maly).pack(side="left", padx=(0, 20))
        tk.Label(cilj_frame, text=str(self.moj_broj.ciljni_broj),
                 bg=BG_PANEL, fg=NARANCASTA, font=self.f_rezultat).pack(side="left")
 
        tvoj_frame = tk.Frame(center, bg=BG_PANEL, padx=50, pady=14)
        tvoj_frame.pack(pady=(0, 10), fill="x")
        tk.Label(tvoj_frame, text="Tvoj rezultat:",
                 bg=BG_PANEL, fg=SIVA_SVIJETLA, font=self.f_maly).pack(side="left", padx=(0, 20))
 
        boja_tv = ZELENA if zaradjeno > 0 else CRVENA
        prikaz_res = str(korisnikov_rezultat) if korisnikov_rezultat is not None else "—"
        tk.Label(tvoj_frame, text=prikaz_res,
                 bg=BG_PANEL, fg=boja_tv, font=self.f_rezultat).pack(side="left")
        tk.Label(tvoj_frame, text=f"+{zaradjeno} bodova",
                 bg=BG_PANEL, fg=boja_tv, font=self.f_rezultat).pack(side="right", padx=(20, 0))
 
        racunar_frame = tk.Frame(center, bg=BG_PANEL, padx=50, pady=14)
        racunar_frame.pack(pady=(0, 10), fill="x")
 
        tk.Label(racunar_frame, text="Računar pronašao:",
                 bg=BG_PANEL, fg=SIVA_SVIJETLA, font=self.f_maly).pack(side="left", padx=(0, 20))
 
        najblizi     = self.moj_broj.najblizi_rezultat
        najblizi_izr = self.moj_broj.najblizi_izraz
        prikaz_racunar = str(najblizi) if najblizi is not None else "—"
        tk.Label(racunar_frame, text=prikaz_racunar,
                 bg=BG_PANEL, fg=PLAVA_AKCENT, font=self.f_rezultat).pack(side="left")
 
        if najblizi_izr:
            tk.Label(racunar_frame,
                     text=f"  →  {najblizi_izr}",
                     bg=BG_PANEL, fg=SIVA_SVIJETLA,
                     font=self.f_maly).pack(side="left", padx=(10, 0))
 
        ukupno_frame = tk.Frame(center, bg=BG_KARTICA, padx=40, pady=16)
        ukupno_frame.pack(pady=(0, 20), fill="x")
        tk.Label(ukupno_frame, text="Ukupni bodovi:",
                 bg=BG_KARTICA, fg=SIVA_SVIJETLA, font=self.f_status).pack(side="left")
        tk.Label(ukupno_frame, text=str(self.igra.bodovi),
                 bg=BG_KARTICA, fg=ZLATNA, font=self.f_bodovi).pack(side="left", padx=(16, 0))
 
        # Prelaz na SKOČKO (ne na main screen)
        tk.Label(center,
                 text="Sljedeće: SKOČKO",
                 bg=BG_TAMNA, fg=NARANCASTA,
                 font=self.f_status).pack(pady=(10, 0))
 
        self._mb_vrati_id = self.root.after(5000, self._start_skocko)
 
    # ══════════════════════════════════════════
    #  MOJ BROJ – timer
    # ══════════════════════════════════════════
    def _mb_pokreni_slag_timer(self):
        self._mb_timer_vrijede = 90
        self._mb_slag_odbrojavaj()
 
    def _mb_slag_odbrojavaj(self):
        self.mb_lbl_timer.config(text=f"{self._mb_timer_vrijede}")
        self.mb_lbl_timer.config(
            fg=CRVENA if self._mb_timer_vrijede <= 15 else ZLATNA)
 
        if self._mb_timer_vrijede <= 0:
            self._mb_slag_vrijeme_isteklo()
            return
 
        self._mb_timer_vrijede -= 1
        self._mb_timer_id = self.root.after(1000, self._mb_slag_odbrojavaj)
 
    def _mb_slag_vrijeme_isteklo(self):
        self.mb_lbl_timer.config(text="0", fg=CRVENA)
        if self._mb_unos_aktivan:
            self.root.after(300, self._mb_slag_klik_potvrdi)
    
    # ══════════════════════════════════════════
    #  SKOCKO UI
    # ══════════════════════════════════════════
    def _build_sk_ekran(self):
        f = self.sk_frame
 
        # ── Naslov ───────────────────────────────────────────────
        self.sk_lbl_naslov = tk.Label(f, text="S K O Č K O",
                                      bg=BG_TAMNA, fg=ZLATNA,
                                      font=self.f_bodovi)
        self.sk_lbl_naslov.pack(pady=(2, 0))

 
        # ── Bodovi ───────────────────────────────────────────────
        info_row = tk.Frame(f, bg=BG_TAMNA)
        info_row.pack(pady=(0, 2))

        self.sk_lbl_bodovi = tk.Label(info_row, text="Bodovi: 0", bg=BG_TAMNA,
                                      fg=ZLATNA, font=self.f_bodovi)
        self.sk_lbl_bodovi.pack(side="left", padx=(40, 0))

        tk.Frame(info_row, bg=BG_TAMNA, width=200).pack(side="left")

        if self._ikona_sat:
            self.sk_lbl_sat = tk.Label(info_row, image=self._ikona_sat, bg=BG_TAMNA)
            self.sk_lbl_sat.pack(side="left", padx=(0, 4))
        else:
            self.sk_lbl_sat = None
        self.sk_lbl_timer = tk.Label(info_row, text="120", bg=BG_TAMNA, fg=ZLATNA, font=self.f_bodovi)
        self.sk_lbl_timer.pack(side="left")
 
        # ── Prostor za rezultat (između bodova i matrice) ─────────
        self.sk_rezultat_frame = tk.Frame(f, bg=BG_TAMNA)
        self.sk_rezultat_frame.pack(pady=(0, 2))

        # ── Glavni sadržaj: matrica + kontrole ───────────────────
        content = tk.Frame(f, bg=BG_TAMNA)
        content.pack(expand=True, pady=0)
        
        # Lijevo: matrica 6×4 pokušaja
        self.sk_matrica_frame = tk.Frame(content, bg=BG_TAMNA)
        self.sk_matrica_frame.pack(side="left", padx=(40, 10))
 
        # Desno: red s dugmadima za unos
        self.sk_unos_frame = tk.Frame(content, bg=BG_TAMNA)
        self.sk_unos_frame.pack(side="left", padx=(10, 40), anchor="n")
 
        # Izgradnja matrice – 6 redova × 4 ćelije + 1 za potvrdi/krugove
        self.sk_redovi_canvas = []   # po jedan Frame za svaki red
        self.sk_redovi_labele = []   # 4 Label-a po redu (za ikonicu)
        self.sk_redovi_foto   = []   # čuvamo PhotoImage reference
        self.sk_redovi_hint   = []   # Frame za hintnove krugove
        self.sk_redovi_btn    = []   # gumb "Potvrdi" po redu
 
        for red in range(Skocko.MAX_POKUSAJA):
            red_frame = tk.Frame(self.sk_matrica_frame, bg=BG_TAMNA)
            red_frame.pack(pady=1)

            labele = []
            foto   = [None] * Skocko.DUZINA

            for kol in range(Skocko.DUZINA):
                cell_frame = tk.Frame(red_frame, width=80, height=80, bg=BG_KARTICA,
                                      highlightbackground="#334455", highlightthickness=1)
                cell_frame.pack_propagate(False)
                cell_frame.pack(side="left", padx=2, pady=1)
                lbl = tk.Label(cell_frame, image="", bg=BG_KARTICA)
                lbl.place(relx=0.5, rely=0.5, anchor="center")
                labele.append(lbl)

            tk.Frame(red_frame, bg=BG_TAMNA, width=16).pack(side="left")

            # Hint frame
            hint_frame = tk.Frame(red_frame, bg=BG_TAMNA)

            # Jedan placeholder dovoljno širok za hint (4 kruga × ~30px)
            placeholder = tk.Frame(red_frame, bg=BG_TAMNA, width=130, height=34)
            placeholder.pack_propagate(False)
            placeholder.pack(side="left", padx=8)

            # Hint frame unutar placeholdera
            hint_frame = tk.Frame(placeholder, bg=BG_TAMNA)
            hint_frame.place(relx=0, rely=0.5, anchor="w")

            # Potvrdi dugme unutar istog placeholdera
            btn_potvrdi = tk.Button(placeholder, text="POTVRDI",
                                    bg=BTN_POTVRDI_BG, fg=BIJELA,
                                    activebackground=BTN_POTVRDI_HOV, activeforeground=BIJELA,
                                    font=self.f_sk_gumb, relief="flat", bd=0,
                                    cursor="hand2", padx=14, pady=6,
                                    command=lambda r=red: self._sk_slag_klik_potvrdi(r))
 
            self.sk_redovi_canvas.append(red_frame)
            self.sk_redovi_labele.append(labele)
            self.sk_redovi_foto.append(foto)
            self.sk_redovi_hint.append(hint_frame)
            self.sk_redovi_btn.append(btn_potvrdi)
 
        # ── Dugmad za unos znakova (6 dugmeta) ───────────────────
        tk.Label(self.sk_unos_frame, text="UNOS", bg=BG_TAMNA,
                 fg=SIVA_SVIJETLA, font=self.f_maly).pack(pady=(0, 6))
 
        self.sk_btn_znakovi = []
        for naziv in Skocko.ZNAKOVI:
            btn = tk.Button(
                self.sk_unos_frame,
                image=self._ikona(naziv) or "",
                text=naziv if not self._ikona(naziv) else "",
                compound="top" if self._ikona(naziv) else "none",
                width=90, height=90,
                bg=BG_KARTICA, fg=ZLATNA,
                activebackground="#2D3F55",
                font=self.f_sk_gumb, relief="flat", bd=0,
                cursor="hand2", state="disabled",
                command=lambda n=naziv: self._sk_klik_znak(n)
            )
            btn.pack(pady=3)
            self.sk_btn_znakovi.append(btn)
 
        # Obrisi gumb
        tk.Frame(self.sk_unos_frame, bg=BG_TAMNA, height=10).pack()
        self.sk_btn_obrisi = tk.Button(
            self.sk_unos_frame, text="⌫  OBRIŠI",
            command=self._sk_slag_klik_obrisi,
            bg=BTN_OBRISI_BG, fg=BIJELA,
            activebackground="#8B3A3A", activeforeground=BIJELA,
            font=self.f_sk_gumb, relief="flat", bd=0,
            cursor="hand2", padx=10, pady=8, state="disabled"
        )
        self.sk_btn_obrisi.pack(pady=4)
 
    # ══════════════════════════════════════════
    #  SKOCKO – start
    # ══════════════════════════════════════════
    def _start_skocko(self):
        if self._mb_vrati_id:
            self.root.after_cancel(self._mb_vrati_id)
            self._mb_vrati_id = None
 
        self.skocko = Skocko()
        self._sk_reset_ekran()
        self._show_sk_ekran()
 
    def _sk_reset_ekran(self):
        self.sk_unos_frame.pack(side="left", padx=(10, 40), anchor="n")
        self.sk_lbl_bodovi.config(text=f"Bodovi: {self.igra.bodovi}")
        self.sk_lbl_timer.config(text="120", fg=ZLATNA)
 
        # Resetuj sva polja matrice
        for red in range(Skocko.MAX_POKUSAJA):
            for kol in range(Skocko.DUZINA):
                lbl = self.sk_redovi_labele[red][kol]
                lbl.config(image="", bg=BG_KARTICA, width=80, height=80)
                self.sk_redovi_foto[red][kol] = None
 
            # Sakrij hint i potvrdi
            self.sk_redovi_hint[red].place_forget()
            self.sk_redovi_btn[red].place_forget()
 
        # Aktiviraj dugmad za unos
        for btn in self.sk_btn_znakovi:
            btn.config(state="normal")
        self.sk_btn_obrisi.config(state="normal")
 
        # Počisti rezultat frame (ne sakrivati — stalno je između bodova i matrice)
        self.sk_rezultat_frame.pack_forget()
        for w in self.sk_rezultat_frame.winfo_children():
            w.destroy()
 
        # Pokaži Potvrdi gumb za prvi red
        self._sk_osvjezi_aktivni_red()
        self._sk_vrijede = 120
        self._sk_pokreni_slag_timer()
 
    def _sk_osvjezi_aktivni_red(self):
        """Osvježi prikaz trenutnog reda — pokaži Potvrdi gumb ako je unos potpun."""
        if self.skocko is None or self.skocko.gotovo:
            return
        red = len(self.skocko.pokusaji)
        if red >= Skocko.MAX_POKUSAJA:
            return
        if self.skocko.unos_potpun():
            self.sk_redovi_btn[red].place(relx=0, rely=0, relwidth=1, relheight=1)
        else:
            self.sk_redovi_btn[red].place_forget()
 
    # ══════════════════════════════════════════
    #  SKOČKO – klik znaka
    # ══════════════════════════════════════════
    def _sk_klik_znak(self, naziv: str):
        if self.skocko is None or self.skocko.gotovo:
            return
        if not self.skocko.dodaj_znak(naziv):
            return
 
        red = len(self.skocko.pokusaji)
        kol = len(self.skocko.trenutni_unos) - 1
 
        # Postavi ikonicu u ćeliju
        lbl   = self.sk_redovi_labele[red][kol]
        ikona = self._ikona(naziv)
        if ikona:
            lbl.config(image=ikona, bg=BG_KARTICA)
            self.sk_redovi_foto[red][kol] = ikona
        else:
            lbl.config(text=naziv, bg=BG_KARTICA, fg=ZLATNA)
 
        self._sk_osvjezi_aktivni_red()
 
    # ══════════════════════════════════════════
    #  SKOČKO – klik obriši
    # ══════════════════════════════════════════
    def _sk_slag_klik_obrisi(self):
        if self.skocko is None or self.skocko.gotovo:
            return
        if not self.skocko.trenutni_unos:
            return
 
        red = len(self.skocko.pokusaji)
        kol = len(self.skocko.trenutni_unos) - 1
 
        self.skocko.obrisi_zadnji()
 
        # Očisti ćeliju — postavi prazan image
        lbl = self.sk_redovi_labele[red][kol]
        lbl.config(image="", bg=BG_KARTICA)
        self.sk_redovi_foto[red][kol] = None
 
        self._sk_osvjezi_aktivni_red()
 
    # ══════════════════════════════════════════
    #  SKOČKO – klik potvrdi (po redu)
    # ══════════════════════════════════════════
    def _sk_slag_klik_potvrdi(self, red: int):
        if self.skocko is None or self.skocko.gotovo:
            return
        if len(self.skocko.pokusaji) != red:
            return  # zaštita
        if not self.skocko.unos_potpun():
            return
 
        boje = self.skocko.potvrdi_pokusaj()
 
        # Sakrij Potvrdi gumb za ovaj red
        self.sk_redovi_btn[red].place_forget()
 
        # Nacrtaj hint krugove
        hint_frame = self.sk_redovi_hint[red]
        # Počisti stari sadržaj (ne bi trebao biti, ali sigurnosti radi)
        for w in hint_frame.winfo_children():
            w.destroy()
 
        boja_mapa = {
            'crvena': CRVENA,
            'zuta':   ZLATNA,
            None:     BG_KARTICA
        }
        for boja in boje:
            canvas = tk.Canvas(hint_frame,
                               width=26, height=26,
                               bg=BG_TAMNA, highlightthickness=0)
            canvas.pack(side="left", padx=2)
            fill = boja_mapa.get(boja, BG_KARTICA)
            canvas.create_oval(2, 2, 24, 24,
                               fill=fill,
                               outline="#111827",
                               width=1)
 
        hint_frame.place(relx=0, rely=0.5, anchor="w")
 
        # Provjeri završetak
        if self.skocko.gotovo:
            self._sk_zavrsi()
        else:
            # Aktiviraj sljedeći red (samo osvježi stanje)
            self._sk_osvjezi_aktivni_red()
            
    # ══════════════════════════════════════════
    #  SKOČKO – timer
    # ══════════════════════════════════════════
    def _sk_pokreni_slag_timer(self):
        if self._sk_timer_id:
            self.root.after_cancel(self._sk_timer_id)
        self._sk_slag_odbrojavaj()

    def _sk_slag_odbrojavaj(self):
        self.sk_lbl_timer.config(text=f"{self._sk_vrijede}")
        self.sk_lbl_timer.config(fg=CRVENA if self._sk_vrijede <= 15 else ZLATNA)

        if self._sk_vrijede <= 0:
            self._sk_slag_vrijeme_isteklo()
            return

        self._sk_vrijede -= 1
        self._sk_timer_id = self.root.after(1000, self._sk_slag_odbrojavaj)

    def _sk_slag_vrijeme_isteklo(self):
        self.sk_lbl_timer.config(text="0", fg=CRVENA)
        if self.skocko and not self.skocko.gotovo:
            self.skocko.gotovo = True
            self.skocko.pobjeda = False
            self._sk_zavrsi()
            
    # ══════════════════════════════════════════
    #  SKOČKO – završetak
    # ══════════════════════════════════════════
    def _sk_zavrsi(self):
        # Zaustavi timer
        if self._sk_timer_id:
            self.root.after_cancel(self._sk_timer_id)
            self._sk_timer_id = None
        self.sk_lbl_timer.config(text="")
        if self.sk_lbl_sat:
            self.sk_lbl_sat.pack_forget()

        # Onemogući unos
        for btn in self.sk_btn_znakovi:
            btn.config(state="disabled")
        self.sk_btn_obrisi.config(state="disabled")

        # Sakrij UNOS panel
        self.sk_unos_frame.pack_forget()

        zaradjeno = 0
        if self.skocko.pobjeda:
            zaradjeno = self.skocko.bodovi_za_pokusaj()
            self.igra.dodaj_bodove(zaradjeno)

        if self.igra.bodovi > self._highscore:
            self._highscore = self.igra.bodovi
            Slagalica.spremi_highscore(self._putanja_highscore, self._highscore)
            self.main_screen.azuriraj_highscore(self._highscore)

        self.sk_lbl_bodovi.config(text=f"Bodovi: {self.igra.bodovi}")
        self._sk_prikazi_rezultate(zaradjeno)
 
    # ══════════════════════════════════════════
    #  SKOCKO – prikaz rezultata
    # ══════════════════════════════════════════
    def _sk_prikazi_rezultate(self, zaradjeno: int):
        for w in self.sk_rezultat_frame.winfo_children():
            w.destroy()
        self.sk_rezultat_frame.pack(after=self.sk_lbl_naslov, pady=(0, 2))

        center = tk.Frame(self.sk_rezultat_frame, bg=BG_TAMNA)
        center.pack()

        if self.skocko.pobjeda:
            poruka = f"Bravo! Pogodili ste kombinaciju!  +{zaradjeno} bodova"
            boja   = ZELENA
        else:
            poruka = "Niste pogodili. Tačna kombinacija je bila:"
            boja   = CRVENA
        
        tk.Label(center, text=poruka, bg=BG_TAMNA, fg=boja,
                 font=self.f_rezultat).pack(pady=(0, 30))

        kom_frame = tk.Frame(center, bg=BG_PANEL, padx=14, pady=8)
        kom_frame.pack(side="left")

        for naziv in self.skocko.kombinacija:
            ikona = self._ikona(naziv)
            if ikona:
                lbl = tk.Label(kom_frame, image=ikona, bg=BG_PANEL)
                lbl.image = ikona
            else:
                lbl = tk.Label(kom_frame, text=naziv, bg=BG_PANEL,
                           fg=ZLATNA, font=self.f_rezultat)
            lbl.pack(side="left", padx=3)

        tk.Label(center, text="Sledeća igra: Ko zna zna", bg=BG_TAMNA, fg=NARANCASTA,
                 font=self.f_status).pack(side="left", padx=(20, 0))

        self._sk_vrati_id = self.root.after(5000, self._start_ko_zna_zna)
 
    def _sk_vrati_na_main(self):
        self._sk_vrati_id = None
        self.igra.reset()
        self.skocko = None
        self._show_main_screen()
        
    # ══════════════════════════════════════════
    #  KO ZNA ZNA – izgradnja UI
    # ══════════════════════════════════════════
    def _build_kzz_ekran(self):
        f = self.kzz_frame

        top_row = tk.Frame(f, bg=BG_TAMNA)
        top_row.pack(fill="x", padx=60, pady=(8, 0))

        self.kzz_lbl_bodovi = tk.Label(top_row, text="Bodovi: 0", bg=BG_TAMNA,
                                       fg=ZLATNA, font=self.f_bodovi)
        self.kzz_lbl_bodovi.pack(side="left")

        kzz_timer_frame = tk.Frame(top_row, bg=BG_TAMNA)
        kzz_timer_frame.pack(side="right")
        if self._ikona_sat:
            self.kzz_lbl_sat = tk.Label(kzz_timer_frame, image=self._ikona_sat, bg=BG_TAMNA)
            self.kzz_lbl_sat.pack(side="left", padx=(0, 4))
        else:
            self.kzz_lbl_sat = None
        self.kzz_lbl_timer = tk.Label(kzz_timer_frame, text="10", bg=BG_TAMNA, fg=ZLATNA, font=self.f_bodovi)
        self.kzz_lbl_timer.pack(side="left")

        self.kzz_lbl_broj_pitanja = tk.Label(f, text="", bg=BG_TAMNA,
                                             fg=SIVA_SVIJETLA, font=self.f_maly)
        self.kzz_lbl_broj_pitanja.pack(pady=(2, 0))

        self.kzz_lbl_feedback = tk.Label(f, text="", bg=BG_TAMNA, fg=BIJELA, font=self.f_rezultat)
        self.kzz_lbl_feedback.pack(pady=(2, 0))

        pitanje_outer = tk.Frame(f, bg=BG_PANEL, padx=40, pady=24)
        pitanje_outer.pack(fill="x", padx=60, pady=(8, 16))

        self.kzz_lbl_pitanje = tk.Label(pitanje_outer, text="",
                                     bg=BG_PANEL, fg=BIJELA,
                                     font=self.f_rezultat,
                                     wraplength=1600, justify="center")
        self.kzz_lbl_pitanje.pack()

        matrica_frame = tk.Frame(f, bg=BG_TAMNA)
        matrica_frame.pack(pady=(0, 10))

        self.kzz_btn_odgovori = []
        for red in range(2):
            red_frame = tk.Frame(matrica_frame, bg=BG_TAMNA)
            red_frame.pack()
            for kol in range(2):
                idx = red * 2 + kol
                btn = tk.Button(red_frame, text="", width=40, height=3, bg=BG_KARTICA, fg=BIJELA,
                                activebackground=ZLATNA_TAMNA, activeforeground=BG_TAMNA, font=self.f_status,
                                relief="flat", bd=0, cursor="hand2", wraplength=500, justify="center",
                                command=lambda i=idx: self._kzz_klik_odgovor(i))
                btn.pack(side="left", padx=8, pady=6)
                self.kzz_btn_odgovori.append(btn)

        self.kzz_btn_preskoci = tk.Button(f, text="PRESKOCI", command=self._kzz_klik_preskoci,
                                          bg="#374151", fg=BIJELA, activebackground="#1F2937",
                                          activeforeground=BIJELA, font=self.f_gumb, relief="flat", bd=0,
                                          cursor="hand2", padx=40, pady=12)
        self.kzz_btn_preskoci.pack(pady=(4, 0))

    # ══════════════════════════════════════════
    #  KO ZNA ZNA – start
    # ══════════════════════════════════════════
    def _start_ko_zna_zna(self):
        if self._sk_vrati_id:
            self.root.after_cancel(self._sk_vrati_id)
            self._sk_vrati_id = None

        self.ko_zna_zna = KoZnaZna(self._putanja_db)
        self._show_kzz_ekran()
        self._kzz_prikazi_pitanje()

    # ══════════════════════════════════════════
    #  KO ZNA ZNA – prikaz pitanja
    # ══════════════════════════════════════════
    def _kzz_prikazi_pitanje(self):
        if self._kzz_timer_id:
            self.root.after_cancel(self._kzz_timer_id)
            self._kzz_timer_id = None

        kzz = self.ko_zna_zna
        if kzz.gotovo():
            self._kzz_zavrsi()
            return

        pit = kzz.trenutno_pitanje()
        br  = kzz.trenutni_idx + 1
        uk  = kzz.ukupno()

        self.kzz_lbl_bodovi.config(text=f"Bodovi: {self.igra.bodovi}")
        self.kzz_lbl_broj_pitanja.config(text=f"Pitanje {br} / {uk}")
        self.kzz_lbl_pitanje.config(text=pit["pitanje"], fg=BIJELA)
        self.kzz_lbl_feedback.config(text="")

        for i, btn in enumerate(self.kzz_btn_odgovori):
            btn.config(text=pit["odgovori"][i], bg=BG_KARTICA,
                       fg=BIJELA, state="normal")

        self.kzz_btn_preskoci.config(state="normal")

        self._kzz_vrijede = 10
        self.kzz_lbl_timer.config(text="10", fg=ZLATNA)
        self._kzz_slag_odbrojavaj()

    # ══════════════════════════════════════════
    #  KO ZNA ZNA – timer
    # ══════════════════════════════════════════
    def _kzz_slag_odbrojavaj(self):
        self.kzz_lbl_timer.config(text=f"{self._kzz_vrijede}")
        self.kzz_lbl_timer.config(fg=CRVENA if self._kzz_vrijede <= 3 else ZLATNA)

        if self._kzz_vrijede <= 0:
            self._kzz_klik_preskoci()
            return

        self._kzz_vrijede -= 1
        self._kzz_timer_id = self.root.after(1000, self._kzz_slag_odbrojavaj)

    # ══════════════════════════════════════════
    #  KO ZNA ZNA – klik odgovor
    # ══════════════════════════════════════════
    def _kzz_klik_odgovor(self, idx: int):
        if self.ko_zna_zna is None or self.ko_zna_zna.gotovo():
            return

        if self._kzz_timer_id:
            self.root.after_cancel(self._kzz_timer_id)
            self._kzz_timer_id = None

        pit      = self.ko_zna_zna.trenutno_pitanje()
        odgovor  = pit["odgovori"][idx]
        tacan    = pit["tacan"]
        zaradjeno = self.ko_zna_zna.odgovori(odgovor)
        self.igra.dodaj_bodove(zaradjeno)

        for i, btn in enumerate(self.kzz_btn_odgovori):
            if pit["odgovori"][i] == tacan:
                btn.config(bg=ZELENA, fg=BIJELA, state="disabled")
            elif i == idx and odgovor != tacan:
                btn.config(bg=CRVENA, fg=BIJELA, state="disabled")
            else:
                btn.config(state="disabled")

        self.kzz_btn_preskoci.config(state="disabled")

        if zaradjeno > 0:
            self.kzz_lbl_feedback.config(text=f"+{zaradjeno} bodova", fg=ZELENA)
        else:
            self.kzz_lbl_feedback.config(text=f"{zaradjeno} boda", fg=CRVENA)

        self.kzz_lbl_bodovi.config(text=f"Bodovi: {self.igra.bodovi}")

        if self.igra.bodovi > self._highscore:
            self._highscore = self.igra.bodovi
            Slagalica.spremi_highscore(self._putanja_highscore, self._highscore)
            self.main_screen.azuriraj_highscore(self._highscore)

        if self.ko_zna_zna.gotovo():
            self.root.after(1500, self._kzz_zavrsi)
        else:
            self.root.after(1500, self._kzz_prikazi_pitanje)

    # ══════════════════════════════════════════
    #  KO ZNA ZNA – preskoči
    # ══════════════════════════════════════════
    def _kzz_klik_preskoci(self):
        if self.ko_zna_zna is None or self.ko_zna_zna.gotovo():
            return

        if self._kzz_timer_id:
            self.root.after_cancel(self._kzz_timer_id)
            self._kzz_timer_id = None

        pit = self.ko_zna_zna.trenutno_pitanje()
        if pit is None:
            return
        self.ko_zna_zna.preskoči()

        for btn in self.kzz_btn_odgovori:
            btn.config(state="disabled")
        self.kzz_btn_preskoci.config(state="disabled")
        
        for i, btn in enumerate(self.kzz_btn_odgovori):
            if pit["odgovori"][i] == pit["tacan"]:
                btn.config(bg=ZELENA, fg=BIJELA)
                break

        self.kzz_lbl_feedback.config(text="Preskoceno", fg=SIVA_SVIJETLA)

        if self.ko_zna_zna.gotovo():
            self.root.after(1500, self._kzz_zavrsi)
        else:
            self.root.after(1500, self._kzz_prikazi_pitanje)

    # ══════════════════════════════════════════
    #  KO ZNA ZNA – završetak
    # ══════════════════════════════════════════
    def _kzz_zavrsi(self):
        if self._kzz_timer_id:
            self.root.after_cancel(self._kzz_timer_id)
            self._kzz_timer_id = None

        self.kzz_lbl_timer.config(text="")
        if self.kzz_lbl_sat:
            self.kzz_lbl_sat.pack_forget()

        for btn in self.kzz_btn_odgovori:
            btn.config(state="disabled")
        self.kzz_btn_preskoci.config(state="disabled")

        if self.igra.bodovi > self._highscore:
            self._highscore = self.igra.bodovi
            Slagalica.spremi_highscore(self._putanja_highscore, self._highscore)
            self.main_screen.azuriraj_highscore(self._highscore)

        self.kzz_lbl_feedback.config(text=f"Kraj igre!  Ukupni bodovi: {self.igra.bodovi}", fg=ZLATNA)
        self.kzz_lbl_pitanje.config(text="Sledeca igra: Spojnice", fg=NARANCASTA)
        self.kzz_lbl_broj_pitanja.config(text="")

        self._kzz_vrati_id = self.root.after(5000, self._start_spojnice)
    
    # ══════════════════════════════════════════
    #  SPOJNICE – izgradnja UI
    # ══════════════════════════════════════════
    def _build_sp_ekran(self):
        f = self.sp_frame

        # ── Gornji red: bodovi + timer ────────────────────────────
        top_row = tk.Frame(f, bg=BG_TAMNA)
        top_row.pack(fill="x", padx=60, pady=(8, 0))

        self.sp_lbl_bodovi = tk.Label(top_row, text="Bodovi: 0",
                                      bg=BG_TAMNA, fg=ZLATNA, font=self.f_bodovi)
        self.sp_lbl_bodovi.pack(side="left")

        sp_timer_frame = tk.Frame(top_row, bg=BG_TAMNA)
        sp_timer_frame.pack(side="right")
        if self._ikona_sat:
            self.sp_lbl_sat = tk.Label(sp_timer_frame, image=self._ikona_sat, bg=BG_TAMNA)
            self.sp_lbl_sat.pack(side="left", padx=(0, 4))
        else:
            self.sp_lbl_sat = None
        self.sp_lbl_timer = tk.Label(sp_timer_frame, text="90",
                                     bg=BG_TAMNA, fg=ZLATNA, font=self.f_bodovi)
        self.sp_lbl_timer.pack(side="left")

        # ── Tema (višeredni label) ────────────────────────────────
        self.sp_lbl_tema = tk.Label(f, text="",
                                    bg=BG_PANEL, fg=BIJELA,
                                    font=self.f_rezultat,
                                    wraplength=1600, justify="center",
                                    padx=40, pady=16)
        self.sp_lbl_tema.pack(fill="x", padx=60, pady=(10, 8))

        # ── Feedback label ────────────────────────────────────────
        self.sp_lbl_feedback = tk.Label(f, text="",
                                        bg=BG_TAMNA, fg=BIJELA,
                                        font=self.f_status)
        self.sp_lbl_feedback.pack(pady=(0, 4))

        # ── Glavni sadržaj: pojmovi (lijevo) + odgovori (desno) ───
        self.sp_content = tk.Frame(f, bg=BG_TAMNA)
        self.sp_content.pack(expand=True, fill="both", padx=60, pady=(0, 10))

        self.sp_lijevo_frame = tk.Frame(self.sp_content, bg=BG_TAMNA)
        self.sp_lijevo_frame.pack(side="left", expand=True, fill="both", padx=(0, 30))

        self.sp_desno_frame = tk.Frame(self.sp_content, bg=BG_TAMNA)
        self.sp_desno_frame.pack(side="left", expand=True, fill="both", padx=(30, 0))

    # ══════════════════════════════════════════
    #  SPOJNICE – start
    # ══════════════════════════════════════════
    def _start_spojnice(self):
        if self._kzz_vrati_id:
            self.root.after_cancel(self._kzz_vrati_id)
            self._kzz_vrati_id = None

        self.spojnice = Spojnice(self._putanja_spojnice_db)
        self._sp_odabrani_pojam = None
        self._sp_anim_running   = False
        self._sp_vrijede        = 90

        self._sp_reset_ekran()
        self._show_sp_ekran()
        self._sp_pokreni_timer()

    def _sp_reset_ekran(self):
        sp = self.spojnice
        
        for w in self.sp_desno_frame.winfo_children():
            w.place_forget()
        if not self.sp_desno_frame.winfo_ismapped():
            self.sp_desno_frame.pack(side="left", expand=True,fill="both", padx=(30, 0))
        self.sp_lbl_bodovi.config(text=f"Bodovi: {self.igra.bodovi}")
        self.sp_lbl_timer.config(text="90", fg=ZLATNA)
        self.sp_lbl_tema.config(text=sp.tema)
        self.sp_lbl_feedback.config(text="")

        if self.sp_lbl_sat:
            self.sp_lbl_sat.pack(side="left", padx=(0, 4))

        # Počisti stara dugmad
        for w in self.sp_lijevo_frame.winfo_children():
            w.destroy()
        for w in self.sp_desno_frame.winfo_children():
            w.destroy()

        self._sp_pojam_dugmad   = {}
        self._sp_odgovor_dugmad = {}
        self._sp_pojam_redovi   = {}   # pojam -> tk.Frame (red u lijevo_frame)
        self._sp_odgovor_redovi = {}   # odgovor -> tk.Frame (red u desno_frame)

        pojmovi   = list(sp.parovi.keys())
        odgovori  = list(sp.parovi.values())
        random.shuffle(pojmovi)
        random.shuffle(odgovori)

        # Čuvamo originalni redosljed prikaza za animaciju
        self._sp_pojam_redosljed   = pojmovi[:]
        self._sp_odgovor_redosljed = odgovori[:]

        for pojam in pojmovi:
            row = tk.Frame(self.sp_lijevo_frame, bg=BG_TAMNA)
            row.pack(fill="x", pady=3)
            btn = tk.Button(row, text=pojam,
                            bg=BG_KARTICA, fg=BIJELA,
                            activebackground=ZLATNA_TAMNA, activeforeground=BG_TAMNA,
                            font=self.f_status, relief="flat", bd=0,
                            cursor="hand2", anchor="center",
                            padx=20, pady=10,
                            wraplength=580, justify="center",
                            command=lambda p=pojam: self._sp_klik_pojam(p))
            btn.pack(fill="x")
            self._sp_pojam_dugmad[pojam]  = btn
            self._sp_pojam_redovi[pojam]  = row

        for odgovor in odgovori:
            row = tk.Frame(self.sp_desno_frame, bg=BG_TAMNA)
            row.pack(fill="x", pady=3)
            btn = tk.Button(row, text=odgovor,
                            bg=BG_KARTICA, fg=BIJELA,
                            activebackground=ZLATNA_TAMNA, activeforeground=BG_TAMNA,
                            font=self.f_status, relief="flat", bd=0,
                            cursor="hand2", anchor="center",
                            padx=20, pady=10,
                            wraplength=580, justify="center",
                            command=lambda o=odgovor: self._sp_klik_odgovor(o))
            btn.pack(fill="x")
            self._sp_odgovor_dugmad[odgovor] = btn
            self._sp_odgovor_redovi[odgovor] = row

    # ══════════════════════════════════════════
    #  SPOJNICE – klik pojma (lijevo)
    # ══════════════════════════════════════════
    def _sp_klik_pojam(self, pojam: str):
        if self.spojnice is None or self._sp_anim_running:
            return
        # Ako je već spojen/onemogućen, ignoriši
        if self.spojnice.parovi.get(pojam) and pojam in self.spojnice.spojeno:
            return

        # Deselektuj prethodni
        if self._sp_odabrani_pojam and self._sp_odabrani_pojam in self._sp_pojam_dugmad:
            prev_btn = self._sp_pojam_dugmad[self._sp_odabrani_pojam]
            if str(prev_btn['state']) != 'disabled':
                prev_btn.config(bg=BG_KARTICA, fg=BIJELA)

        if self._sp_odabrani_pojam == pojam:
            # Deselektovanje
            self._sp_odabrani_pojam = None
            self.sp_lbl_feedback.config(text="")
        else:
            # Selektovanje novog
            self._sp_odabrani_pojam = pojam
            btn = self._sp_pojam_dugmad[pojam]
            btn.config(bg=ZLATNA, fg=BG_TAMNA)
            self.sp_lbl_feedback.config(
                text=f"Odabrano: {pojam}  →  kliknite odgovor", fg=ZLATNA)

    # ══════════════════════════════════════════
    #  SPOJNICE – klik odgovora (desno)
    # ══════════════════════════════════════════
    def _sp_klik_odgovor(self, odgovor: str):
        if self.spojnice is None or self._sp_anim_running:
            return
        if self._sp_odabrani_pojam is None:
            self.sp_lbl_feedback.config(text="Prvo odaberite pojam s lijeve strane!", fg=CRVENA)
            return

        pojam = self._sp_odabrani_pojam
        tacan = self.spojnice.parovi.get(pojam) == odgovor

        btn_pojam   = self._sp_pojam_dugmad.get(pojam)
        btn_odgovor = self._sp_odgovor_dugmad.get(odgovor)

        if tacan:
            self.spojnice.spojeno[pojam] = odgovor
            self.spojnice.bodovi += Spojnice.BODOVI_TACNO
            self.igra.dodaj_bodove(Spojnice.BODOVI_TACNO)
            self.sp_lbl_bodovi.config(text=f"Bodovi: {self.igra.bodovi}")
            if btn_pojam:
                btn_pojam.config(bg=ZELENA, fg=BIJELA, state="disabled", cursor="arrow")
            if btn_odgovor:
                btn_odgovor.config(bg=ZELENA, fg=BIJELA, state="disabled", cursor="arrow")
            self.sp_lbl_feedback.config(text=f"✔  Tačno! +{Spojnice.BODOVI_TACNO} bodova", fg=ZELENA)
        else:
        # POGREŠNO — samo resetuj selekciju, NE onemogućuj pojam!
            if btn_pojam:
                btn_pojam.config(bg=CRVENA, fg=BIJELA, state="disabled", cursor="arrow")
            if btn_odgovor:
            # Kratko pokaži crvenu, pa vrati na normalu
                btn_odgovor.config(bg=CRVENA, fg=BIJELA)
                self.root.after(600, lambda b=btn_odgovor: b.config(bg=BG_KARTICA, fg=BIJELA)
                                if str(b['state']) != 'disabled' else None)
            self.sp_lbl_feedback.config(text="✘  Pogrešno! Pokušajte ponovo.", fg=CRVENA)

        self._sp_odabrani_pojam = None
        self.spojnice.odabrani_pojam = None

        if self.igra.bodovi > self._highscore:
            self._highscore = self.igra.bodovi
            Slagalica.spremi_highscore(self._putanja_highscore, self._highscore)
            self.main_screen.azuriraj_highscore(self._highscore)

        # Završi samo kad su SVI PAROVI tačno spojeni
        sva_disabled = all(str(btn['state']) == 'disabled' for btn in self._sp_pojam_dugmad.values())
        if sva_disabled:
            self.root.after(800, lambda: self._sp_zavrsi(isteklo=False))

    # ══════════════════════════════════════════
    #  SPOJNICE – timer
    # ══════════════════════════════════════════
    def _sp_pokreni_timer(self):
        if self._sp_timer_id:
            self.root.after_cancel(self._sp_timer_id)
        self._sp_odbrojavaj()

    def _sp_odbrojavaj(self):
        self.sp_lbl_timer.config(text=f"{self._sp_vrijede}")
        self.sp_lbl_timer.config(fg=CRVENA if self._sp_vrijede <= 15 else ZLATNA)

        if self._sp_vrijede <= 0:
            self._sp_zavrsi(isteklo=True)
            return

        self._sp_vrijede -= 1
        self._sp_timer_id = self.root.after(1000, self._sp_odbrojavaj)

    # ══════════════════════════════════════════
    #  SPOJNICE – završetak
    # ══════════════════════════════════════════
    def _sp_zavrsi(self, isteklo: bool = False):
        if self._sp_anim_running:
            return
        if self._sp_timer_id:
            self.root.after_cancel(self._sp_timer_id)
            self._sp_timer_id = None

        self.sp_lbl_timer.config(text="")
        if self.sp_lbl_sat:
            self.sp_lbl_sat.pack_forget()

        # Onemogući sva preostala dugmad
        for btn in self._sp_pojam_dugmad.values():
            if str(btn['state']) != 'disabled':
                btn.config(state="disabled", cursor="arrow")
        for btn in self._sp_odgovor_dugmad.values():
            if str(btn['state']) != 'disabled':
                btn.config(state="disabled", cursor="arrow")

        if isteklo:
            self.sp_lbl_feedback.config(text="Vrijeme je isteklo!", fg=CRVENA)

        self._sp_anim_running = True
        self.root.after(600, self._sp_prikazi_rjesenja)

    def _sp_prikazi_rjesenja(self):
        sp = self.spojnice

        for w in self.sp_desno_frame.winfo_children():
            w.destroy()

        for pojam in self._sp_pojam_redosljed:
            odgovor = sp.parovi.get(pojam)
            if not odgovor:
                continue

            btn_pojam = self._sp_pojam_dugmad.get(pojam)
            bg_boja = btn_pojam.cget("bg") if btn_pojam else BG_KARTICA
            btn_h = btn_pojam.winfo_height() if btn_pojam else 0

            row = tk.Frame(self.sp_desno_frame, bg=BG_TAMNA, height=btn_h)
            row.pack_propagate(False)
            row.pack(fill="x", pady=3)

            lbl = tk.Label(row, text=odgovor, bg=bg_boja, fg=BIJELA,
            font=self.f_status, anchor="center", justify="center",
            padx=20, pady=10, wraplength=580,)
            lbl.pack(fill="both", expand=True)

        self._sp_anim_running = False
        self._sp_prikazi_kraj()

    def _sp_prikazi_kraj(self):
        """Prikaz finalnog rezultata nakon animacije, zatim prelaz na main screen."""
        self.sp_lbl_feedback.config(
            text=f"Kraj igre Spojnice!  Ukupni bodovi: {self.igra.bodovi}  |  "
                 f"Sljedeća igra: Asocijacije",
            fg=NARANCASTA)
        spojeno_tacno = sum(1 for p in self.spojnice.parovi if p in self.spojnice.spojeno)
        self.sp_lbl_tema.config(text=f"Spojili ste {spojeno_tacno} /"
                                f"{len(self.spojnice.parovi)} parova  →  "
                                f"+{self.spojnice.bodovi} bodova u ovoj rundi", fg=ZLATNA)

        if self.igra.bodovi > self._highscore:
            self._highscore = self.igra.bodovi
            Slagalica.spremi_highscore(self._putanja_highscore, self._highscore)
            self.main_screen.azuriraj_highscore(self._highscore)

        self._sp_vrati_id = self.root.after(5000, self._sp_vrati_na_main)

    def _sp_vrati_na_main(self):
        self._sp_vrati_id = None
        self.igra.reset()
        self.spojnice = None
        self._show_main_screen()
 
    # ══════════════════════════════════════════
    #  Hover
    # ══════════════════════════════════════════
    def _dodaj_hover(self, widget, normal_bg, hover_bg):
        widget.bind("<Enter>",
                    lambda e: widget.config(bg=hover_bg)
                    if str(widget['state']) != 'disabled' else None)
        widget.bind("<Leave>",
                    lambda e: widget.config(bg=normal_bg)
                    if str(widget['state']) != 'disabled' else None)


# ─────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────
def main():
    root = tk.Tk()
    try:
        root.iconbitmap(default="")
    except Exception:
        pass
    SlagalicaApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()