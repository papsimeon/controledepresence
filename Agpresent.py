from tkinter import *
import tkinter as tk
from tkinter import ttk
import cv2
from tkinter import ttk, messagebox
import openpyxl
from PIL import Image, ImageTk
from pyzbar.pyzbar import decode
import mysql.connector
from datetime import datetime
import pyttsx3
import locale
import os
import sys

# Définir la langue en français
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Connexion à la base de données MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="bchcontrole"
)
cursor = conn.cursor()

# Créer la table qragpresent si elle n'existe pas
cursor.execute("""
    CREATE TABLE IF NOT EXISTS qragpresent (
        id INT AUTO_INCREMENT PRIMARY KEY,
        matricule VARCHAR(20),
        nom VARCHAR(50),
        prenom VARCHAR(50),
        service VARCHAR(50),
        mention VARCHAR(100),
        statut VARCHAR(20),
        heurearrivee TIME,
        datepresence DATE,
        heurefin TIME
    )
""")

# Créer la table qragent si elle n'existe pas
cursor.execute("""
    CREATE TABLE IF NOT EXISTS qragent (
        id INT AUTO_INCREMENT PRIMARY KEY,
        matricule VARCHAR(20),
        nom VARCHAR(50),
        prenom VARCHAR(50),
        service VARCHAR(50),
        mention VARCHAR(100)
    )
""")

# Configuration de la voix en français pour pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Choisir la voix française

def update_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%A %d %B %Y")
    time_label.config(text=current_time)
    date_label.config(text=current_date.capitalize())
    root.after(1000, update_time)  # Met à jour l'heure toutes les secondes


