import tkinter as tk
from tkinter import ttk
import math
from datetime import datetime, date


BG           = "#0d0d0d"
DISPLAY_BG   = "#141414"
CARD_BG      = "#161618"
BTN_NUM      = "#1c1c1e"
BTN_OP       = "#2c2c2e"
BTN_SCI      = "#1a1f2e"
BTN_ACCENT   = "#0a84ff"
BTN_CLEAR    = "#3a1515"
BTN_MEM      = "#1a2a1a"
BTN_NAV      = "#111113"

TEXT_MAIN    = "#ffffff"
TEXT_SUB     = "#8e8e93"
TEXT_ACCENT  = "#0a84ff"
TEXT_SCI     = "#64d2ff"
TEXT_MEM     = "#30d158"
TEXT_ORANGE  = "#ff9f0a"

HOVER_NUM    = "#2c2c2e"
HOVER_OP     = "#3a3a3c"
HOVER_SCI    = "#253050"
HOVER_ACCENT = "#0066cc"
HOVER_MEM    = "#1e3d22"
HOVER_NAV    = "#1a1a1c"

FONT_EXPR    = ("Courier New", 12)
FONT_DISPLAY = ("Courier New", 32, "bold")
FONT_BTN     = ("Courier New", 11, "bold")
FONT_BTN_SM  = ("Courier New", 9,  "bold")
FONT_TITLE   = ("Courier New", 12, "bold")
FONT_LABEL   = ("Courier New", 10)
FONT_RESULT  = ("Courier New", 16, "bold")
FONT_CARD    = ("Courier New", 10, "bold")


class HBtn(tk.Button):
    def __init__(self, master, bg_n, bg_h, **kw):
        super().__init__(master, bg=bg_n, activebackground=bg_h,
                         activeforeground=kw.get("fg", TEXT_MAIN),
                         relief="flat", bd=0, cursor="hand2", **kw)
        self._n, self._h = bg_n, bg_h
        self.bind("<Enter>", lambda e: self.config(bg=bg_h))
        self.bind("<Leave>", lambda e: self.config(bg=bg_n))

    def set_active(self, active):
        col = BTN_ACCENT if active else self._n
        self.config(bg=col)


# ════════════════════════════════════════════════════════════════════════════
#  MAIN APP SHELL
# ════════════════════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Calculator")
        self.geometry("400x600")
        self.resizable(False, False)
        self.configure(bg=BG)

        self._build_nav()

        
        self.container = tk.Frame(self, bg=BG)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        
        self.pages = {}
        for P in (ScientificPage, HomePage,
                  BMIPage, AgePage, DiscountPage, TemperaturePage,
                  SpeedPage, LengthPage, MassPage, AreaPage,
                  VolumePage, DataPage, TimePage, DatePage, NumeralPage):
            p = P(self.container, self)
            self.pages[P] = p
            p.grid(row=0, column=0, sticky="nsew")

        self.show(ScientificPage)

   
    def _build_nav(self):
        nav = tk.Frame(self, bg="#0a0a0a", height=52)
        nav.pack(side="bottom", fill="x")
        nav.pack_propagate(False)

        self._nav_btns = {}
        items = [
            ("⊞", "Converters", HomePage),
            ("∫", "Scientific",  ScientificPage),
        ]
        for icon, label, page in items:
            col = tk.Frame(nav, bg="#0a0a0a")
            col.pack(side="left", expand=True, fill="both")
            b = HBtn(col, "#0a0a0a", "#151517",
                     text=f"{icon}\n{label}", fg=TEXT_SUB,
                     font=("Courier New", 8, "bold"),
                     command=lambda p=page: self.show(p),
                     pady=4)
            b.pack(fill="both", expand=True)
            self._nav_btns[page] = b

        
        tk.Frame(self, bg="#222224", height=1).pack(side="bottom", fill="x")

    def show(self, page_cls):
        self.pages[page_cls].tkraise()
        
        for p, btn in self._nav_btns.items():
            is_active = (p == page_cls or
                         (page_cls not in self._nav_btns and p == HomePage))
            btn.config(fg=TEXT_ACCENT if is_active else TEXT_SUB)


