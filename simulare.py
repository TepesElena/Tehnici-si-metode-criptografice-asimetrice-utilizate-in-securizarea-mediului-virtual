import tkinter as tk
from tkinter import ttk, scrolledtext
from tkinter import PhotoImage

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

    F_MAIN      = "Segoe UI"
    F_CODE      = "Consolas"
    SIZE_H1     = 14
    SIZE_H2     = 10
    SIZE_BODY   = 9

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
        tag = "bold" if bold else "normal"
        self.text_area.insert("end", f"{message}\n", tag)
        self.text_area.tag_config("bold", font=(Constante.F_CODE, 9, "bold"), foreground=color)
        self.text_area.tag_config("normal", foreground=color)
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
            return f"#{r:02x}{g:02x}{b:02x}"

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

class DiffieHellmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Analiza protocolului Diffie-Hellman")
        self.root.geometry("1200x900")
        self.root.configure(bg=Constante.BG_APP)

        self.p_var = tk.IntVar(value=23)
        self.g_var = tk.IntVar(value=5)
        self.alice_priv = tk.IntVar(value=6)
        self.bob_priv = tk.IntVar(value=15)
        self.darth_priv = tk.IntVar(value=13)

        self._setup_ui()

    def _create_param_box(self, parent):
        box = tk.Frame(parent, bg="#F8FAFC", padx=12, pady=10, highlightthickness=1, highlightbackground=Constante.BORDER)
        
        tk.Label(box, text="PARAMETRI MATEMATICI (PUBLICI)", font=(Constante.F_MAIN, 8, "bold"), 
                 fg=Constante.ACCENT, bg="#F8FAFC").pack(anchor="w", pady=(0, 5))

        for var, label, desc in [(self.p_var, "p (Modul):", "Numar prim"), (self.g_var, "g (Baza):", "Generator")]:
            line = tk.Frame(box, bg="#F8FAFC")
            line.pack(fill="x", pady=2)
            tk.Label(line, text=label, font=(Constante.F_MAIN, 9, "bold"), bg="#F8FAFC").pack(side="left")
            tk.Entry(line, textvariable=var, font=(Constante.F_CODE, 9), width=5, relief="flat", 
                     highlightthickness=1, highlightbackground=Constante.BORDER).pack(side="left", padx=5)
            tk.Label(line, text=desc, font=(Constante.F_MAIN, 7), fg=Constante.TEXT_SEC, bg="#F8FAFC").pack(side="left", padx=10)
        return box

    def _setup_ui(self):
        header = tk.Frame(self.root, bg="white", highlightthickness=1, highlightbackground=Constante.BORDER)
        header.pack(fill="x", side="top")
        tk.Label(header, text="Studiu practic asupra protocolului Diffie–Hellman și securizarea sa prin autentificare", 
                 font=(Constante.F_MAIN, Constante.SIZE_H1, "bold"), 
                 bg="white", padx=20, pady=15).pack(side="bottom")

        self.paned = tk.PanedWindow(self.root, orient="horizontal", bg=Constante.BORDER, sashwidth=4)
        self.paned.pack(fill="both", expand=True)

        self.left_f = tk.Frame(self.paned, bg=Constante.BG_APP)
        self.log_panel = LogPanel(self.paned)

        self.paned.add(self.left_f, stretch="always")
        self.paned.add(self.log_panel, width=500)

        self.nb = ttk.Notebook(self.left_f)
        self.nb.pack(fill="both", expand=True, padx=10, pady=10)

        self._tab_std()
        self._tab_mitm()
        self._tab_auth()

    def _tab_std(self):
        f = tk.Frame(self.nb, bg=Constante.BG_APP, padx=20, pady=20)
        self.nb.add(f, text=" 1. Protocolul DH - Funcționare ")
        
        # 1. Participanți
        grid = tk.Frame(f, bg=Constante.BG_APP)
        grid.pack(fill="x", pady=5)
        self.p1_a = ParticipantCard(grid, "ALICE", Constante.ACCENT, ["Cheia publică A", "Secret S"], self.alice_priv, "Cheia privată a:")
        self.p1_a.pack(side="left", fill="both", expand=True, padx=5)
        self.p1_b = ParticipantCard(grid, "BOB", Constante.WARNING, ["Cheia publică B", "Secret S"], self.bob_priv, "Cheia privată b:")
        self.p1_b.pack(side="left", fill="both", expand=True, padx=5)
        
        # 2. Parametri (Înainte de buton)
        self._create_param_box(f).pack(fill="x", pady=15)
        
        # 3. Buton
        tk.Button(f, text="Execută", bg=Constante.ACCENT, fg="white", 
                  font=(Constante.F_MAIN, 9, "bold"), command=self.run_s1, relief="flat", padx=25, pady=10).pack()

    def _tab_mitm(self):
        f = tk.Frame(self.nb, bg=Constante.BG_APP, padx=20, pady=20)
        self.nb.add(f, text=" 2. Protocolul DH - Vulnerabilitate MITM ")
        
        # 1. Participanți
        grid = tk.Frame(f, bg=Constante.BG_APP)
        grid.pack(fill="x", pady=5)
        self.p2_a = ParticipantCard(grid, "ALICE", Constante.ACCENT, ["Vede Pub:", "Secret S1"], self.alice_priv, "Cheia privată a:")
        self.p2_a.pack(side="left", fill="both", expand=True, padx=2)
        self.p2_d = ParticipantCard(grid, "DARTH (ATAC)", Constante.ERROR, ["S1 (Alice)", "S2 (Bob)"], self.darth_priv, "Cheia privată d:")
        self.p2_d.pack(side="left", fill="both", expand=True, padx=2)
        self.p2_b = ParticipantCard(grid, "BOB", Constante.WARNING, ["Vede Pub:", "Secret S2"], self.bob_priv, "Cheia privată b:")
        self.p2_b.pack(side="left", fill="both", expand=True, padx=2)
        
        # 2. Parametri
        self._create_param_box(f).pack(fill="x", pady=15)
        
        # 3. Buton
        tk.Button(f, text="Execută", bg=Constante.ERROR, fg="white", 
                  font=(Constante.F_MAIN, 9, "bold"), command=self.run_s2, relief="flat", padx=25, pady=10).pack()

    def _tab_auth(self):
        f = tk.Frame(self.nb, bg=Constante.BG_APP, padx=20, pady=20)
        self.nb.add(f, text=" 3. Protocolul DH - Securizare prin autentificare ")
        
        # 1. Participanți
        grid = tk.Frame(f, bg=Constante.BG_APP)
        grid.pack(fill="x", pady=5)
        self.p3_a = ParticipantCard(grid, "ALICE", Constante.ACCENT, ["Cheia publică A", "Semnătura", "Secret"], self.alice_priv, "Cheia privată a:")
        self.p3_a.pack(side="left", fill="both", expand=True, padx=2)
        self.p3_d = ParticipantCard(grid, "DARTH", Constante.ERROR, ["Vede A, B", "Stare Atac"], None)
        self.p3_d.pack(side="left", fill="both", expand=True, padx=2)
        self.p3_b = ParticipantCard(grid, "BOB", Constante.WARNING, ["Cheia publică B", "Semnătura", "Secret"], self.bob_priv, "Cheia privată b:")
        self.p3_b.pack(side="left", fill="both", expand=True, padx=2)
        
        # 2. Parametri
        self._create_param_box(f).pack(fill="x", pady=15)
        
        # 3. Buton
        tk.Button(f, text="Execută", bg=Constante.SUCCESS, fg="white", 
                  font=(Constante.F_MAIN, 9, "bold"), command=self.run_s3, relief="flat", padx=25, pady=10).pack()

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
        A, B = pow(g, a, p), pow(g, b, p)
        s = pow(B, a, p)

        self.log_panel.clear()
        self.log_panel.log("DH Autentificat", Constante.SUCCESS, True)
        
        self.log_panel.log("Pasul 1: Semnare Digitala", bold=True)
        self.log_panel.log("Alice: semnează cheia A cu cheia ei privată RSA.")
        self.log_panel.log("Bob: semnează cheia B cu cheia lui privată RSA.\n")

        self.log_panel.log("Pasul 2: Schimb și Verificare", bold=True)
        self.log_panel.log(f"Alice trimite A={A} + Semnătură.")
        self.log_panel.log(f"Bob trimite B={B} + Semnătură.")
        self.log_panel.log("Darth interceptează traficul.\n", Constante.WARNING)
        
        self.p3_a.update_val("Cheia publică A", A)
        self.p3_b.update_val("Cheia publică B", B)
        self.p3_d.update_val("Vede A, B", f"A={A}, B={B}")

        self.log_panel.log("Pasul 3: Analiza Darth", bold=True)
        self.log_panel.log("Darth încearcă să modifice A in D.")
        self.log_panel.log("DAR: Darth nu are cheia RSA a lui Alice pentru a semna D!")
        self.log_panel.log("Rezultat: Bob va detecta semnatura falsă și va opri conexiunea.\n", Constante.ERROR)
        
        self.p3_d.update_val("Stare Atac", "EȘUAT", True)
        self.p3_a.update_val("Semnătura", "VALIDĂ", True)
        self.p3_b.update_val("Semnătura", "FALSĂ / MODIFICATĂ", True)
        self.p3_b.update_val("Secret", "CONEXIUNE ÎNTRERUPTĂ")
        self.p3_a.update_val("Secret", s)
        
        self.log_panel.log("Autentificarea previne MITM.", Constante.SUCCESS, True)

if __name__ == "__main__":
    root = tk.Tk()
    icon = PhotoImage(file="ico.png") 
    root.iconphoto(True, icon)
    app = DiffieHellmanGUI(root)
    root.mainloop()