def scanner_qr_and_save():
    def scan_qr():
        def start_capture():
            nonlocal capturing
            capturing = True
            capture_frame()
    
        def capture_frame():
            _, frame = scanner.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img_tk = ImageTk.PhotoImage(image=img)
            video_label.img = img_tk
            video_label.config(image=img_tk)
            decoded_objects = decode(frame)

            for obj in decoded_objects:
                if obj.type == 'QRCODE':
                    info = obj.data.decode('utf-8')
                    try:
                        matricule, nom, prenom, service, mention = info.split(",")
                        heurearrive = datetime.now().strftime("%H:%M:%S")
                        datepresence = datetime.now().strftime("%Y-%m-%d")
                        statut = "Présent"

                        matricule = matricule.strip("()'")
                        nom = nom.strip("()'")
                        prenom = prenom.strip("()'")
                        service = service.strip("()'")
                        mention = mention.strip("()'")

                        nom = nom.replace("'", "")
                        prenom = prenom.replace("'", "")
                        service = service.replace("'", "")
                        mention = mention.replace("'", "")

                        # Vérification de l'existence du matricule dans la table qragent
                        cursor.execute("SELECT * FROM qragent WHERE matricule = %s", (matricule,))
                        agent_record = cursor.fetchone()

                        if not agent_record:
                            engine = pyttsx3.init()
                            engine.say("Code QR non reconnu")
                            engine.runAndWait()
                        else:
                            # Vérification de la présence du matricule et de la date dans la table qragpresent
                            cursor.execute("SELECT * FROM qragpresent WHERE matricule = %s AND datepresence = %s", (matricule, datepresence))
                            existing_record = cursor.fetchone()

                            if existing_record:
                                engine = pyttsx3.init()
                                engine.say("Vous ête déjà présent")
                                engine.runAndWait()
                            else:
                                cursor.execute("""
                                    INSERT INTO qragpresent (matricule, nom, prenom, service, mention, statut, heurearrivee, datepresence)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                                """, (matricule, nom, prenom, service, mention, statut, heurearrive, datepresence))
                                conn.commit()
                                table_ag_present.insert('', 'end', values=(matricule, nom, prenom, service, mention, statut, heurearrive, datepresence))

                                engine = pyttsx3.init()
                                engine.say("Votre présence a été prise en compte.")
                                engine.runAndWait()

                                break
                    except ValueError:
                        engine = pyttsx3.init()
                        engine.say("Code QR non reconnu")
                        engine.runAndWait()

            if capturing:
                video_label.after(10, capture_frame)

        scanner = cv2.VideoCapture(0)
        capturing = False
        video_label.after(1000, start_capture)

    def update_time_in_new_window():
        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = datetime.now().strftime("%A %d %B %Y")
        time_label_new_window.config(text=current_time)
        date_label_new_window.config(text=current_date.capitalize())
        new_window.after(1000, update_time_in_new_window)

    new_window = tk.Toplevel(root)
    new_window.title("Scanner Code QR")
    new_window.geometry("1900x1080+0+0")
    new_window.config(bg="lightgray")

    

    video_label = tk.Label(new_window)
    video_label.pack()

    scan_button_arrivee = tk.Button(new_window, text="Marquez votre arrivée", command=scan_qr, cursor="hand2", font=("Comic Sans MS", 13), bd=5, relief=tk.GROOVE, bg="white")
    scan_button_arrivee.pack()

    scan_button_arrivee.bind("<Enter>", lambda e: scan_button_arrivee.config(bg='green', fg='white'))
    scan_button_arrivee.bind("<Leave>", lambda e: scan_button_arrivee.config(bg='white', fg='black'))

    columns = ("Matricule", "Nom", "Prenom", "Service", "Mention", "Statut", "Heure Arrivee", "Date", "Heure de fin")
    table_ag_present = ttk.Treeview(new_window, columns=columns, show='headings')
    for col in columns:
        table_ag_present.heading(col, text=col)
    
    scroll_x = ttk.Scrollbar(new_window, orient=HORIZONTAL, command=table_ag_present.xview)
    scroll_y = ttk.Scrollbar(new_window, orient=VERTICAL, command=table_ag_present.yview)
    
    table_ag_present.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
    
    scroll_x.pack(side=BOTTOM, fill=X)
    scroll_y.pack(side=RIGHT, fill=Y)
    
    table_ag_present.pack(fill=BOTH, expand=True)
    
    def afficher_agents():
        cursor.execute("SELECT * FROM qragpresent")
        result = cursor.fetchall()
        clear_table()
        for row_index, row in enumerate(result):
            table_ag_present.insert("", tk.END, values=row)

    def clear_table():
        table_ag_present.delete(*table_ag_present.get_children())

    afficher_agents()

    # En-tête avec l'heure
    time_label_new_window = tk.Label(new_window)
    time_label_new_window.place(x=1080, y=130)

    # Label pour afficher la date
    date_label_new_window = tk.Label(new_window, font=("Comic Sans MS", 14, "bold"),bg="lightgray", fg="black")
    date_label_new_window.place(x=970, y=3)

    # Ajouter le label pour l'heure dans la nouvelle fenêtre
    time_label_new_window = tk.Label(new_window, font=("Comic Sans MS", 15,"bold"),bg="lightgray", fg="black")
    time_label_new_window.place(x=1040, y=33)

    # Démarrer la mise à jour de l'heure dans la nouvelle fenêtre
    update_time_in_new_window()


