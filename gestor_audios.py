import os
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
from pathlib import Path
import webbrowser
import sys
import ctypes

# --- SECCIÓN: CONFIGURACIÓN DE RUTAS PARA .EXE (PyInstaller) ---
def get_resource_path(relative_path):
    """ Obtiene la ruta absoluta de los recursos, funciona para .py y para .exe """
    try:
        base_path = Path(sys._MEIPASS)
    except Exception:
        base_path = Path(os.path.abspath("."))
    return base_path / relative_path

def play_sound(filename):
    sound_path = get_resource_path(filename)
    if not sound_path.exists():
        return
    try:
        # MCI para Windows: reproduce MP3 sin librerías externas
        ctypes.windll.winmm.mciSendStringW(f'close all', None, 0, None)
        ctypes.windll.winmm.mciSendStringW(f'open "{sound_path}" type mpegvideo alias mp3', None, 0, None)
        ctypes.windll.winmm.mciSendStringW(f'play mp3', None, 0, None)
    except:
        pass

# --- SECCIÓN: DIÁLOGOS PERSONALIZADOS ---
class CustomDialog(ctk.CTkToplevel):
    def __init__(self, parent, title, text, confirm_handler, type="confirm"):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x220")
        self.resizable(False, False)
        self.configure(fg_color="#1E1E1E")
        self.after(100, self.lift)
        self.attributes('-topmost', True)
        self.grab_set() 
        
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 200
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 110
        self.geometry(f"+{x}+{y}")

        play_sound("pop.mp3")

        self.label = ctk.CTkLabel(self, text=text, font=("SF Pro Text", 15), wraplength=320)
        self.label.pack(expand=True, pady=(30, 10))

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=25)

        t = parent.textos[parent.idioma_actual]

        if type == "confirm":
            self.btn_ok = ctk.CTkButton(btn_frame, text=t["btn_confirm"], fg_color="#cc241d", hover_color="#fb4934", width=120,
                                        command=lambda: [play_sound("delete.mp3"), confirm_handler(), self.destroy()])
            self.btn_ok.pack(side="left", padx=10)
            self.btn_cancel = ctk.CTkButton(btn_frame, text=t["btn_cancel"], fg_color="#444", width=120,
                                            command=self.destroy)
            self.btn_cancel.pack(side="left", padx=10)
        else:
            self.btn_close = ctk.CTkButton(btn_frame, text="OK", command=self.destroy, width=120)
            self.btn_close.pack()