#Converter grid
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller

        self.MODES = [
            ("🎂", "Age", AgePage),
            ("📐", "Area", AreaPage),
            ("⚖", "BMI", BMIPage),
            ("📅", "Date", DatePage),
            ("🏷", "Discount", DiscountPage),
            ("📏", "Length", LengthPage),
            ("🏋", "Mass", MassPage),
            ("🔢", "Numeral", NumeralPage),
            ("🚀", "Speed", SpeedPage),
            ("🌡", "Temperature", TemperaturePage),
            ("⏱", "Time", TimePage),
            ("🧪", "Volume", VolumePage),
        ]

        
        hdr = tk.Frame(self, bg="#0a0a0a", height=50)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        tk.Label(hdr, text="CONVERTERS", bg="#0a0a0a",
                 fg=TEXT_ACCENT, font=FONT_TITLE).pack(side="left", padx=16, pady=14)

        
        canvas = tk.Canvas(self, bg=BG, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        
        outer = tk.Frame(canvas, bg=BG)
        canvas.create_window((0, 0), window=outer, anchor="n")

        
        grid = tk.Frame(outer, bg=BG)
        grid.pack(pady=20)

        cols = 3

        
        for i, (icon, label, cls) in enumerate(self.MODES):
            r = i // cols
            c = i % cols

            card = tk.Frame(grid, bg=CARD_BG, width=110, height=100)
            card.grid(row=r, column=c, padx=10, pady=10)
            card.pack_propagate(False)

            tk.Label(card, text=icon, bg=CARD_BG,
                     fg=TEXT_ORANGE, font=("Courier New", 20)).pack(pady=(10, 0))

            tk.Label(card, text=label, bg=CARD_BG,
                     fg=TEXT_MAIN, font=FONT_CARD).pack(pady=(5, 10))

            
            for w in [card] + card.winfo_children():
                w.bind("<Button-1>", lambda e, cl=cls: controller.show(cl))
                w.bind("<Enter>", lambda e, fr=card: fr.config(bg="#202022"))
                w.bind("<Leave>", lambda e, fr=card: fr.config(bg=CARD_BG))

        
        for c in range(cols):
            grid.columnconfigure(c, weight=1)

       
        grid.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)




