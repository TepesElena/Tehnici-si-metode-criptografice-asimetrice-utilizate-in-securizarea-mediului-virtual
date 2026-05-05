import tkinter as tk
from tkinter import ttk, scrolledtext
from tkinter import PhotoImage
import random

class Constante:
    BG_APP      = "#F1F5F9"
    BG_SIDE     = "#FFFFFF"
    BORDER      = "#E2E8F0"
    TEXT_PRI    = "#0F172A"
    TEXT_SEC    = "#475569"
    ACCENT      = "#2563EB"
    SUCCESS     = "#10B981"
    ERROR       = "#EF4444"
    WARNING     = "#F59E0B"
    PURPLE      = "#7C3AED"
    PURPLE_LT   = "#F5F3FF"

    F_MAIN      = "Segoe UI"
    F_CODE      = "Consolas"
    SIZE_H1     = 14
    SIZE_H2     = 10
    SIZE_BODY   = 9

def _is_prime(n, k=6):
    if n < 2: return False
    for p in [2,3,5,7,11,13,17,19,23,29,31,37]:
        if n == p: return True
        if n % p == 0: return False
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2; s += 1
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1: continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1: break
        else:
            return False
    return True

def _gen_prime(bits):
    while True:
        p = random.randrange(2**(bits-1), 2**bits)
        if _is_prime(p): return p

