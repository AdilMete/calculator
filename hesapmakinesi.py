import customtkinter as ctk
import math

# Görünüm Ayarları
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AhsenCalculatorPro(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Pencere Yapılandırması
        self.title("Ahsen Multi-Tool Pro v5.2")
        self.geometry("340x600")
        self.resizable(False, False)
        
        # Değişkenler
        self.current_mode = "Standart"
        self.is_dark = True 
        self.units = {
            "Metre": 1.0, "Santimetre": 0.01, "Kilometre": 1000.0,
            "İnç (in)": 0.0254, "Ayak (ft)": 0.3048, "Mil (mi)": 1609.34
        }

        # --- ARAYÜZ ELEMANLARI ---
        
        # Üst Panel
        self.top_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.top_panel.pack(fill="x", padx=20, pady=(15, 0))

        self.menu_btn = ctk.CTkButton(self.top_panel, text="≡", width=35, height=35,
                                     font=("Roboto", 22, "bold"), command=self.toggle_settings)
        self.menu_btn.pack(side="left")

        self.mode_label = ctk.CTkLabel(self.top_panel, text=self.current_mode, font=("Roboto", 18, "bold"))
        self.mode_label.pack(side="left", padx=15)

        # Giriş Ekranı
        self.entry = ctk.CTkEntry(self, width=300, height=70, font=("Roboto", 32), justify="right")
        self.entry.pack(pady=10, padx=20)

        # Mod Çerçeveleri
        self.std_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.sci_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.conv_frame = ctk.CTkFrame(self, fg_color="transparent")

        # Ayarlar Paneli (Başlangıçta gizli)
        self.settings_frame = ctk.CTkFrame(self, corner_radius=0)
        self.setup_settings_panel()

        # Butonları ve Arayüzleri Oluştur
        self.create_standard_buttons()
        self.create_scientific_buttons()
        self.create_converter_ui()
        
        # Başlangıç Modunu Göster
        self.show_mode("Standart")

    # --- AYARLAR VE TEMA MANTIĞI ---

    def setup_settings_panel(self):
        ctk.CTkLabel(self.settings_frame, text="AYARLAR", font=("Roboto", 20, "bold")).pack(pady=20)

        self.theme_btn = ctk.CTkButton(self.settings_frame, text="Aydınlık Mod", 
                                      fg_color="#555555", command=self.change_theme)
        self.theme_btn.pack(pady=10, padx=40, fill="x")

        ctk.CTkLabel(self.settings_frame, text="Mod Seçimi", font=("Roboto", 14)).pack(pady=(20, 5))
        for m in ["Standart", "Bilimsel", "Uzunluk"]:
            btn = ctk.CTkButton(self.settings_frame, text=m, 
                               command=lambda x=m: self.change_mode_from_settings(x))
            btn.pack(pady=5, padx=40, fill="x")

        ctk.CTkButton(self.settings_frame, text="Kapat", fg_color="transparent", 
                     border_width=1, command=self.toggle_settings).pack(pady=30)

    def toggle_settings(self):
        if self.settings_frame.winfo_ismapped():
            self.settings_frame.place_forget()
        else:
            self.settings_frame.place(x=0, y=0, relwidth=1, relheight=1)

    def change_theme(self):
        if self.is_dark:
            ctk.set_appearance_mode("light")
            self.theme_btn.configure(text="Karanlık Mod")
            self.is_dark = False
        else:
            ctk.set_appearance_mode("dark")
            self.theme_btn.configure(text="Aydınlık Mod")
            self.is_dark = True

    def change_mode_from_settings(self, new_mode):
        self.current_mode = new_mode
        self.show_mode(new_mode)
        self.toggle_settings()

    def show_mode(self, mode):
        for f in [self.std_frame, self.sci_frame, self.conv_frame]: f.pack_forget()
        self.mode_label.configure(text=mode)
        
        if mode == "Standart":
            self.geometry("340x580"); self.std_frame.pack(pady=10)
        elif mode == "Bilimsel":
            self.geometry("340x780"); self.sci_frame.pack(pady=10)
        else:
            self.geometry("340x650"); self.conv_frame.pack(pady=10)

    # --- BUTON OLUŞTURMA VE HESAPLAMA MANTIĞI ---

    def build_grid(self, frame, buttons, columns):
        row, col = 0, 0
        for btn_text in buttons:
            if btn_text in ['=', '+', '-', '*', '/', 'mod']: color, hover = "#1f6aa5", "#144870"
            elif btn_text in ['C', 'CE', '⌫']: color, hover = "#a33232", "#7a2525"
            else: color, hover = "#3d3d3d", "#2b2b2b"

            btn = ctk.CTkButton(frame, text=btn_text, width=70, height=55, corner_radius=8,
                               fg_color=color, hover_color=hover, command=lambda b=btn_text: self.tikla(b))
            btn.grid(row=row, column=col, padx=3, pady=3)
            col += 1
            if col >= columns: col = 0; row += 1

    def create_standard_buttons(self):
        btns = ['%', 'CE', 'C', '⌫', '1/x', 'x²', '√x', '/', '7', '8', '9', '*', '4', '5', '6', '-', '1', '2', '3', '+', '+/-', '0', ',', '=']
        self.build_grid(self.std_frame, btns, columns=4)

    def create_scientific_buttons(self):
        btns = ['sin', 'cos', 'tan', 'π', 'x²', 'x³', 'xʸ', 'e', '√x', '∛x', '10ˣ', 'ln', 'C', '⌫', 'mod', '/', '7', '8', '9', '*', '4', '5', '6', '-', '1', '2', '3', '+', '+/-', '0', ',', '=']
        self.build_grid(self.sci_frame, btns, columns=4)

    def create_converter_ui(self):
        ctk.CTkLabel(self.conv_frame, text="Şundan:").pack(pady=2)
        self.from_unit = ctk.CTkOptionMenu(self.conv_frame, values=list(self.units.keys()))
        self.from_unit.pack(pady=5)
        
        ctk.CTkLabel(self.conv_frame, text="Şuna:").pack(pady=2)
        self.to_unit = ctk.CTkOptionMenu(self.conv_frame, values=list(self.units.keys()))
        self.to_unit.pack(pady=5)
        
        self.convert_btn = ctk.CTkButton(self.conv_frame, text="DÖNÜŞTÜR", font=("Roboto", 14, "bold"), height=40, command=self.do_conversion)
        self.convert_btn.pack(pady=15)
        
        num_frame = ctk.CTkFrame(self.conv_frame, fg_color="transparent")
        num_frame.pack()
        nums = ['7', '8', '9', '4', '5', '6', '1', '2', '3', 'C', '0', '.']
        
        r, c = 0, 0 # İşte o hatanın düzeldiği yer!
        for n in nums:
            btn = ctk.CTkButton(num_frame, text=n, width=65, height=50, command=lambda x=n: self.tikla(x))
            btn.grid(row=r, column=c, padx=3, pady=3)
            c += 1
            if c > 2: c = 0; r += 1

    def tikla(self, deger):
        mevcut = self.entry.get()
        if mevcut in ["Hata", "Sayı girin!"]: self.entry.delete(0, 'end'); mevcut = ""
        
        if deger == 'C' or deger == 'CE': self.entry.delete(0, 'end')
        elif deger == '⌫': self.entry.delete(len(mevcut)-1, 'end')
        elif deger == ',': self.entry.insert('end', '.')
        elif deger == '=':
            try:
                islem = mevcut.replace('^', '**').replace('π', str(math.pi)).replace('e', str(math.e))
                sonuc = eval(islem)
                self.entry.delete(0, 'end'); self.entry.insert(0, str(sonuc))
            except: self.entry.delete(0, 'end'); self.entry.insert(0, "Hata")
        elif deger == '√x': self.hesapla_direkt(f"math.sqrt({mevcut})")
        elif deger == 'x²': self.hesapla_direkt(f"({mevcut})**2")
        elif deger == 'sin': self.hesapla_direkt(f"math.sin(math.radians({mevcut}))")
        elif deger == 'cos': self.hesapla_direkt(f"math.cos(math.radians({mevcut}))")
        elif deger == 'tan': self.hesapla_direkt(f"math.tan(math.radians({mevcut}))")
        else: self.entry.insert('end', deger)

    def hesapla_direkt(self, islem):
        try:
            sonuc = eval(islem)
            self.entry.delete(0, 'end'); self.entry.insert(0, str(sonuc))
        except: self.entry.delete(0, 'end'); self.entry.insert(0, "Hata")

    def do_conversion(self):
        try:
            val = float(self.entry.get())
            in_meters = val * self.units[self.from_unit.get()]
            result = in_meters / self.units[self.to_unit.get()]
            self.entry.delete(0, 'end'); self.entry.insert(0, f"{result:.4f}")
        except: self.entry.delete(0, 'end'); self.entry.insert(0, "Hata")

if __name__ == "__main__":
    app = AhsenCalculatorPro()
    app.mainloop()