#Scientific calculator
class ScientificPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller

        self.expr        = ""
        self.display_str = ""
        self.memory      = 0.0
        self.last_result = None
        self.angle_mode  = "DEG"
        self.inv_mode    = False

        self._build()
        self._bind_keys()

    def _build(self):
        
        hdr = tk.Frame(self, bg="#0a0a0a", height=50)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="SCIENTIFIC", bg="#0a0a0a",
                 fg=TEXT_ACCENT, font=FONT_TITLE).pack(side="left", padx=14, pady=14)

        self.angle_btn = HBtn(hdr, BTN_SCI, HOVER_SCI, text="DEG",
                              fg=TEXT_SCI, font=FONT_BTN_SM,
                              command=self._toggle_angle, padx=8, pady=4)
        self.angle_btn.pack(side="right", padx=6, pady=12)

        self.inv_btn = HBtn(hdr, BTN_SCI, HOVER_SCI, text="2nd",
                            fg=TEXT_SCI, font=FONT_BTN_SM,
                            command=self._toggle_inv, padx=8, pady=4)
        self.inv_btn.pack(side="right", padx=2, pady=12)

    
        disp = tk.Frame(self, bg=DISPLAY_BG, height=95)
        disp.pack(fill="x", padx=10, pady=(6, 2))
        disp.pack_propagate(False)

        self.expr_var   = tk.StringVar(value="")
        self.result_var = tk.StringVar(value="0")
        self.mem_var    = tk.StringVar(value="")

        top_row = tk.Frame(disp, bg=DISPLAY_BG)
        top_row.pack(fill="x", padx=10, pady=(8, 0))
        tk.Label(top_row, textvariable=self.mem_var,
                 bg=DISPLAY_BG, fg=TEXT_MEM, font=FONT_BTN_SM, anchor="w").pack(side="left")
        tk.Label(top_row, textvariable=self.expr_var,
                 bg=DISPLAY_BG, fg=TEXT_SUB, font=FONT_EXPR, anchor="e").pack(side="right")

        tk.Label(disp, textvariable=self.result_var,
                 bg=DISPLAY_BG, fg=TEXT_MAIN, font=FONT_DISPLAY,
                 anchor="e").pack(fill="x", padx=10, pady=(2, 8))

        
        bf = tk.Frame(self, bg=BG)
        bf.pack(fill="both", expand=True, padx=8, pady=4)

        N, O, S, A, M, C = BTN_NUM, BTN_OP, BTN_SCI, BTN_ACCENT, BTN_MEM, BTN_CLEAR
        HN, HO, HS, HA, HM = HOVER_NUM, HOVER_OP, HOVER_SCI, HOVER_ACCENT, HOVER_MEM

        self.sci_btns = {}

        rows = [
            [("MC",M,HM,TEXT_MEM),("MR",M,HM,TEXT_MEM),("M+",M,HM,TEXT_MEM),
             ("M−",M,HM,TEXT_MEM),("MS",M,HM,TEXT_MEM)],
            [("sin",S,HS,TEXT_SCI),("cos",S,HS,TEXT_SCI),("tan",S,HS,TEXT_SCI),
             ("x!",S,HS,TEXT_SCI),("π",S,HS,TEXT_SCI)],
            [("log",S,HS,TEXT_SCI),("ln",S,HS,TEXT_SCI),("√",S,HS,TEXT_SCI),
             ("x²",S,HS,TEXT_SCI),("e",S,HS,TEXT_SCI)],
            [("xʸ",S,HS,TEXT_SCI),("1/x",S,HS,TEXT_SCI),("∛",S,HS,TEXT_SCI),
             ("EXP",S,HS,TEXT_SCI),("Ans",S,HS,TEXT_SCI)],
            [("C",C,HO,"#ff453a"),("±",O,HO,TEXT_MAIN),("%",O,HO,TEXT_MAIN),
             ("÷",A,HA,TEXT_MAIN),("⌫",O,HO,TEXT_MAIN)],
            [("7",N,HN,TEXT_MAIN),("8",N,HN,TEXT_MAIN),("9",N,HN,TEXT_MAIN),
             ("×",A,HA,TEXT_MAIN),("(",O,HO,TEXT_MAIN)],
            [("4",N,HN,TEXT_MAIN),("5",N,HN,TEXT_MAIN),("6",N,HN,TEXT_MAIN),
             ("−",A,HA,TEXT_MAIN),(")",O,HO,TEXT_MAIN)],
            [("1",N,HN,TEXT_MAIN),("2",N,HN,TEXT_MAIN),("3",N,HN,TEXT_MAIN),
             ("+",A,HA,TEXT_MAIN),(".",O,HO,TEXT_MAIN)],
        ]

        for r, row in enumerate(rows):
            for c, (lbl, bg, hov, fg) in enumerate(row):
                b = HBtn(bf, bg, hov, text=lbl, fg=fg,
                         font=FONT_BTN if len(lbl) <= 3 else FONT_BTN_SM,
                         command=lambda l=lbl: self._press(l))
                b.grid(row=r, column=c, padx=3, pady=2, sticky="nsew")
                if bg == S:
                    self.sci_btns[lbl] = b

        
        HBtn(bf, N, HN, text="0", fg=TEXT_MAIN, font=FONT_BTN,
             command=lambda: self._press("0")).grid(
            row=8, column=0, columnspan=2, padx=3, pady=2, sticky="nsew")
        HBtn(bf, N, HN, text="00", fg=TEXT_MAIN, font=FONT_BTN,
             command=lambda: self._press("00")).grid(
            row=8, column=2, padx=3, pady=2, sticky="nsew")
        HBtn(bf, A, HA, text="=", fg=TEXT_MAIN, font=FONT_BTN,
             command=lambda: self._press("=")).grid(
            row=8, column=3, columnspan=2, padx=3, pady=2, sticky="nsew")

        for c in range(5):
            bf.columnconfigure(c, weight=1)
        for r in range(9):
            bf.rowconfigure(r, weight=1)

    def _bind_keys(self):
        for k in "0123456789.+-*/()":
            self.bind(f"<Key-{k}>", lambda e, ch=k: self._press(ch))
        self.bind("<Return>",    lambda e: self._press("="))
        self.bind("<BackSpace>", lambda e: self._press("⌫"))
        self.bind("<Escape>",    lambda e: self._press("C"))

    def _toggle_angle(self):
        modes = ["DEG", "RAD", "GRAD"]
        self.angle_mode = modes[(modes.index(self.angle_mode) + 1) % 3]
        self.angle_btn.config(text=self.angle_mode)

    def _toggle_inv(self):
        self.inv_mode = not self.inv_mode
        self.inv_btn.config(bg=BTN_ACCENT if self.inv_mode else BTN_SCI,
                            fg=TEXT_MAIN  if self.inv_mode else TEXT_SCI)
        inv_map = {"sin":"sin⁻¹","cos":"cos⁻¹","tan":"tan⁻¹",
                   "log":"10ˣ","ln":"eˣ","√":"x²","x²":"√","∛":"x³","xʸ":"ʸ√x"}
        fwd = inv_map if self.inv_mode else {v: k for k, v in inv_map.items()}
        for old, btn in list(self.sci_btns.items()):
            if old in fwd:
                new = fwd[old]
                btn.config(text=new, command=lambda l=new: self._press(l))
                self.sci_btns[new] = btn
                del self.sci_btns[old]

    def _to_rad(self, x):
        if self.angle_mode == "DEG":  return math.radians(x)
        if self.angle_mode == "GRAD": return x * math.pi / 200
        return x

    def _from_rad(self, x):
        if self.angle_mode == "DEG":  return math.degrees(x)
        if self.angle_mode == "GRAD": return x * 200 / math.pi
        return x

    def _press(self, key):
        try:
            self._handle(key)
        except Exception as ex:
            self._show_error(str(ex))

    def _handle(self, key):
        
        if key == "MC":
            self.memory = 0.0; self.mem_var.set(""); return
        if key == "MR":
            self._append(str(self.memory)); return
        if key in ("M+","M−","MS"):
            val = self._eval_safe()
            if val is None: return
            if   key == "MS": self.memory = val
            elif key == "M+": self.memory += val
            else:             self.memory -= val
            self.mem_var.set(f"M={self._fmt(self.memory)}"); return

        
        if key == "C":
            self.expr = ""; self.display_str = ""
            self.expr_var.set(""); self.result_var.set("0"); return
        if key == "⌫":
            self.expr = self.expr[:-1]
            self.display_str = self.display_str[:-1]
            self.expr_var.set(self.display_str)
            self._live_eval(); return

        
        if key == "=":
            val = self._eval_safe()
            if val is not None:
                self.expr_var.set("")
                self.result_var.set(self._fmt(val))
                self.last_result = val
                self.expr = self._fmt(val)
                self.display_str = self._fmt(val)
            return

        
        if key == "π":  self._append(str(math.pi), "π"); return
        if key == "e":  self._append(str(math.e),  "e"); return
        if key == "Ans":
            if self.last_result is not None:
                self._append(str(self.last_result), "Ans")
            return

        
        unary = {
            "sin":   lambda x: math.sin(self._to_rad(x)),
            "cos":   lambda x: math.cos(self._to_rad(x)),
            "tan":   lambda x: math.tan(self._to_rad(x)),
            "sin⁻¹": lambda x: self._from_rad(math.asin(x)),
            "cos⁻¹": lambda x: self._from_rad(math.acos(x)),
            "tan⁻¹": lambda x: self._from_rad(math.atan(x)),
            "log":   math.log10,   "10ˣ": lambda x: 10**x,
            "ln":    math.log,     "eˣ":  math.exp,
            "√":     math.sqrt,    "x²":  lambda x: x**2,
            "∛":     lambda x: x**(1/3), "x³": lambda x: x**3,
            "1/x":   lambda x: 1/x,
            "x!":    lambda x: float(math.factorial(int(x))),
        }
        if key in unary:
            val = self._eval_safe()
            if val is None: return
            result = unary[key](val)
            self.expr_var.set(f"{key}({self._fmt(val)})")
            self.result_var.set(self._fmt(result))
            self.last_result = result
            self.expr = self._fmt(result)
            self.display_str = self._fmt(result)
            return

        if key == "xʸ":  self._append("**", "^");     return
        if key == "ʸ√x": self._append("**(1/", "^(1/"); return
        if key == "EXP":  self._append("*10**", "E");  return

        if key == "±":
            val = self._eval_safe()
            if val is not None:
                neg = -val
                self.expr = self._fmt(neg); self.display_str = self._fmt(neg)
                self.expr_var.set(self.display_str); self.result_var.set(self._fmt(neg))
            return

        if key == "%":
            val = self._eval_safe()
            if val is not None:
                pct = val / 100
                self.expr = self._fmt(pct); self.display_str = self._fmt(pct)
                self.expr_var.set(self.display_str); self.result_var.set(self._fmt(pct))
            return

        
        op_map = {"×": "*", "÷": "/", "−": "-"}
        raw = op_map.get(key, key)
        DISP_OPS = {"+", "−", "×", "÷", "^"}
        RAW_OPS  = {"+", "-", "*", "/"}
        if (key in DISP_OPS or raw in RAW_OPS) and self.expr:
            for op in ("**", "*", "/", "+", "-"):
                if self.expr.endswith(op):
                    self.expr = self.expr[:-len(op)]; break
            for op in ("^(1/", "^", "×", "÷", "−", "+", "-", "*", "/"):
                if self.display_str.endswith(op):
                    self.display_str = self.display_str[:-len(op)]; break

        self._append(raw, key)

    def _append(self, raw, display=None):
        if display is None: display = raw
        self.expr += raw
        self.display_str += display
        self.expr_var.set(self.display_str)
        self._live_eval()

    def _live_eval(self):
        val = self._eval_safe(silent=True)
        if val is not None:
            self.result_var.set(self._fmt(val))

    def _eval_safe(self, silent=False):
        try:
            if not self.expr.strip(): return None
            result = eval(self.expr, {"__builtins__": {}},
                          {"math": math, "pi": math.pi, "e": math.e})
            return float(result)
        except:
            if not silent: self._show_error("Syntax Error")
            return None

    def _show_error(self, msg):
        self.result_var.set("Error")
        self.expr_var.set(msg)
        self.expr = ""; self.display_str = ""

    @staticmethod
    def _fmt(val):
        if val == int(val) and abs(val) < 1e15:
            return str(int(val))
        return f"{val:.10g}"