def scanner_qr_and_save_depart():
    def scan_qr():
        def start_capture():
            nonlocal capturing
            capturing = True
            capture_frame()

        def capture_frame():
            _, frame = scanner.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img_tk = ImageTk.PhotoImage(image=img)
            video_label.img = img_tk
            video_label.config(image=img_tk)
            decoded_objects = decode(frame)

            for obj in decoded_objects:
                if obj.type == 'QRCODE':
                    info = obj.data.decode('utf-8')
                    matricule, nom, prenom, service, mention = info.split(",")
                    heurefin = datetime.now().strftime("%H:%M:%S")

                    matricule = matricule.strip("()'")
                    nom = nom.strip("()'")
                    prenom = prenom.strip("()'")
                    service = service.strip("()'")
                    mention = mention.strip("()'")

                    cursor.execute("SELECT * FROM qragpresent WHERE matricule = %s AND datepresence = %s", (matricule, datetime.now().strftime("%Y-%m-%d")))
                    existing_record = cursor.fetchone()

                    if existing_record:
                        cursor.execute("""
                            UPDATE qragpresent
                            SET heurefin = %s
                            WHERE matricule = %s AND datepresence = %s
                        """, (heurefin, matricule, datetime.now().strftime("%Y-%m-%d")))
                        conn.commit()

                        engine = pyttsx3.init()
                        engine.setProperty('voice', 'french')
                        engine.say("Votre départ a été enregistré.")
                        engine.runAndWait()
                    else:
                        engine = pyttsx3.init()
                        engine.setProperty('voice', 'french')
                        engine.say("Veuillez enregistrer d'abord l'heure d'arrivée.")
                        engine.runAndWait()

                    break

            if capturing:
                video_label.after(10, capture_frame)

        scanner = cv2.VideoCapture(0)
        capturing = False
        video_label.after(1000, start_capture)

    def update_time_in_new_window():
        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = datetime.now().strftime("%A %d %B %Y")
        time_label_new_window.config(text=current_time)
        date_label_new_window.config(text=current_date.capitalize())
        new_window.after(1000, update_time_in_new_window)

    new_window = tk.Toplevel(root)
    new_window.title("Scanner Code QR pour Départ")
    new_window.geometry("1900x1080+0+0")
    new_window.config(bg="lightgray")

    video_label = tk.Label(new_window)
    video_label.pack()

    scan_button_depart = tk.Button(new_window, text="Marquez votre départ", command=scan_qr, cursor="hand2", font=("Comic Sans MS", 13), bd=5, relief=tk.GROOVE, bg="white")
    scan_button_depart.pack()

    scan_button_depart.bind("<Enter>", lambda e: scan_button_depart.config(bg='red', fg='white'))
    scan_button_depart.bind("<Leave>", lambda e: scan_button_depart.config(bg='white', fg='black'))

    # En-tête avec l'heure
    time_label_new_window = tk.Label(new_window)
    time_label_new_window.place(x=1080, y=130)

    # Label pour afficher la date
    date_label_new_window = tk.Label(new_window, font=("Comic Sans MS", 15, "bold"),bg="lightgray", fg="black")
    date_label_new_window.place(x=950, y=25)

    # Ajouter le label pour l'heure dans la nouvelle fenêtre
    time_label_new_window = tk.Label(new_window, font=("Comic Sans MS", 16,"bold"),bg="lightgray", fg="black")
    time_label_new_window.place(x=1030, y=55)

    # Démarrer la mise à jour de l'heure dans la nouvelle fenêtre
    update_time_in_new_window()

    
    #***********Les fonctions du bouton marquer Départ
    def on_enter(event):
        scan_button_depart.config(bg='green', fg='white')

    def on_leave(event):
        scan_button_depart.config(bg='white', fg='black')

    video_label = tk.Label(new_window)
    video_label.pack()

    #Bouton marquer Départ
    
    #Evenement de changer la couleur du bouton marquer Départ
    scan_button_depart.bind("<Enter>", on_enter)
    scan_button_depart.bind("<Leave>", on_leave)


    def afficher_agents():
        cursor.execute("SELECT * FROM qragpresent")
        result = cursor.fetchall()
        clear_table()
        for row_index, row in enumerate(result):
            table_ag_present.insert("", tk.END, values=row)

    def clear_table():
        table_ag_present.delete(*table_ag_present.get_children())

    columns = ("Matricule", "Nom", "Prenom", "Service", "Mention", "Statut", "Heure Arrivee", "Date", "Heure de fin")
    table_ag_present = ttk.Treeview(new_window, columns=columns, show='headings')
    for col in columns:
        table_ag_present.heading(col, text=col)
    
    scroll_x = ttk.Scrollbar(new_window, orient=HORIZONTAL, command=table_ag_present.xview)
    scroll_y = ttk.Scrollbar(new_window, orient=VERTICAL, command=table_ag_present.yview)
    
    table_ag_present.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
    
    scroll_x.pack(side=BOTTOM, fill=X)
    scroll_y.pack(side=RIGHT, fill=Y)
    
    table_ag_present.pack(fill=BOTH, expand=True)
    afficher_agents()

def stop():
    root.destroy()

def quittez():
    root.destroy()

root = tk.Tk()
root.title("Marquez la Présence")
root.geometry("1920x1080+0+0")

title = tk.Label(text="GESTION DE PRESENCE DES AGENTS", font=("Comic Sans MS", 20, "bold"), bg="#9a82fa", fg="black", anchor="w").place(x=350, y=30)

#scan_qr_button_frame = tk.Frame(root, bg="lightgray", bd=5, relief=GROOVE)
#scan_qr_button_frame.place(x=435, y=120, width=500, height=520)

