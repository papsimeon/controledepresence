from PyInstaller.utils.hooks import collect_submodules

# Chemin de la DLL
iconv_dll_path = "C:\Windows\System32\libiconv.dll"
#iconv_dll_path = "C:/path/to/libiconv.dll"  # Remplacez par le chemin correct

hiddenimports = [
    'cv2',           # OpenCV
    'datetime',
    'hashlib',
    'locale',
    'mysql.connector',
    'matplotlib.backends.backend_tkagg',
    'matplotlib.pyplot',
    'messagebox',
    'os',
    'openpyxl',
    'pymysql.cursors',
    'PIL.Image',
    'PIL.ImageTk',
    'pandas',
    'pyzbar.pyzbar',
    'pyttsx3',
    'qrcode',        # qrcode library
    're',
    'seaborn',
    'sys',
    'sqlalchemy',
    'tkinter',
    'tkinter.ttk',
    'tkcalendar',
] + collect_submodules('tkinter')

a = Analysis(
    ['Login.py', 'Menu.py', 'Agent.py', 'Agpresent.py', 'Rapport.py', 
     'Present.py', 'Absent.py','Dashboard.py', 'Compteuser.py'],
    pathex=[],
    #binaries=[],
    binaries=[(iconv_dll_path, '.')],
    datas=[
        ('assets/bccok.jpg', 'assets'),
        ('assets/akieni.png', 'assets'),
        ('assets/bchz.jpg', 'assets'),
        ('assets/bempreinteee.jpg', 'assets'),
        ('assets/bccoqr.jpg', 'assets'),
        ('assets/bchzz.jpg', 'assets')
    ],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Login',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False
)