class BasePage(tk.Frame):
    def __init__(self, parent, controller, title, icon=""):
        super().__init__(parent, bg=BG)
        self.controller = controller

        # Header
        hdr = tk.Frame(self, bg="#0a0a0a", height=50)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        HBtn(hdr, "#0a0a0a", "#151517", text="← Back",
             fg=TEXT_ACCENT, font=FONT_BTN_SM,
             command=lambda: controller.show(HomePage),
             padx=10).pack(side="left", padx=6, pady=12)
        tk.Label(hdr, text=f"{icon}  {title}", bg="#0a0a0a",
                 fg=TEXT_MAIN, font=FONT_TITLE).pack(side="left", pady=14)

        self.body = tk.Frame(self, bg=BG)
        self.body.pack(fill="both", expand=True, padx=18, pady=14)
        self.body.columnconfigure(1, weight=1)

    def _entry(self, label, row):
        tk.Label(self.body, text=label, bg=BG, fg=TEXT_SUB,
                 font=FONT_LABEL).grid(row=row, column=0, sticky="w", pady=8)
        e = tk.Entry(self.body, bg=DISPLAY_BG, fg=TEXT_MAIN,
                     font=("Courier New", 13), insertbackground=TEXT_MAIN,
                     relief="flat", highlightthickness=1,
                     highlightcolor=BTN_ACCENT, highlightbackground="#2a2a2a")
        e.grid(row=row, column=1, sticky="ew", pady=8, ipady=7, padx=(10, 0))
        return e

    def _dropdown(self, label, options, row):
        tk.Label(self.body, text=label, bg=BG, fg=TEXT_SUB,
                 font=FONT_LABEL).grid(row=row, column=0, sticky="w", pady=8)
        var = tk.StringVar(value=options[0])
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Dark.TCombobox",
                        fieldbackground=DISPLAY_BG, background=DISPLAY_BG,
                        foreground=TEXT_MAIN, arrowcolor=TEXT_ACCENT,
                        selectbackground=DISPLAY_BG, selectforeground=TEXT_MAIN)
        cb = ttk.Combobox(self.body, textvariable=var, values=options,
                          state="readonly", font=("Courier New", 11),
                          style="Dark.TCombobox")
        cb.grid(row=row, column=1, sticky="ew", pady=8, padx=(10, 0))
        return var

    def _calc_btn(self, label, cmd, row):
        HBtn(self.body, BTN_ACCENT, HOVER_ACCENT, text=label,
             fg=TEXT_MAIN, font=FONT_BTN, command=cmd, pady=10).grid(
            row=row, column=0, columnspan=2, sticky="ew", pady=12)

    def _result_lbl(self, row):
        lbl = tk.Label(self.body, text="", bg=DISPLAY_BG, fg=TEXT_ACCENT,
                       font=FONT_RESULT, wraplength=320, padx=12, pady=12,
                       relief="flat", anchor="center")
        lbl.grid(row=row, column=0, columnspan=2, sticky="ew", pady=4)
        return lbl


