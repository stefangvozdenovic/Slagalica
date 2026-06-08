""" SLAGALICA
=====================================
Klase:
  - Slagalica   : sva logika igre slova (abeceda, težine, rječnik, highscore, animacija, unos, provjera)
  - Igra         : praćenje bodova, stanje igre, potvrda riječi
  - MainScreen   : početni ekran, highscore, navigacija
  - SlagalicaApp : glavni GUI, orkestrator ekrana """

import tkinter as tk
from tkinter import font as tkfont
import random
import os

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
            return 5.0
        elif slovo in self.RIJETKA:
            return 1.0
        return 2.5
 
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



# ─────────────────────────────────────────────
#  Klasa  IGRA
# ─────────────────────────────────────────────
class Igra:
    def __init__(self):
        self.bodovi: int  = 0
        self.runda: int   = 0
        self.istorija: list = []

    def nova_runda(self):
        self.runda += 1

    def potvrdi_rijec(self, rijec_lista: list, ispravna: bool) -> int:
        if ispravna:
            zaradjeno = len(rijec_lista) * 2
            self.bodovi += zaradjeno
            rijec_str = "".join(rijec_lista)
            self.istorija.append((rijec_str, zaradjeno))
            return zaradjeno
        self.istorija.append(("".join(rijec_lista), 0))
        return 0

    def reset(self):
        self.bodovi = 0
        self.runda  = 0
        self.istorija.clear()


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
 
        self._rjecnik:   set = Slagalica.ucitaj_rjecnik(self._putanja_rjecnika)
        self._highscore: int = Slagalica.ucitaj_highscore(self._putanja_highscore)
 
        self.igra = Igra()
        self.slagalica: Slagalica = None
 
        self._igra_aktivna   = False
        self._unos_aktivan   = False
        self._animacija_aktivna = False
        self._animacija_id   = None
        self._timer_id      = None
        self._vrati_id      = None
        self.preostalo_vrijeme = 60
 
        self._def_fontovi()
        self._build_ui()
 
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
 
    # ══════════════════════════════════════════
    #  Izgradnja UI
    # ══════════════════════════════════════════
    def _build_ui(self):
        self.header_frame = tk.Frame(self.root, bg=BG_TAMNA, height=90)
        self.header_frame.pack(fill="x", pady=(10, 0))
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
            on_igraj=self._start_igra,
            on_izlaz=self.root.destroy,
            f_bodovi=self.f_bodovi,
            f_gumb=self.f_gumb,
            f_maly=self.f_maly,
            f_status=self.f_status
        )
 
        self.igra_frame = tk.Frame(self.container, bg=BG_TAMNA)
        self._build_igra_ekran()
 
        self.main_screen.show()
 
    def _build_igra_ekran(self):
        f = self.igra_frame
 
        self.lbl_timer = tk.Label(f, text="60",
                                  bg=BG_TAMNA, fg=ZLATNA,
                                  font=self.f_timer)
        self.lbl_timer.pack(pady=(8, 4))
 
        self.lbl_status = tk.Label(f, text="",
                                   bg=BG_TAMNA, fg=BIJELA,
                                   font=self.f_status,
                                   justify="center", wraplength=1400)
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
                btn = tk.Button(
                    row_frame,
                    textvariable=var,
                    width=4, height=2,
                    bg=BG_KARTICA, fg=ZLATNA,
                    activebackground=ZLATNA_TAMNA,
                    activeforeground=BG_TAMNA,
                    font=self.f_slovo,
                    relief="flat", bd=0,
                    cursor="hand2",
                    state="disabled",
                    command=lambda i=idx: self._klik_slovo(i)
                )
                btn.pack(side="left", padx=5, pady=5)
                self._dodaj_hover(btn, BG_KARTICA, "#2D3F55")
                self.dugmad.append(btn)
 
        self.kontrole_frame = tk.Frame(f, bg=BG_TAMNA)
        self.kontrole_frame.pack(pady=(0, 10))
 
        self.btn_potvrdi = tk.Button(
            self.kontrole_frame, text="✔  POTVRDI",
            command=self._klik_potvrdi,
            bg=BTN_POTVRDI_BG, fg=BIJELA,
            activebackground=BTN_POTVRDI_HOV, activeforeground=BIJELA,
            font=self.f_gumb, relief="flat", bd=0,
            cursor="hand2", padx=40, pady=14, state="disabled"
        )
        self.btn_potvrdi.pack(side="left", padx=12)
 
        self.btn_obrisi = tk.Button(
            self.kontrole_frame, text="⌫  OBRIŠI",
            command=self._klik_obrisi,
            bg=BTN_OBRISI_BG, fg=BIJELA,
            activebackground="#8B3A3A", activeforeground=BIJELA,
            font=self.f_gumb, relief="flat", bd=0,
            cursor="hand2", padx=30, pady=14, state="disabled"
        )
        self.btn_obrisi.pack(side="left", padx=12)
 
        self.rezultat_frame = tk.Frame(f, bg=BG_TAMNA)
 
    # ══════════════════════════════════════════
    #  Navigacija
    # ══════════════════════════════════════════
    def _show_main_screen(self):
        self.igra_frame.place_forget()
        self.main_screen.show()
 
    def _show_igra_ekran(self):
        self.main_screen.hide()
        self.igra_frame.place(relx=0, rely=0.08, relwidth=1, relheight=0.92)
 
    # ══════════════════════════════════════════
    #  Start igre
    # ══════════════════════════════════════════
    def _start_igra(self):
        # Otkaži eventualni zakazani povratak na main screen
        if self._vrati_id:
            self.root.after_cancel(self._vrati_id)
            self._vrati_id = None
        self._show_igra_ekran()
        self._reset_igra_ekran()
        self._nova_runda()
 
    def _reset_igra_ekran(self):
        self.lbl_status.config(text="", fg=BIJELA)
        self.lbl_unos.config(text="", fg=ZLATNA)
        self.lbl_rjecnik_status.config(text="")
        self.lbl_timer.config(text="60", fg=ZLATNA)
        self.btn_potvrdi.config(state="disabled")
        self.btn_obrisi.config(state="disabled")
 
        self.rezultat_frame.pack_forget()
        self.slova_outer.pack(pady=(0, 14))
        self.kontrole_frame.pack(pady=(0, 10))
 
        for i, btn in enumerate(self.dugmad):
            btn.config(state="disabled", bg=BG_KARTICA, fg=ZLATNA)
            self.var_slova[i].set("?")
 
    def _nova_runda(self):
        self._zaustavi_animaciju()
        self.igra.nova_runda()
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
            text="🎯  Kliknite na dugmad da fiksirate slova!", fg=BIJELA)
 
        self._pokreni_animaciju()
 
    # ══════════════════════════════════════════
    #  Animacija
    # ══════════════════════════════════════════
    def _pokreni_animaciju(self):
        self._animacija_aktivna = True
        self._animiraj()
 
    def _animiraj(self):
        if not self._animacija_aktivna or self.slagalica is None:
            return
        if self.slagalica.sva_fiksirana():
            return
        for i in range(12):
            if self.slagalica.fiksirana_slova[i] is None:
                self.slagalica.animacija_slova[i] = self.slagalica.random_jedno()
        self._osvjezi_slova(list(self.slagalica.animacija_slova))
        self._animacija_id = self.root.after(80, self._animiraj)
 
    def _zaustavi_animaciju(self):
        self._animacija_aktivna = False
        if self._animacija_id:
            self.root.after_cancel(self._animacija_id)
            self._animacija_id = None
        self._igra_aktivna = False
        if self._timer_id:
            self.root.after_cancel(self._timer_id)
            self._timer_id = None
 
    def _osvjezi_slova(self, slova: list):
        for i, s in enumerate(slova):
            if self.slagalica and self.slagalica.fiksirana_slova[i] is None:
                self.var_slova[i].set(s)
 
    # ══════════════════════════════════════════
    #  Klik na slovo
    # ══════════════════════════════════════════
    def _klik_slovo(self, idx: int):
        if not self._igra_aktivna or self.slagalica is None:
            return
 
        if not self._unos_aktivan:
            fiksirano = self.slagalica.fiksiraj_slovo(idx)
            if fiksirano:
                self.dugmad[idx].config(bg=FIKSIRANO_BG, fg=FIKSIRANO_FG)
                self.var_slova[idx].set(fiksirano)
 
            if self.slagalica.sva_fiksirana():
                self._zaustavi_animaciju()
                self._igra_aktivna = True
                self._unos_aktivan = True
                for i, btn in enumerate(self.dugmad):
                    btn.config(bg=BG_KARTICA, fg=ZLATNA,
                               cursor="hand2", state="normal")
                    self.var_slova[i].set(self.slagalica.fiksirana_slova[i])
                self.btn_potvrdi.config(state="normal")
                self.btn_obrisi.config(state="normal")
                self.lbl_status.config(
                    text="✏️  Kliknite slova da složite riječ, zatim POTVRDI",
                    fg=ZLATNA)
                self.preostalo_vrijeme = 60
                self.lbl_timer.config(text="60", fg=ZLATNA)
                self._pokreni_timer()
        else:
            slovo = self.slagalica.fiksirana_slova[idx]
            if slovo is None:
                return
            if self.slagalica.dodaj_slovo_u_unos(slovo):
                self.dugmad[idx].config(state="disabled",
                                        bg="#0F2030", fg="#334455")
                self._osvjezi_unos()
 
    # ══════════════════════════════════════════
    #  Unos
    # ══════════════════════════════════════════
    def _osvjezi_unos(self):
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
 
    def _klik_obrisi(self):
        if not self.slagalica or not self._unos_aktivan:
            return
        if not self.slagalica.unos:
            return
        zadnje = self.slagalica.unos[-1]   # zadnji token npr. 'Dž'
        self.slagalica.obrisi_zadnje()
        for i, btn in enumerate(self.dugmad):
            if (self.slagalica.fiksirana_slova[i] == zadnje
                    and str(btn['state']) == 'disabled'
                    and str(btn['bg']).lower() == "#0f2030"):
                btn.config(state="normal", bg=BG_KARTICA, fg=ZLATNA)
                break
        self._osvjezi_unos()
 
    # ══════════════════════════════════════════
    #  Potvrdi
    # ══════════════════════════════════════════
    def _klik_potvrdi(self):
        if not self.slagalica or not self._unos_aktivan:
            return
        unos_lista = self.slagalica.unos
        unos_str   = "".join(unos_lista)
        if not unos_lista:
            self.lbl_status.config(
                text="⚠️  Niste unijeli nijedno slovo!", fg=ZLATNA)
            return
 
        if self._timer_id:
            self.root.after_cancel(self._timer_id)
            self._timer_id = None
        self.lbl_timer.config(text="")
 
        ispravna  = self.slagalica.provjeri_rijec(unos_str)
        zaradjeno = self.igra.potvrdi_rijec(unos_lista, ispravna)
 
        self._unos_aktivan = False
        self._igra_aktivna = False
 
        self.slova_outer.pack_forget()
        self.kontrole_frame.pack_forget()
        self.lbl_status.config(text="")
        self.lbl_rjecnik_status.config(text="")
 
        self._prikazi_rezultate(unos_str, ispravna, zaradjeno)
 
    # ══════════════════════════════════════════
    #  Prikaz rezultata
    # ══════════════════════════════════════════
    def _prikazi_rezultate(self, unos: str, ispravna: bool, zaradjeno: int):
        for widget in self.rezultat_frame.winfo_children():
            widget.destroy()
 
        self.rezultat_frame.pack(fill="both", expand=True, pady=20)
 
        center = tk.Frame(self.rezultat_frame, bg=BG_TAMNA)
        center.place(relx=0.5, rely=0.5, anchor="center")
 
        tk.Label(center, text="REZULTAT RUNDE",
                 bg=BG_TAMNA, fg=SIVA_SVIJETLA,
                 font=self.f_maly).pack(pady=(0, 10))
 
        # ── Tvoja riječ ──────────────────────────────────────────
        tvoja_frame = tk.Frame(center, bg=BG_PANEL, padx=50, pady=20)
        tvoja_frame.pack(pady=(0, 24), fill="x")
 
        tk.Label(tvoja_frame, text="Tvoja riječ:",
                 bg=BG_PANEL, fg=SIVA_SVIJETLA,
                 font=self.f_maly).pack(side="left", padx=(0, 20))
 
        boja = ZELENA if ispravna else CRVENA
        tk.Label(tvoja_frame,
                 text=unos.upper() if unos else "—",
                 bg=BG_PANEL, fg=boja,
                 font=self.f_rezultat).pack(side="left")
 
        poruka_bodovi = f"+{zaradjeno} bodova" if ispravna else "+0 bodova"
        tk.Label(tvoja_frame,
                 text=poruka_bodovi,
                 bg=BG_PANEL, fg=boja,
                 font=self.f_rezultat).pack(side="right", padx=(20, 0))
 
        # ── Ukupni bodovi ────────────────────────────────────────
        ukupno_frame = tk.Frame(center, bg=BG_KARTICA, padx=40, pady=16)
        ukupno_frame.pack(pady=(0, 30), fill="x")
 
        tk.Label(ukupno_frame, text="Ukupni bodovi:",
                 bg=BG_KARTICA, fg=SIVA_SVIJETLA,
                 font=self.f_status).pack(side="left")
        tk.Label(ukupno_frame, text=str(self.igra.bodovi),
                 bg=BG_KARTICA, fg=ZLATNA,
                 font=self.f_bodovi).pack(side="left", padx=(16, 0))
 
        if self.igra.bodovi > self._highscore:
            self._highscore = self.igra.bodovi
            Slagalica.spremi_highscore(self._putanja_highscore, self._highscore)
            self.main_screen.azuriraj_highscore(self._highscore)
            tk.Label(ukupno_frame, text="  🎉 NOVI REKORD!",
                     bg=BG_KARTICA, fg=ZLATNA,
                     font=self.f_status).pack(side="left")
 
        # Povratak na main screen nakon 5 sekundi
        self.lbl_status.config(
            text="Povratak na početni ekran za 5 sekundi...",
            fg=SIVA_SVIJETLA)
        self._vrati_id = self.root.after(5000, self._vrati_na_main)
 
    def _vrati_na_main(self):
        self._vrati_id = None
        self.igra.reset()
        self.slagalica = None
        self._reset_igra_ekran()
        self._show_main_screen()
 
    # ══════════════════════════════════════════
    #  Timer
    # ══════════════════════════════════════════
    def _pokreni_timer(self):
        self._odbrojavaj()
 
    def _odbrojavaj(self):
        self.lbl_timer.config(text=f"⏱ {self.preostalo_vrijeme}")
        self.lbl_timer.config(fg=CRVENA if self.preostalo_vrijeme <= 10 else ZLATNA)
 
        if self.preostalo_vrijeme <= 0:
            self._vrijeme_isteklo()
            return
 
        self.preostalo_vrijeme -= 1
        self._timer_id = self.root.after(1000, self._odbrojavaj)
 
    def _vrijeme_isteklo(self):
        self.lbl_timer.config(text="⏱ 0", fg=CRVENA)
        if self._unos_aktivan:
            self.lbl_status.config(
                text="⏰ Vrijeme je isteklo! Automatska provjera...",
                fg=ZLATNA)
            self.root.after(500, self._klik_potvrdi)
 
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