title = tk.Label(root, text="Marquer la présence", font=("Comic Sans MS", 18, "bold"), fg="black")
title.place(x=630, y=180)


# Charger l'image depuis le chemin spécifié
#image Akieni
image_path = resource_path("assets/akieni.png")
image = Image.open(image_path)
photo = ImageTk.PhotoImage(image)

# Redimensionner l'image si nécessaire
image = image.resize((300, 320), Image.Resampling.LANCZOS)
photo = ImageTk.PhotoImage(image)

# Créer un widget Label pour afficher l'image au milieu
label_image = Label(image=photo, bg="white")
label_image.bch = photo
label_image.place(relx=0.2, rely=0.5, anchor="center")

# En-tête avec la date et l'heure
header_frame = tk.Frame(root)
header_frame.place(x=990, y=90)

# Label pour afficher la date
date_label = tk.Label(header_frame, font=("Comic Sans MS", 15, "bold"), fg="black")
date_label.pack(side=tk.TOP)

# Label pour afficher l'heure
time_label = tk.Label(header_frame, font=("Comic Sans MS", 17, "bold"), fg="black")
time_label.pack(side=tk.TOP)

# Démarrer la mise à jour de la date et de l'heure
update_time()


#***********Les fonctions du bouton Arrivée
def on_enter(event):
    scan_qr_button_arrivee.config(bg='#9a82fa', fg='white')

def on_leave(event):
    scan_qr_button_arrivee.config(bg='white', fg='#9a82fa')

#Bouton Arrivée
scan_qr_button_arrivee = tk.Button(root, text="Arriver", command=scanner_qr_and_save, cursor="hand2", font=("Comic Sans MS", 13), bd=5, relief=tk.GROOVE,bg="white",fg="#9a82fa")
scan_qr_button_arrivee.place(x=520, y=280, width=130, height=50)

#evenement de changer la couleur du bouton Arrivé
scan_qr_button_arrivee.bind("<Enter>", on_enter)
scan_qr_button_arrivee.bind("<Leave>", on_leave)

#***********Les fonctions du bouton Départ
def on_enter(event):
    scan_qr_button_depart.config(bg='#9a82fa', fg='white')

def on_leave(event):
    scan_qr_button_depart.config(bg='white', fg='#9a82fa')

#Bouton Départ
scan_qr_button_depart = tk.Button(root, text="Départ", command=scanner_qr_and_save_depart, cursor="hand2", font=("Comic Sans MS", 13), bd=5, relief=tk.GROOVE,bg="white",fg="#9a82fa")
scan_qr_button_depart.place(x=520, y=360, width=130, height=50)

#Evenement de changer la couleur du bouton Départ
scan_qr_button_depart.bind("<Enter>", on_enter)
scan_qr_button_depart.bind("<Leave>", on_leave)


def quitter():
    root.destroy()

def retour():
    root.destroy()
    import Rapport

#***********Les fonctions du bouton rapport
def on_enter(event):
    btn_rapport_present.config(bg='#9a82fa', fg='white')

def on_leave(event):
    btn_rapport_present.config(bg='white', fg='#9a82fa')

btn_rapport_present = tk.Button(root, text="Rapport",command=retour ,cursor="hand2",font=("Comic Sans MS", 13),bd=5, relief=GROOVE,bg="white",fg="#9a82fa")
btn_rapport_present.place(x=700, y=310, width=130, height=60)

#evenement de changer la couleur du bouton rapport
btn_rapport_present.bind("<Enter>", on_enter)
btn_rapport_present.bind("<Leave>", on_leave)


#***********Les fonctions du bouton quitter
def on_enter(event):
    btn_quitter_present.config(bg='red', fg='white')

def on_leave(event):
    btn_quitter_present.config(bg='white', fg='red')

#Bouton quitter
btn_quitter_present = tk.Button(root, text="Quitter",command=quitter, cursor="hand2", font=("Comic Sans MS", 13), bd=5, relief=tk.GROOVE, fg="red",bg="white")
btn_quitter_present.place(x=880, y=310, width=130, height=60)

#evenement de changer la couleur du bouton quitter
btn_quitter_present.bind("<Enter>", on_enter)
btn_quitter_present.bind("<Leave>", on_leave)


root.mainloop()