# Converter Page

class BMIPage(BasePage):
    def __init__(self, p, c):
        super().__init__(p, c, "BMI Calculator", "⚖")
        self.weight = self._entry("Weight (kg)", 0)
        self.height = self._entry("Height (cm)", 1)
        self._calc_btn("Calculate BMI", self._calc, 2)
        self.res = self._result_lbl(3)

    def _calc(self):
        try:
            w = float(self.weight.get()); h = float(self.height.get()) / 100
            bmi = round(w / h**2, 2)
            cat = ("Underweight" if bmi < 18.5 else "Normal weight" if bmi < 25
                   else "Overweight" if bmi < 30 else "Obese")
            self.res.config(text=f"BMI  {bmi}\n{cat}")
        except: self.res.config(text="Invalid input")


class AgePage(BasePage):
    def __init__(self, p, c):
        super().__init__(p, c, "Age Calculator", "🎂")
        self.dob = self._entry("Date of Birth  (YYYY-MM-DD)", 0)
        self._calc_btn("Calculate Age", self._calc, 1)
        self.res = self._result_lbl(2)

    def _calc(self):
        try:
            dob   = datetime.strptime(self.dob.get(), "%Y-%m-%d").date()
            today = date.today()
            yrs   = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            mos   = (today.month - dob.month) % 12
            days  = abs((today - dob.replace(year=today.year)).days) % 30
            self.res.config(text=f"{yrs} yrs  {mos} mos  {days} days")
        except: self.res.config(text="Use format  YYYY-MM-DD")