# --- SECCIÓN: APLICACIÓN PRINCIPAL ---
class AudioSwitcher(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DDNet Audio Manager - Made by Fiji")
        self.geometry("750x850")
        self.configure(fg_color="#1E1E1E")

        # SONIDO GLOBAL
        self.bind_all("<Button-1>", lambda e: play_sound("boton.mp3"))

        self.ruta_juego = tk.StringVar(value=self.detectar_steam())
        self.idioma_actual = "Español"
        self.storage_path = Path(os.environ['USERPROFILE']) / "Documents" / "DDnet-Audios"
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.switches_dict = {}
        self.perfil_activo_nombre = None

        self.textos = {
            "Español": {
                "tab1": "Perfiles", "tab2": "Instrucciones", "tab3": "Ajustes",
                "ruta_lbl": "Ruta de DDNet (Carpeta ddnet):",
                "btn_crear": "Capturar Audio Actual", "btn_buscar": "Seleccionar Carpeta",
                "btn_abrir_p": "Abrir Carpeta en Documentos", "btn_refresh": "Actualizar Lista",
                "dial_tit": "Nuevo Perfil", "dial_msg": "Nombre del perfil:",
                "inst_t": "Guía de Uso Rápido",
                "inst_1": "📂 1. Configura la ruta de 'ddnet' en Ajustes.",
                "inst_2": "📥 2. 'Capturar' copiará tus sonidos actuales.",
                "inst_3": "🔄 3. Usa el Switch para activar un pack.",
                "inst_4": "💾 4. Ubicación: Documentos/DDnet-Audios",
                "credits": "Desarrollado por Fiji", "discord_btn": "Contactar en Discord",
                "confirm_del": "¿Eliminar este pack de audio?",
                "btn_confirm": "Eliminar", "btn_cancel": "Cancelar",
                "rename_tit": "Renombrar", "rename_msg": "Nuevo nombre:"
            },
            "English": {
                "tab1": "Profiles", "tab2": "Instructions", "tab3": "Settings",
                "ruta_lbl": "DDNet Path (ddnet folder):",
                "btn_crear": "Capture Current Audio", "btn_buscar": "Select Folder",
                "btn_abrir_p": "Open Documents Folder", "btn_refresh": "Refresh List",
                "dial_tit": "New Profile", "dial_msg": "Profile name:",
                "inst_t": "Quick Start Guide",
                "inst_1": "📂 1. Set your 'ddnet' folder path in Settings.",
                "inst_2": "📥 2. 'Capture' will copy your current sounds.",
                "inst_3": "🔄 3. Use the Switch to activate a pack.",
                "inst_4": "💾 4. Location: Documents/DDnet-Audios",
                "credits": "Made by Fiji", "discord_btn": "Contact on Discord",
                "confirm_del": "Delete this audio pack?",
                "btn_confirm": "Delete", "btn_cancel": "Cancel",
                "rename_tit": "Rename", "rename_msg": "New name:"
            },
            "Русский": {
                "tab1": "Профили", "tab2": "Инструкция", "tab3": "Настройки",
                "ruta_lbl": "Путь к DDNet (папка ddnet):",
                "btn_crear": "Захватить звук", "btn_buscar": "Выбрать папку",
                "btn_abrir_p": "Открыть папку в Документах", "btn_refresh": "Обновить список",
                "dial_tit": "Новый профиль", "dial_msg": "Имя профиля:",
                "inst_t": "Быстрое руководство",
                "inst_1": "📂 1. Укажите путь к папке 'ddnet' в Настройках.",
                "inst_2": "📥 2. 'Захватить' скопирует текущие звуки.",
                "inst_3": "🔄 3. Используйте переключатель для активации.",
                "inst_4": "💾 4. Путь: Документы/DDnet-Audios",
                "credits": "Создано Fiji", "discord_btn": "Связаться в Discord",
                "confirm_del": "Удалить этот аудио пак?",
                "btn_confirm": "Удалить", "btn_cancel": "Отмена",
                "rename_tit": "Переименовать", "rename_msg": "Новое имя:"
            }
        }
        self.setup_ui()
        self.actualizar_textos()

    def detectar_steam(self):
        ruta_std = Path(r"C:\Program Files (x86)\Steam\steamapps\common\DDraceNetwork\ddnet")
        return str(ruta_std) if ruta_std.exists() else "No detectado"

    def setup_ui(self):
        self.tabview = ctk.CTkTabview(self, segmented_button_selected_color="#007AFF", corner_radius=25)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)
        self.tab_perfiles = self.tabview.add("Perfiles")
        self.tab_instrucciones = self.tabview.add("Instrucciones")
        self.tab_ajustes = self.tabview.add("Ajustes")

        header_frame = ctk.CTkFrame(self.tab_perfiles, fg_color="transparent")
        header_frame.pack(fill="x", pady=10)
        self.lbl_perf_titulo = ctk.CTkLabel(header_frame, text="", font=("SF Pro Display", 22, "bold"))
        self.lbl_perf_titulo.pack(side="left", padx=20)
        self.btn_refresh = ctk.CTkButton(header_frame, text="↻", width=40, corner_radius=10, 
                                          fg_color="#333", hover_color="#007AFF", 
                                          command=self.cargar_lista_perfiles)
        self.btn_refresh.pack(side="right", padx=20)
        
        self.scroll_frame = ctk.CTkScrollableFrame(self.tab_perfiles, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.progress = ctk.CTkProgressBar(self.tab_perfiles, height=8, corner_radius=10, progress_color="#28a745")
        self.progress.set(0)
        self.progress.pack(pady=15, fill="x", padx=40)

        self.inst_container = ctk.CTkFrame(self.tab_instrucciones, fg_color="transparent")
        self.inst_container.pack(expand=True, fill="both", padx=30, pady=20)
        self.lbl_inst_title = ctk.CTkLabel(self.inst_container, text="", font=("SF Pro Display", 24, "bold"), text_color="#007AFF")
        self.lbl_inst_title.pack(pady=10)
        self.step_widgets = []
        for i in range(4):
            btn = ctk.CTkButton(self.inst_container, text="", font=("SF Pro Text", 14), anchor="w", 
                                fg_color="#2D2D2D", height=55, corner_radius=15, state="disabled")
            btn.pack(fill="x", pady=7)
            self.step_widgets.append(btn)

        self.lbl_ruta = ctk.CTkLabel(self.tab_ajustes, text="")
        self.lbl_ruta.pack(pady=(10, 5))
        self.entry_ruta = ctk.CTkEntry(self.tab_ajustes, textvariable=self.ruta_juego, width=520, state="readonly", fg_color="#121212")
        self.entry_ruta.pack(pady=5)
        self.btn_buscar = ctk.CTkButton(self.tab_ajustes, text="", command=self.seleccionar_ruta, corner_radius=10)
        self.btn_buscar.pack(pady=10)

        ctk.CTkFrame(self.tab_ajustes, height=2, fg_color="#333333").pack(fill="x", pady=15, padx=60)
        self.btn_capturar = ctk.CTkButton(self.tab_ajustes, text="", fg_color="#28a745", hover_color="#218838", 
                                          command=self.crear_nuevo_perfil, corner_radius=12)
        self.btn_capturar.pack(pady=5)
        self.btn_abrir_storage = ctk.CTkButton(self.tab_ajustes, text="", fg_color="#444444", hover_color="#555555", 
                                               command=self.abrir_carpeta_perfiles, corner_radius=12)
        self.btn_abrir_storage.pack(pady=10)

        self.combo_lang = ctk.CTkComboBox(self.tab_ajustes, values=["Español", "English", "Русский"], 
                                          command=self.cambiar_idioma, state="readonly", corner_radius=10)
        self.combo_lang.set("Español")
        self.combo_lang.pack(pady=10)

        self.credit_frame = ctk.CTkFrame(self.tab_ajustes, fg_color="#121212", corner_radius=15)
        self.credit_frame.pack(fill="x", padx=40, pady=20, side="bottom") 
        self.lbl_credits = ctk.CTkLabel(self.credit_frame, text="", font=("SF Pro Text", 14, "italic"))
        self.lbl_credits.pack(pady=(10, 5))
        self.btn_discord = ctk.CTkButton(self.credit_frame, text="", fg_color="#5865F2", hover_color="#4752C4", 
                                         command=lambda: webbrowser.open("https://discord.com/users/memarksme"), corner_radius=10)
        self.btn_discord.pack(pady=(0, 15))

    def actualizar_textos(self):
        t = self.textos[self.idioma_actual]
        for i, tab in enumerate(["Perfiles", "Instrucciones", "Ajustes"]):
            self.tabview._segmented_button._buttons_dict[tab].configure(text=t[f"tab{i+1}"])
        self.lbl_perf_titulo.configure(text=t["tab1"])
        self.lbl_ruta.configure(text=t["ruta_lbl"])
        self.btn_buscar.configure(text=t["btn_buscar"])
        self.btn_capturar.configure(text=t["btn_crear"])
        self.btn_abrir_storage.configure(text=t["btn_abrir_p"])
        self.lbl_inst_title.configure(text=t["inst_t"])
        for i, btn in enumerate(self.step_widgets): btn.configure(text=t[f"inst_{i+1}"])
        self.lbl_credits.configure(text=t["credits"])
        self.btn_discord.configure(text=t["discord_btn"])
        self.cargar_lista_perfiles()

    def cambiar_idioma(self, n):
        self.idioma_actual = n
        self.actualizar_textos()

    def cargar_lista_perfiles(self):
        for w in self.scroll_frame.winfo_children(): w.destroy()
        self.switches_dict = {}
        if not self.storage_path.exists(): return
        for p in sorted([f for f in self.storage_path.iterdir() if f.is_dir()]):
            row = ctk.CTkFrame(self.scroll_frame, fg_color="#2D2D2D", corner_radius=12)
            row.pack(pady=5, fill="x", padx=10)
            ctk.CTkLabel(row, text=f" 🔊 {p.name}", font=("SF Pro Text", 14, "bold")).pack(side="left", padx=15, pady=10)
            ctk.CTkButton(row, text="🗑", width=35, fg_color="#cc241d", hover_color="#fb4934",
                          command=lambda path=p: self.confirm_delete_ui(path)).pack(side="right", padx=10)
            ctk.CTkButton(row, text="✏️", width=35, fg_color="#444", hover_color="#666",
                          command=lambda path=p: self.renombrar_perfil(path)).pack(side="right", padx=5)
            sw_var = tk.BooleanVar(value=(self.perfil_activo_nombre == p.name))
            sw = ctk.CTkSwitch(row, text="", variable=sw_var, width=50, progress_color="#28a745",
                               command=lambda n=p.name, v=sw_var: self.handle_switch(n, v))
            sw.pack(side="right", padx=10)
            self.switches_dict[p.name] = (sw, sw_var)

    def handle_switch(self, nombre, variable):
        if variable.get():
            for name, (widget, var) in self.switches_dict.items():
                if name != nombre: var.set(False)
            self.aplicar_perfil(nombre)
            self.perfil_activo_nombre = nombre
        else:
            if self.perfil_activo_nombre == nombre:
                self.perfil_activo_nombre = None

    def confirm_delete_ui(self, path):
        t = self.textos[self.idioma_actual]
        CustomDialog(self, t["tab1"], t["confirm_del"], lambda: self.eliminar_perfil(path))

    def eliminar_perfil(self, path):
        if self.perfil_activo_nombre == path.name: self.perfil_activo_nombre = None
        shutil.rmtree(path)
        self.cargar_lista_perfiles()

    def renombrar_perfil(self, path):
        t = self.textos[self.idioma_actual]
        dialog = ctk.CTkInputDialog(text=t["rename_msg"], title=t["rename_tit"])
        nuevo_nombre = dialog.get_input()
        if nuevo_nombre:
            if self.perfil_activo_nombre == path.name: self.perfil_activo_nombre = nuevo_nombre
            path.rename(path.parent / nuevo_nombre)
            self.cargar_lista_perfiles()

    def seleccionar_ruta(self):
        path = filedialog.askdirectory()
        if path: self.ruta_juego.set(path)

    def abrir_carpeta_perfiles(self):
        if self.storage_path.exists(): subprocess.Popen(f'explorer "{self.storage_path}"')

    def crear_nuevo_perfil(self):
        t = self.textos[self.idioma_actual]
        dialog = ctk.CTkInputDialog(text=t["dial_msg"], title=t["dial_tit"])
        nombre = dialog.get_input()
        if nombre:
            origen = Path(self.ruta_juego.get()) / "data" / "audio"
            destino = self.storage_path / nombre / "audio"
            if origen.exists():
                shutil.copytree(origen, destino, dirs_exist_ok=True)
                self.cargar_lista_perfiles()
                play_sound("pop.mp3")

    def aplicar_perfil(self, nombre):
        try:
            self.progress.set(0.1); self.update()
            origen = self.storage_path / nombre / "audio"
            destino = Path(self.ruta_juego.get()) / "data" / "audio"
            if not origen.exists(): return
            if destino.exists(): shutil.rmtree(destino)
            shutil.copytree(origen, destino)
            self.progress.set(1.0)
        except:
            if nombre in self.switches_dict: self.switches_dict[nombre][1].set(False)
        finally:
            self.after(1000, lambda: self.progress.set(0))

if __name__ == "__main__":
    AudioSwitcher().mainloop()