def rsa_keygen(bits=16):
    p = _gen_prime(bits // 2)
    q = _gen_prime(bits // 2)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    def ext_gcd(a, b):
        if a == 0: return b, 0, 1
        g, x1, y1 = ext_gcd(b % a, a)
        return g, y1 - (b // a) * x1, x1
    _, d, _ = ext_gcd(e, phi)
    return (e, n), (d % phi, n)   # (pub_key, priv_key)

def rsa_sign(message, priv_key):
    d, n = priv_key
    return pow(hash(str(message)) % n, d, n)

def rsa_verify(message, signature, pub_key):
    e, n = pub_key
    return (hash(str(message)) % n) == pow(signature, e, n)


class LogPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=Constante.BG_SIDE, bd=0)

        hdr = tk.Frame(self, bg=Constante.BG_SIDE)
        hdr.pack(fill="x", padx=10, pady=(10, 2))

        tk.Label(
            hdr,
            text="LOG",
            font=(Constante.F_MAIN, Constante.SIZE_H2, "bold"),
            fg=Constante.TEXT_PRI,
            bg=Constante.BG_SIDE
        ).pack(side="left")

        tk.Button(
            hdr,
            text="Reset",
            font=(Constante.F_MAIN, 8),
            bg=Constante.BG_APP,
            command=self.clear,
            relief="flat",
            padx=5
        ).pack(side="right")

        self.text_area = scrolledtext.ScrolledText(
            self,
            font=(Constante.F_CODE, 9),
            bg=Constante.BG_SIDE,
            fg=Constante.TEXT_PRI,
            bd=0
        )
        self.text_area.pack(fill="both", expand=True, padx=5, pady=5)
        self.text_area.config(state="disabled")

    def log(self, message, color=Constante.TEXT_PRI, bold=False):
        self.text_area.config(state="normal")
        tag = f"tag_{id(message)}_{self.text_area.index('end')}"
        font = (Constante.F_CODE, 9, "bold") if bold else (Constante.F_CODE, 9)
        self.text_area.tag_config(tag, foreground=color, font=font)
        self.text_area.insert("end", f"{message}\n", tag)
        self.text_area.see("end")
        self.text_area.config(state="disabled")

    def clear(self):
        self.text_area.config(state="normal")
        self.text_area.delete("1.0", tk.END)
        self.text_area.config(state="disabled")


class ParticipantCard(tk.LabelFrame):
    def __init__(self, parent, title, color, fields, secret_var=None, secret_label="Cheie privată:"):
        super().__init__(
            parent,
            text=f" {title} ",
            font=(Constante.F_MAIN, Constante.SIZE_H2, "bold"),
            bg="white",
            fg=color,
            padx=10,
            pady=10
        )

        self.boxes = {}

        def lighten(hex_color, factor=0.85):
            hex_color = hex_color.lstrip("#")
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            r = int(r + (255 - r) * factor)
            g = int(g + (255 - g) * factor)
            b = int(b + (255 - b) * factor)
            return f"#{r:02x}{g:02x}{g:02x}"

        bg_light = lighten(color, 0.85)

        if secret_var:
            f = tk.Frame(self, bg=bg_light, padx=8, pady=5)
            f.pack(fill="x", pady=(0, 10))
            tk.Label(f, text=secret_label, font=(Constante.F_MAIN, 8, "bold"), fg=Constante.TEXT_SEC, bg=bg_light).pack(side="left")
            tk.Entry(f, textvariable=secret_var, font=(Constante.F_CODE, 9), width=5, relief="flat", bg="white").pack(side="right")

        for name in fields:
            box = tk.Frame(self, bg=bg_light, padx=8, pady=6)
            box.pack(fill="x", pady=4)
            tk.Label(box, text=name, font=(Constante.F_MAIN, 7), fg=Constante.TEXT_SEC, bg=bg_light).pack(anchor="w")
            v = tk.StringVar(value="—")
            lbl = tk.Label(box, textvariable=v, font=(Constante.F_CODE, 11, "bold"), fg=Constante.TEXT_PRI, bg=bg_light)
            lbl.pack(anchor="w")
            self.boxes[name] = (v, lbl)

    def update_val(self, key, val, flash=False):
        if key in self.boxes:
            var, lbl = self.boxes[key]
            var.set(str(val))
            if flash:
                lbl.config(fg=Constante.ACCENT)
                self.after(500, lambda: lbl.config(fg=Constante.TEXT_PRI))

    def reset(self):
        for v, l in self.boxes.values():
            v.set("—")


class RSAInfoCard(tk.LabelFrame):
    """
    Displays RSA key details + signature + verification badge
    for one participant in scenario 3.
    """
    def __init__(self, parent, title, color):
        super().__init__(
            parent,
            text=f" {title} — Detalii RSA ",
            font=(Constante.F_MAIN, 8, "bold"),
            bg=Constante.PURPLE_LT,
            fg=Constante.PURPLE,
            padx=10,
            pady=8
        )
        self._color  = color
        self._labels = {}   # key → (StringVar, Label)

        rows = [
            ("rsa_n",    "Modul RSA  n",              Constante.PURPLE_LT, Constante.PURPLE),
            ("rsa_e",    "Exponent public  e",         Constante.PURPLE_LT, Constante.PURPLE),
            ("sig",      "Semnătură digitală  sig(A/B)", "#F0FDF4",         Constante.SUCCESS),
            ("verified", "Verificare semnătură",       "#F0FDF4",           Constante.SUCCESS),
        ]

        for key, label_text, bg, fg in rows:
            box = tk.Frame(self, bg=bg, padx=8, pady=5,
                           highlightbackground="#DDD6FE", highlightthickness=1)
            box.pack(fill="x", pady=3)
            tk.Label(box, text=label_text, font=(Constante.F_MAIN, 7),
                     fg=Constante.TEXT_SEC, bg=bg).pack(anchor="w")
            var = tk.StringVar(value="—")
            lbl = tk.Label(box, textvariable=var,
                           font=(Constante.F_CODE, 10, "bold"),
                           fg=fg, bg=bg, anchor="w", wraplength=220, justify="left")
            lbl.pack(anchor="w")
            self._labels[key] = (var, lbl)

    def set(self, key, value, flash_color=None):
        if key not in self._labels:
            return
        var, lbl = self._labels[key]
        var.set(str(value))
        if flash_color:
            orig = lbl.cget("fg")
            lbl.config(fg=flash_color)
            self.after(600, lambda: lbl.config(fg=orig))

    def mark_verified(self, ok: bool):
        var, lbl = self._labels["verified"]
        if ok:
            var.set("✓  VALIDĂ")
            lbl.config(fg=Constante.SUCCESS)
        else:
            var.set("✗  INVALIDĂ")
            lbl.config(fg=Constante.ERROR)

    def reset(self):
        for var, lbl in self._labels.values():
            var.set("—")


class DiffieHellmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Analiza protocolului Diffie-Hellman")
        self.root.geometry("1200x900")
        self.root.configure(bg=Constante.BG_APP)

        self.p_var       = tk.IntVar(value=23)
        self.g_var       = tk.IntVar(value=5)
        self.alice_priv  = tk.IntVar(value=6)
        self.bob_priv    = tk.IntVar(value=15)
        self.darth_priv  = tk.IntVar(value=13)

        self._setup_ui()

    def _create_param_box(self, parent):
        box = tk.Frame(parent, bg="#F8FAFC", padx=12, pady=10,
                       highlightthickness=1, highlightbackground=Constante.BORDER)
        tk.Label(box, text="PARAMETRI MATEMATICI (PUBLICI)",
                 font=(Constante.F_MAIN, 8, "bold"),
                 fg=Constante.ACCENT, bg="#F8FAFC").pack(anchor="w", pady=(0, 5))
        for var, label, desc in [
            (self.p_var, "p (Modul):", "Numar prim"),
            (self.g_var, "g (Baza):",  "Generator"),
        ]:
            line = tk.Frame(box, bg="#F8FAFC")
            line.pack(fill="x", pady=2)
            tk.Label(line, text=label, font=(Constante.F_MAIN, 9, "bold"),
                     bg="#F8FAFC").pack(side="left")
            tk.Entry(line, textvariable=var, font=(Constante.F_CODE, 9),
                     width=5, relief="flat",
                     highlightthickness=1, highlightbackground=Constante.BORDER
                     ).pack(side="left", padx=5)
            tk.Label(line, text=desc, font=(Constante.F_MAIN, 7),
                     fg=Constante.TEXT_SEC, bg="#F8FAFC").pack(side="left", padx=10)
        return box

    def _setup_ui(self):
        header = tk.Frame(self.root, bg="white",
                          highlightthickness=1, highlightbackground=Constante.BORDER)
        header.pack(fill="x", side="top")
        tk.Label(header,
                 text="Studiu practic asupra protocolului Diffie–Hellman și securizarea sa prin autentificare",
                 font=(Constante.F_MAIN, Constante.SIZE_H1, "bold"),
                 bg="white", padx=20, pady=15).pack(side="bottom")

        self.paned = tk.PanedWindow(self.root, orient="horizontal",
                                    bg=Constante.BORDER, sashwidth=4)
        self.paned.pack(fill="both", expand=True)

        self.left_f    = tk.Frame(self.paned, bg=Constante.BG_APP)
        self.log_panel = LogPanel(self.paned)
        self.paned.add(self.left_f,    stretch="always")
        self.paned.add(self.log_panel, width=500)

        self.nb = ttk.Notebook(self.left_f)
        self.nb.pack(fill="both", expand=True, padx=10, pady=10)

        self._tab_std()
        self._tab_mitm()
        self._tab_auth()

    def _tab_std(self):
        f = tk.Frame(self.nb, bg=Constante.BG_APP, padx=20, pady=20)
        self.nb.add(f, text=" 1. Protocolul DH - Funcționare ")

        grid = tk.Frame(f, bg=Constante.BG_APP)
        grid.pack(fill="x", pady=5)
        self.p1_a = ParticipantCard(grid, "ALICE", Constante.ACCENT,
                                    ["Cheia publică A", "Secret S"],
                                    self.alice_priv, "Cheia privată a:")
        self.p1_a.pack(side="left", fill="both", expand=True, padx=5)
        self.p1_b = ParticipantCard(grid, "BOB", Constante.WARNING,
                                    ["Cheia publică B", "Secret S"],
                                    self.bob_priv, "Cheia privată b:")
        self.p1_b.pack(side="left", fill="both", expand=True, padx=5)

        self._create_param_box(f).pack(fill="x", pady=15)
        tk.Button(f, text="Execută", bg=Constante.ACCENT, fg="white",
                  font=(Constante.F_MAIN, 9, "bold"), command=self.run_s1,
                  relief="flat", padx=25, pady=10).pack()

    def _tab_mitm(self):
        f = tk.Frame(self.nb, bg=Constante.BG_APP, padx=20, pady=20)
        self.nb.add(f, text=" 2. Protocolul DH - Vulnerabilitate MITM ")

        grid = tk.Frame(f, bg=Constante.BG_APP)
        grid.pack(fill="x", pady=5)
        self.p2_a = ParticipantCard(grid, "ALICE", Constante.ACCENT,
                                    ["Vede Pub:", "Secret S1"],
                                    self.alice_priv, "Cheia privată a:")
        self.p2_a.pack(side="left", fill="both", expand=True, padx=2)
        self.p2_d = ParticipantCard(grid, "DARTH (ATAC)", Constante.ERROR,
                                    ["S1 (Alice)", "S2 (Bob)"],
                                    self.darth_priv, "Cheia privată d:")
        self.p2_d.pack(side="left", fill="both", expand=True, padx=2)
        self.p2_b = ParticipantCard(grid, "BOB", Constante.WARNING,
                                    ["Vede Pub:", "Secret S2"],
                                    self.bob_priv, "Cheia privată b:")
        self.p2_b.pack(side="left", fill="both", expand=True, padx=2)

        self._create_param_box(f).pack(fill="x", pady=15)
        tk.Button(f, text="Execută", bg=Constante.ERROR, fg="white",
                  font=(Constante.F_MAIN, 9, "bold"), command=self.run_s2,
                  relief="flat", padx=25, pady=10).pack()

    def _tab_auth(self):
        outer = tk.Frame(self.nb, bg=Constante.BG_APP)
        self.nb.add(outer, text=" 3. Protocolul DH - Securizare prin autentificare ")

        canvas = tk.Canvas(outer, bg=Constante.BG_APP, highlightthickness=0)
        vsb = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        f = tk.Frame(canvas, bg=Constante.BG_APP, padx=20, pady=20)
        win_id = canvas.create_window((0, 0), window=f, anchor="nw")

        def _on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def _on_canvas_resize(event):
            canvas.itemconfig(win_id, width=event.width)

        f.bind("<Configure>", _on_configure)
        canvas.bind("<Configure>", _on_canvas_resize)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        grid = tk.Frame(f, bg=Constante.BG_APP)
        grid.pack(fill="x", pady=5)

        self.p3_a = ParticipantCard(
            grid, "ALICE", Constante.ACCENT,
            ["Cheia publică A", "Semnătură RSA", "Secret"],
            self.alice_priv, "Cheia privată a:")
        self.p3_a.pack(side="left", fill="both", expand=True, padx=2)

        self.p3_d = ParticipantCard(
            grid, "DARTH", Constante.ERROR,
            ["Vede A, B", "Stare Atac"], None)
        self.p3_d.pack(side="left", fill="both", expand=True, padx=2)

        self.p3_b = ParticipantCard(
            grid, "BOB", Constante.WARNING,
            ["Cheia publică B", "Semnătură RSA", "Secret"],
            self.bob_priv, "Cheia privată b:")
        self.p3_b.pack(side="left", fill="both", expand=True, padx=2)

        rsa_lbl = tk.Frame(f, bg=Constante.BG_APP)
        rsa_lbl.pack(fill="x", pady=(14, 2))
        tk.Frame(rsa_lbl, bg="#DDD6FE", height=1).pack(
            fill="x", side="left", expand=True, pady=6)
        tk.Label(rsa_lbl, text="  DETALII SEMNĂTURĂ DIGITALĂ RSA  ",
                 font=(Constante.F_MAIN, 8, "bold"),
                 fg=Constante.PURPLE, bg=Constante.BG_APP).pack(side="left")
        tk.Frame(rsa_lbl, bg="#DDD6FE", height=1).pack(
            fill="x", side="left", expand=True, pady=6)

        rsa_row = tk.Frame(f, bg=Constante.BG_APP)
        rsa_row.pack(fill="x", pady=(0, 6))

        self.rsa_alice = RSAInfoCard(rsa_row, "ALICE", Constante.ACCENT)
        self.rsa_alice.pack(side="left", fill="both", expand=True, padx=(0, 6))

        darth_rsa = tk.LabelFrame(rsa_row,
                                   text=" DARTH — Tentativă falsificare ",
                                   font=(Constante.F_MAIN, 8, "bold"),
                                   bg="#FEF2F2", fg=Constante.ERROR,
                                   padx=10, pady=8)
        darth_rsa.pack(side="left", fill="both", expand=True, padx=6)
        for line in [
            "✗  Nu are cheia privată RSA a lui Alice",
            "✗  Nu poate calcula  sig(D) valid",
            "✗  Bob detectează semnătura falsă",
            "✗  Conexiunea este refuzată automat",
        ]:
            tk.Label(darth_rsa, text=line, font=(Constante.F_MAIN, 8),
                     fg=Constante.ERROR, bg="#FEF2F2", anchor="w").pack(fill="x", pady=2)
        tk.Frame(darth_rsa, bg="#FECACA", height=1).pack(fill="x", pady=6)
        tk.Label(darth_rsa, text="ATAC BLOCAT DE AUTENTIFICARE",
                 font=(Constante.F_MAIN, 9, "bold"),
                 fg=Constante.ERROR, bg="#FEF2F2").pack()

        self.rsa_bob = RSAInfoCard(rsa_row, "BOB", Constante.WARNING)
        self.rsa_bob.pack(side="right", fill="both", expand=True, padx=(6, 0))

        self._create_param_box(f).pack(fill="x", pady=10)
        tk.Button(f, text="Execută", bg=Constante.SUCCESS, fg="white",
                  font=(Constante.F_MAIN, 9, "bold"), command=self.run_s3,
                  relief="flat", padx=25, pady=10).pack(anchor="w")

    def run_s1(self):
        p, g = self.p_var.get(), self.g_var.get()
        a, b = self.alice_priv.get(), self.bob_priv.get()
        A, B = pow(g, a, p), pow(g, b, p)
        s = pow(B, a, p)

        self.log_panel.clear()
        self.log_panel.log("Inițiere schimb DH standard", Constante.ACCENT, True)

        self.log_panel.log("Pasul 1: Alegerea cheilor private (secrete)", bold=True)
        self.log_panel.log(f"Alice alege: a = {a}")
        self.log_panel.log(f"Bob alege: b = {b}\n")

        self.log_panel.log("Pasul 2: Calculul cheilor publice", bold=True)
        self.log_panel.log(f"Alice: A = g^a mod p = {g}^{a} mod {p} = {A}")
        self.log_panel.log(f"Bob: B = g^b mod p = {g}^{b} mod {p} = {B}\n")
        self.p1_a.update_val("Cheia publică A", A, True)
        self.p1_b.update_val("Cheia publică B", B, True)

        self.log_panel.log("Pasul 3: Schimbul de chei", bold=True)
        self.log_panel.log(f"Alice -> (A={A}) -> Bob")
        self.log_panel.log(f"Bob -> (B={B}) -> Alice\n")

        self.log_panel.log("Pasul 4: Calculul secretului comun S", bold=True)
        self.log_panel.log(f"Alice calculeaza: S = B^a mod p = {B}^{a} mod {p} = {s}")
        self.log_panel.log(f"Bob calculeaza: S = A^b mod p = {A}^{b} mod {p} = {s}")
        self.p1_a.update_val("Secret S", s, True)
        self.p1_b.update_val("Secret S", s, True)
        self.log_panel.log(f"\nSecret comun stabilit S = {s}", Constante.SUCCESS, True)

    def run_s2(self):
        p, g = self.p_var.get(), self.g_var.get()
        a, b, d = self.alice_priv.get(), self.bob_priv.get(), self.darth_priv.get()
        A, B, D = pow(g, a, p), pow(g, b, p), pow(g, d, p)
        s_ad, s_bd = pow(D, a, p), pow(D, b, p)

        self.log_panel.clear()
        self.log_panel.log("Atac MITM", Constante.ERROR, True)

        self.log_panel.log("Pasul 1: Interceptare", bold=True)
        self.log_panel.log(f"Alice trimite A={A}. Darth interceptează A.")
        self.log_panel.log(f"Bob trimite B={B}. Darth interceptează B.\n")

        self.log_panel.log("Pasul 2: Substituție", bold=True)
        self.log_panel.log(f"Darth trimite D={D} către Alice (zice că e Bob)")
        self.log_panel.log(f"Darth trimite D={D} către Bob (zice că e Alice)\n")
        self.p2_a.update_val("Vede Pub:", f"D={D}", True)
        self.p2_b.update_val("Vede Pub:", f"D={D}", True)

        self.log_panel.log("Pasul 3: Compromiterea", bold=True)
        self.log_panel.log(f"Alice calculează secret S1 = D^a mod p = {s_ad}")
        self.log_panel.log(f"Bob calculează secret S2 = D^b mod p = {s_bd}")
        self.log_panel.log(f"Darth calculează S1 = A^d mod p = {s_ad}")
        self.log_panel.log(f"Darth calculează S2 = B^d mod p = {s_bd}\n")

        self.p2_a.update_val("Secret S1", s_ad)
        self.p2_b.update_val("Secret S2", s_bd)
        self.p2_d.update_val("S1 (Alice)", s_ad, True)
        self.p2_d.update_val("S2 (Bob)", s_bd, True)
        self.log_panel.log("Darth poate descifra și modifica tot traficul!", Constante.ERROR)

    def run_s3(self):
        p, g = self.p_var.get(), self.g_var.get()
        a, b = self.alice_priv.get(), self.bob_priv.get()

        self.rsa_alice.reset()
        self.rsa_bob.reset()

        self.log_panel.clear()
        self.log_panel.log("DH Autentificat cu RSA", Constante.SUCCESS, True)

        self.log_panel.log("Pasul 1: Generare perechi de chei RSA", bold=True)
        alice_pub, alice_prv = rsa_keygen(bits=16)
        bob_pub,   bob_prv   = rsa_keygen(bits=16)
        a_e, a_n = alice_pub
        b_e, b_n = bob_pub
        self.log_panel.log(f"  Alice  →  e={a_e}, n={a_n}  (publică)")
        self.log_panel.log(f"           d={alice_prv[0]}  (privată — secretă)")
        self.log_panel.log(f"  Bob    →  e={b_e}, n={b_n}  (publică)")
        self.log_panel.log(f"           d={bob_prv[0]}  (privată — secretă)\n")

        self.rsa_alice.set("rsa_n", a_n)
        self.rsa_alice.set("rsa_e", a_e)
        self.rsa_bob.set("rsa_n", b_n)
        self.rsa_bob.set("rsa_e", b_e)

        self.log_panel.log("Pasul 2: Calculul cheilor publice DH", bold=True)
        A = pow(g, a, p)
        B = pow(g, b, p)
        self.log_panel.log(f"  Alice:  A = {g}^{a} mod {p} = {A}")
        self.log_panel.log(f"  Bob:    B = {g}^{b} mod {p} = {B}\n")

        self.p3_a.update_val("Cheia publică A", A, True)
        self.p3_b.update_val("Cheia publică B", B, True)
        self.p3_d.update_val("Vede A, B", f"A={A}, B={B}")

        self.log_panel.log("Pasul 3: Semnare digitală RSA", bold=True)
        sig_a = rsa_sign(A, alice_prv)
        sig_b = rsa_sign(B, bob_prv)

        self.log_panel.log(f"  Alice semnează A={A}:")
        self.log_panel.log(f"    sig_A = H(A)^d mod n = {sig_a}")
        self.log_panel.log(f"  Bob semnează B={B}:")
        self.log_panel.log(f"    sig_B = H(B)^d mod n = {sig_b}\n")

        sig_a_disp = f"{str(sig_a)[:8]}…{str(sig_a)[-4:]}"
        sig_b_disp = f"{str(sig_b)[:8]}…{str(sig_b)[-4:]}"
        self.p3_a.update_val("Semnătură RSA", sig_a_disp, True)
        self.p3_b.update_val("Semnătură RSA", sig_b_disp, True)
        self.rsa_alice.set("sig", sig_a_disp)
        self.rsa_bob.set("sig",   sig_b_disp)

        self.log_panel.log("Pasul 4: Verificare semnături", bold=True)
        ok_a = rsa_verify(A, sig_a, alice_pub)
        ok_b = rsa_verify(B, sig_b, bob_pub)

        res_a = "✓ VALIDĂ" if ok_a else "✗ INVALIDĂ"
        res_b = "✓ VALIDĂ" if ok_b else "✗ INVALIDĂ"
        self.log_panel.log(f"  Bob verifică sig_A:    {res_a}")
        self.log_panel.log(f"  Alice verifică sig_B:  {res_b}\n")

        self.rsa_alice.mark_verified(ok_a)
        self.rsa_bob.mark_verified(ok_b)

        self.log_panel.log("Pasul 5: Analiza Darth", bold=True)
        self.log_panel.log("  Darth încearcă să modifice A în D.")
        self.log_panel.log("  DAR: Darth nu are cheia privată RSA a lui Alice!", Constante.ERROR)
        self.log_panel.log("  Orice semnătură generată de Darth va eșua verificarea.")
        self.log_panel.log("  Rezultat: Bob detectează frauda și oprește conexiunea.\n", Constante.ERROR)

        self.p3_d.update_val("Stare Atac", "EȘUAT ✗", True)

        self.log_panel.log("Pasul 6: Calcul secret comun (autentificat)", bold=True)
        s = pow(B, a, p)
        self.log_panel.log(f"  Alice:  S = B^a mod p = {B}^{a} mod {p} = {s}")
        self.log_panel.log(f"  Bob:    S = A^b mod p = {A}^{b} mod {p} = {s}\n")

        self.p3_a.update_val("Secret", s, True)
        self.p3_b.update_val("Secret", "CONEXIUNE ÎNTRERUPTĂ")

        self.log_panel.log("Autentificarea previne MITM.", Constante.SUCCESS, True)
        self.log_panel.log(f"Secret comun stabilit S = {s}", Constante.SUCCESS, True)


if __name__ == "__main__":
    root = tk.Tk()
    try:
        icon = PhotoImage(file="ico.png")
        root.iconphoto(True, icon)
    except Exception:
        pass
    app = DiffieHellmanGUI(root)
    root.mainloop()