class DiscountPage(BasePage):
    def __init__(self, p, c):
        super().__init__(p, c, "Discount", "🏷")
        self.price    = self._entry("Original Price", 0)
        self.discount = self._entry("Discount  (%)", 1)
        self._calc_btn("Calculate", self._calc, 2)
        self.res = self._result_lbl(3)

    def _calc(self):
        try:
            p = float(self.price.get()); d = float(self.discount.get())
            saved = round(p * d / 100, 2); final = round(p - saved, 2)
            self.res.config(text=f"Save  {saved}\nFinal  {final}")
        except: self.res.config(text="Invalid input")


class _UnitPage(BasePage):
    UNITS = {}
    def __init__(self, p, c, title, icon, base_unit):
        super().__init__(p, c, title, icon)
        self.base_unit = base_unit
        self.val  = self._entry("Value", 0)
        opts = list(self.UNITS.keys())
        self.frm  = self._dropdown("From", opts, 1)
        self.to_  = self._dropdown("To",   opts, 2)
        self._calc_btn("Convert", self._calc, 3)
        self.res  = self._result_lbl(4)

    def _to_base(self, v, unit):  return v / self.UNITS[unit]
    def _from_base(self, v, unit): return v * self.UNITS[unit]

    def _calc(self):
        try:
            v   = float(self.val.get())
            base = self._to_base(v, self.frm.get())
            result = self._from_base(base, self.to_.get())
            self.res.config(text=f"{round(result, 8)}  {self.to_.get()}")
        except: self.res.config(text="Invalid input")


