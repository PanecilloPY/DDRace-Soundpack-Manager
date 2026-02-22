# DDNet Audio Manager (Gestor de Audios)

Pequeña aplicación de escritorio para capturar y aplicar perfiles de audio del cliente DDNet.

## Descripción

`gestor_audios.py` es una GUI (basada en CustomTkinter) que permite:
- Capturar la carpeta `data/audio` del cliente DDNet y guardarla como perfil en `Documentos/DDnet-Audios`.
- Aplicar un perfil (copiar su carpeta `audio` a la instalación local de DDNet).
- Cambiar idioma de la UI entre Español, English y Русский.

## Requisitos

- Windows (probado).
- Python 3.10+.
- Virtual environment (recomendado).
- Dependencias (instalables con pip):
  - `customtkinter`

## Instalación rápida

1. Clona o descarga este repositorio.
2. En la carpeta del proyecto, crea y activa un entorno virtual:

```powershell
python -m venv venv
& venv\Scripts\Activate.ps1
```

3. Instala dependencias:

```powershell
pip install customtkinter
```

## Uso

1. Ejecuta la aplicación:

```powershell
python gestor_audios.py
```

2. En la pestaña `Ajustes` verifica o selecciona la ruta de tu instalación de DDNet (la carpeta que contiene `data/audio`).
3. Para crear un nuevo perfil: en `Ajustes` pulsa "Capturar Audio Actual" y dale un nombre.
4. Para aplicar un perfil: ve a `Perfiles` y pulsa el botón del perfil que quieras aplicar. La aplicación sustituirá la carpeta `data/audio` de la instalación por la del perfil.

## Ubicación de perfiles

Los perfiles se almacenan en:

```
%USERPROFILE%\Documents\DDnet-Audios\<NombrePerfil>\audio
```

Asegúrate de que el juego esté cerrado antes de aplicar un perfil.

## Crear un ejecutable (.exe)

1. Instala `PyInstaller` en tu entorno:

```powershell
pip install pyinstaller
```

2. Desde la raíz del proyecto genera el ejecutable con el siguiente comando (reemplaza `tu_icono.ico` por la ruta a tu icono):

```powershell
pyinstaller --noconsole --onefile --add-data "boton.mp3;." --add-data "pop.mp3;." --add-data "delete.mp3;." --icon="tu_icono.ico" gestor_audios.py
```

3. El ejecutable resultante se ubicará en `dist\gestor_audios.exe`. Si necesitas incluir archivos adicionales o recursos, edita el archivo `.spec` que genera `pyinstaller` y vuelve a construir.


## Contribuir

- Abre un issue para sugerencias o errores.
- Envía pull requests con mejoras.

## Licencia

Incluye la licencia que prefieras (por ejemplo MIT). Si no se especifica, se asume "Todos los derechos reservados".
