import os
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from pathlib import Path

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AudioSwitcher(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("DDNet Audio Manager - Pro Edition")
        self.geometry("700x670")
        self.configure(fg_color="#1E1E1E")

        # --- RUTAS Y ESTADOS ---
        self.ruta_juego = tk.StringVar(value=self.detectar_steam())
        self.idioma_actual = "Español"
        
        # Ruta en Documentos
        self.storage_path = Path(os.environ['USERPROFILE']) / "Documents" / "DDnet-Audios"
        self.storage_path.mkdir(parents=True, exist_ok=True)

        self.textos = {
            "Español": {
                "tab1": "Perfiles", "tab2": "Instrucciones", "tab3": "Ajustes",
                "titulo": "GESTOR DE AUDIO", "ruta_lbl": "Ruta de DDNet (Carpeta ddnet):",
                "btn_crear": "Capturar Audio Actual", "btn_buscar": "Seleccionar Carpeta",
                "btn_abrir_p": "Abrir Carpeta en Documentos", "btn_refresh": "Actualizar Lista",
                "dial_tit": "Nuevo Perfil", "dial_msg": "Nombre del perfil:",
                "inst": "1. En 'Ajustes', verifica la ruta de tu carpeta 'ddnet'.\n\n2. Los perfiles se guardan en: Documentos/DDnet-Audios.\n\n3. Cada perfil debe ser una carpeta con una subcarpeta llamada 'audio' dentro.",
                "msg_exito": "¡Perfil aplicado con éxito!", "msg_error": "Error: ¿Cerraste el juego?"
            },
            "English": {
                "tab1": "Profiles", "tab2": "How to Use", "tab3": "Settings",
                "titulo": "AUDIO MANAGER", "ruta_lbl": "DDNet Path (ddnet folder):",
                "btn_crear": "Capture Current Audio", "btn_buscar": "Select Folder",
                "btn_abrir_p": "Open Documents Folder", "btn_refresh": "Refresh List",
                "dial_tit": "New Profile", "dial_msg": "Profile name:",
                "inst": "1. In 'Settings', check your 'ddnet' folder path.\n\n2. Profiles are stored in: Documents/DDnet-Audios.\n\n3. Each profile must be a folder with an 'audio' subfolder inside.",
                "msg_exito": "Profile applied successfully!", "msg_error": "Error: Is the game closed?"
            },
            "Русский": {
                "tab1": "Профили", "tab2": "Инструкция", "tab3": "Настройки",
                "titulo": "МЕНЕДЖЕР ЗВУКА", "ruta_lbl": "Путь к DDNet (папка ddnet):",
                "btn_crear": "Захватить текущий звук", "btn_buscar": "Выбрать папку",
                "btn_abrir_p": "Открыть папку в Документах", "btn_refresh": "Обновить список",
                "dial_tit": "Новый профиль", "dial_msg": "Имя профиля:",
                "inst": "1. В 'Настройках' проверьте путь к папке 'ddnet'.\n\n2. Профили хранятся в: Документы/DDnet-Audios.\n\n3. Каждый профиль должен быть папкой с подпапкой 'audio'.",
                "msg_exito": "Профиль успешно применен!", "msg_error": "Ошибка: Игра закрыта?"
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

        # --- PESTAÑA PERFILES ---
        header_frame = ctk.CTkFrame(self.tab_perfiles, fg_color="transparent")
        header_frame.pack(fill="x", pady=10)

        self.lbl_perf_titulo = ctk.CTkLabel(header_frame, text="", font=("SF Pro Display", 22, "bold"))
        self.lbl_perf_titulo.pack(side="left", padx=20)

        self.btn_refresh = ctk.CTkButton(header_frame, text="↻", width=40, corner_radius=10, 
                                          fg_color="#333", hover_color="#007AFF", command=self.cargar_lista_perfiles)
        self.btn_refresh.pack(side="right", padx=20)
        
        self.scroll_frame = ctk.CTkScrollableFrame(self.tab_perfiles, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.progress = ctk.CTkProgressBar(self.tab_perfiles, height=8, corner_radius=10, progress_color="#007AFF")
        self.progress.set(0)
        self.progress.pack(pady=15, fill="x", padx=40)

        # --- PESTAÑA INSTRUCCIONES ---
        self.txt_instrucciones = ctk.CTkLabel(self.tab_instrucciones, text="", font=("SF Pro Text", 16), wraplength=550, justify="left")
        self.txt_instrucciones.pack(pady=40, padx=30)

        # --- PESTAÑA AJUSTES ---
        self.lbl_ruta = ctk.CTkLabel(self.tab_ajustes, text="")
        self.lbl_ruta.pack(pady=(20, 5))
        
        self.entry_ruta = ctk.CTkEntry(self.tab_ajustes, textvariable=self.ruta_juego, width=520, state="readonly", fg_color="#121212")
        self.entry_ruta.pack(pady=5)
        
        self.btn_buscar = ctk.CTkButton(self.tab_ajustes, text="", command=self.seleccionar_ruta, corner_radius=10)
        self.btn_buscar.pack(pady=10)

        ctk.CTkFrame(self.tab_ajustes, height=2, fg_color="#333333").pack(fill="x", pady=20, padx=60)

        self.btn_capturar = ctk.CTkButton(self.tab_ajustes, text="", fg_color="#28a745", hover_color="#218838", 
                                          command=self.crear_nuevo_perfil, corner_radius=12)
        self.btn_capturar.pack(pady=5)

        self.btn_abrir_storage = ctk.CTkButton(self.tab_ajustes, text="", fg_color="#444444", hover_color="#555555", 
                                               command=self.abrir_carpeta_perfiles, corner_radius=12)
        self.btn_abrir_storage.pack(pady=10)

        self.combo_lang = ctk.CTkComboBox(self.tab_ajustes, values=["Español", "English", "Русский"], 
                                          command=self.cambiar_idioma, state="readonly", corner_radius=10)
        self.combo_lang.set("Español")
        self.combo_lang.pack(pady=20)

        self.cargar_lista_perfiles()

    def actualizar_textos(self):
        t = self.textos[self.idioma_actual]
        self.tabview._segmented_button._buttons_dict["Perfiles"].configure(text=t["tab1"])
        self.tabview._segmented_button._buttons_dict["Instrucciones"].configure(text=t["tab2"])
        self.tabview._segmented_button._buttons_dict["Ajustes"].configure(text=t["tab3"])
        
        self.lbl_perf_titulo.configure(text=t["tab1"])
        self.txt_instrucciones.configure(text=t["inst"])
        self.lbl_ruta.configure(text=t["ruta_lbl"])
        self.btn_buscar.configure(text=t["btn_buscar"])
        self.btn_capturar.configure(text=t["btn_crear"])
        self.btn_abrir_storage.configure(text=t["btn_abrir_p"])

    def cambiar_idioma(self, nuevo_idioma):
        self.idioma_actual = nuevo_idioma
        self.actualizar_textos()

    def seleccionar_ruta(self):
        path = filedialog.askdirectory(title="Selecciona la carpeta 'ddnet'")
        if path:
            self.ruta_juego.set(path)

    def abrir_carpeta_perfiles(self):
        if os.path.exists(self.storage_path):
            subprocess.Popen(f'explorer "{self.storage_path}"')

    def cargar_lista_perfiles(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if self.storage_path.exists():
            perfiles = sorted([f for f in self.storage_path.iterdir() if f.is_dir()])
            for p in perfiles:
                btn = ctk.CTkButton(self.scroll_frame, text=f"  🔊  {p.name}", 
                                    anchor="w", height=48, corner_radius=12,
                                    fg_color="#2D2D2D", hover_color="#007AFF",
                                    command=lambda n=p.name: self.aplicar_perfil(n))
                btn.pack(pady=4, fill="x", padx=10)

    def crear_nuevo_perfil(self):
        t = self.textos[self.idioma_actual]
        # Diálogo con idioma dinámico
        dialog = ctk.CTkInputDialog(text=t["dial_msg"], title=t["dial_tit"])
        nombre = dialog.get_input()
        
        if nombre:
            origen = Path(self.ruta_juego.get()) / "data" / "audio"
            destino = self.storage_path / nombre / "audio"
            
            if origen.exists():
                shutil.copytree(origen, destino, dirs_exist_ok=True)
                self.cargar_lista_perfiles()
                messagebox.showinfo("DDNet", "OK!")
            else:
                messagebox.showerror("Error", f"Path not found:\n{origen}")

    def aplicar_perfil(self, nombre_perfil):
        try:
            self.progress.set(0.3)
            self.update()

            origen = self.storage_path / nombre_perfil / "audio"
            destino = Path(self.ruta_juego.get()) / "data" / "audio"

            if not origen.exists():
                raise Exception(f"Error: subfolder 'audio' not found in {nombre_perfil}")

            if destino.exists():
                shutil.rmtree(destino)
            
            self.progress.set(0.7)
            self.update()
            
            shutil.copytree(origen, destino)
            
            self.progress.set(1.0)
            messagebox.showinfo("DDNet", self.textos[self.idioma_actual]["msg_exito"])
        except Exception as e:
            messagebox.showerror("Error", f"{self.textos[self.idioma_actual]['msg_error']}\n\n{e}")
        finally:
            self.after(1000, lambda: self.progress.set(0))

if __name__ == "__main__":
    app = AudioSwitcher()
    app.mainloop()