class TemperaturePage(BasePage):
    def __init__(self, p, c):
        super().__init__(p, c, "Temperature", "🌡")
        self.val  = self._entry("Value", 0)
        opts = ["Celsius", "Fahrenheit", "Kelvin"]
        self.frm  = self._dropdown("From", opts, 1)
        self.to_  = self._dropdown("To",   opts, 2)
        self._calc_btn("Convert", self._calc, 3)
        self.res  = self._result_lbl(4)

    def _calc(self):
        try:
            v  = float(self.val.get()); fr = self.frm.get(); to = self.to_.get()
            c  = (v if fr=="Celsius" else (v-32)*5/9 if fr=="Fahrenheit" else v-273.15)
            r  = (c if to=="Celsius" else c*9/5+32 if to=="Fahrenheit" else c+273.15)
            self.res.config(text=f"{round(r,4)}  {to}")
        except: self.res.config(text="Invalid input")


class SpeedPage(_UnitPage):
    UNITS = {"m/s":1,"km/h":3.6,"mph":2.23694,"knots":1.94384,"ft/s":3.28084}
    def __init__(self, p, c): super().__init__(p, c, "Speed", "🚀", "m/s")
    def _to_base(self, v, u): return v / self.UNITS[u]
    def _from_base(self, v, u): return v * self.UNITS[u]


class LengthPage(_UnitPage):
    UNITS = {"m":1,"km":0.001,"cm":100,"mm":1000,"mile":0.000621371,
             "yard":1.09361,"foot":3.28084,"inch":39.3701,"nm":0.000539957}
    def __init__(self, p, c): super().__init__(p, c, "Length", "📏", "m")
    def _to_base(self, v, u): return v / self.UNITS[u]
    def _from_base(self, v, u): return v * self.UNITS[u]


class MassPage(_UnitPage):
    UNITS = {"kg":1,"g":1000,"mg":1e6,"lb":2.20462,"oz":35.274,
             "ton":0.001,"stone":0.157473}
    def __init__(self, p, c): super().__init__(p, c, "Mass", "🏋", "kg")
    def _to_base(self, v, u): return v / self.UNITS[u]
    def _from_base(self, v, u): return v * self.UNITS[u]


class AreaPage(_UnitPage):
    UNITS = {"m²":1,"km²":1e-6,"cm²":1e4,"mm²":1e6,"hectare":1e-4,
             "acre":0.000247105,"ft²":10.7639,"in²":1550,"yd²":1.19599}
    def __init__(self, p, c): super().__init__(p, c, "Area", "📐", "m²")
    def _to_base(self, v, u): return v / self.UNITS[u]
    def _from_base(self, v, u): return v * self.UNITS[u]


class VolumePage(_UnitPage):
    UNITS = {"L":1,"mL":1000,"m³":0.001,"cm³":1000,"gallon":0.264172,
             "quart":1.05669,"pint":2.11338,"cup":4.22675,"fl oz":33.814}
    def __init__(self, p, c): super().__init__(p, c, "Volume", "🧪", "L")
    def _to_base(self, v, u): return v / self.UNITS[u]
    def _from_base(self, v, u): return v * self.UNITS[u]


class DataPage(_UnitPage):
    UNITS = {"bit":1,"byte":8,"KB":8e3,"MB":8e6,"GB":8e9,"TB":8e12,"PB":8e15}
    def __init__(self, p, c): super().__init__(p, c, "Data", "💾", "bit")
    def _to_base(self, v, u): return v * self.UNITS[u]
    def _from_base(self, v, u): return v / self.UNITS[u]


class TimePage(_UnitPage):
    UNITS = {"second":1,"minute":60,"hour":3600,"day":86400,
             "week":604800,"month":2.628e6,"year":3.156e7,"millisecond":0.001}
    def __init__(self, p, c): super().__init__(p, c, "Time", "⏱", "second")
    def _to_base(self, v, u): return v * self.UNITS[u]
    def _from_base(self, v, u): return v / self.UNITS[u]


class DatePage(BasePage):
    def __init__(self, p, c):
        super().__init__(p, c, "Date Difference", "📅")
        self.d1 = self._entry("Start  (YYYY-MM-DD)", 0)
        self.d2 = self._entry("End    (YYYY-MM-DD)", 1)
        self._calc_btn("Calculate", self._calc, 2)
        self.res = self._result_lbl(3)

    def _calc(self):
        try:
            d1 = datetime.strptime(self.d1.get(), "%Y-%m-%d").date()
            d2 = datetime.strptime(self.d2.get(), "%Y-%m-%d").date()
            diff = abs((d2 - d1).days)
            self.res.config(text=f"{diff} days\n≈ {round(diff/7,1)} weeks"
                                  f"  ≈ {round(diff/30.44,1)} months")
        except: self.res.config(text="Use format  YYYY-MM-DD")


class NumeralPage(BasePage):
    def __init__(self, p, c):
        super().__init__(p, c, "Numeral System", "🔢")
        self.val  = self._entry("Value", 0)
        opts = ["Decimal", "Binary", "Octal", "Hexadecimal"]
        self.frm  = self._dropdown("From", opts, 1)
        self.to_  = self._dropdown("To",   opts, 2)
        self._calc_btn("Convert", self._calc, 3)
        self.res  = self._result_lbl(4)

    def _calc(self):
        base = {"Decimal":10,"Binary":2,"Octal":8,"Hexadecimal":16}
        try:
            v    = int(self.val.get(), base[self.frm.get()])
            to_b = base[self.to_.get()]
            r    = (str(v) if to_b==10 else bin(v) if to_b==2
                    else oct(v) if to_b==8 else hex(v))
            self.res.config(text=r)
        except: self.res.config(text="Invalid input for selected base")


# ════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = App()
    app.mainloop()
