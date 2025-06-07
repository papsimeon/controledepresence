from tkinter import *
import mysql.connector
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import messagebox
from datetime import datetime
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

def export_to_excel():
    try:
        # Connexion à la base de données MySQL
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bchcontrole"
        )
        cursor = conn.cursor()

        # Exécution de la requête pour récupérer les données
        query = "SELECT matricule, nom, prenom, service, mention, statut, heurearrivee, datepresence, heurefin FROM qragpresent"
        cursor.execute(query)
        result = cursor.fetchall()

        # Définir les colonnes de la table
        columns = ['matricule', 'nom', 'prenom', 'service', 'mention', 'statut', 'heurearrivee', 'datepresence', 'heurefin']

        # Créer un DataFrame pandas
        df = pd.DataFrame(result, columns=columns)

        # Convertir les colonnes de temps en chaînes de caractères au format 'HH:MM:SS'
        df['heurearrivee'] = df['heurearrivee'].apply(lambda x: (pd.Timestamp(0) + x).time().strftime('%H:%M:%S'))
        df['heurefin'] = df['heurefin'].apply(lambda x: (pd.Timestamp(0) + x).time().strftime('%H:%M:%S'))
        df['datepresence'] = df['datepresence'].astype(str)

        # Ouvrir une boîte de dialogue pour choisir l'emplacement de sauvegarde du fichier Excel
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
        if file_path:
            # Exporter le DataFrame vers un fichier Excel
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Succès", "Rapport exporté avec succès!")
        else:
            messagebox.showwarning("Annulé", "Exportation annulée.")

        # Fermer la connexion à la base de données
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")

def update_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%A %d %B %Y")
    time_label.config(text=current_time)
    date_label.config(text=current_date.capitalize())
    root.after(1000, update_time)  # Met à jour l'heure toutes les secondes

# Fonction pour faire appel à la fenêtre des présents
def rapport_present():
    #root.destroy()
    import Present

# Fonction pour faire appel à la fenêtre des absents
def rapport_absent():
    #root.destroy()
    import Absent

def rapport_dashboard():
    import Dashboard

# Création de l'interface Tkinter
root = tk.Tk()
root.title("Rapport")
root.geometry("1920x1080+0+0")
root.config(bg="lightgray")

title = Label(text="CONTROLE DE PRESENCE DES AGENTS", font=("Comic Sans MS", 20, "bold"), bg="#9a82fa", fg="black", anchor="w").place(x=370, y=20)

title = tk.Label(root, text="Génerer le Rapport", font=("Comic Sans MS", 20, "bold"), bg="lightgray", fg="black")
title.place(x=620, y=180)

# En-tête avec la date et l'heure
header_frame = tk.Frame(root, bg="lightgray")
header_frame.place(x=1030, y=90)

# Label pour afficher la date
date_label = tk.Label(header_frame, font=("Comic Sans MS", 15, "bold"), bg="lightgray", fg="black")
date_label.pack(side=tk.TOP)

# Label pour afficher l'heure
time_label = tk.Label(header_frame, font=("Comic Sans MS", 17, "bold"), bg="lightgray", fg="black")
time_label.pack(side=tk.TOP)

# Démarrer la mise à jour de la date et de l'heure
update_time()

# Charger l'image depuis le chemin spécifié
#image_path = "./assets/bchzz.jpg."  # Remplacez par le chemin de votre image
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

#***********Les fonctions du bouton rapport_present
def on_enter(event):
    rapport_present_button.config(bg='#9a82fa', fg='white')

def on_leave(event):
    rapport_present_button.config(bg='white', fg='black')

# Bouton rapport des présents
rapport_present_button = tk.Button(root, text="Presents", command=rapport_present, cursor="hand2", font=("Comic Sans MS", 13), bd=5, relief=tk.GROOVE, bg="white")
rapport_present_button.place(x=520, y=280, width=130, height=50)

# Événement de changer la couleur du bouton Présents
rapport_present_button.bind("<Enter>", on_enter)
rapport_present_button.bind("<Leave>", on_leave)


#***********Les fonctions du bouton rapport_absent
def on_enter(event):
    rapport_absent_button.config(bg='#9a82fa', fg='white')

def on_leave(event):
    rapport_absent_button.config(bg='white', fg='black')

# Bouton rapport des absents
rapport_absent_button = tk.Button(root, text="Absents", command=rapport_absent, cursor="hand2", font=("Comic Sans MS", 13), bd=5, relief=tk.GROOVE, bg="white")
#rapport_absent_button.place(x=480, y=287, width=130, height=60)
rapport_absent_button.place(x=520, y=360, width=130, height=60)

# Événement de changer la couleur du bouton rapport_absent
rapport_absent_button.bind("<Enter>", on_enter)
rapport_absent_button.bind("<Leave>", on_leave)


#***********Les fonctions du bouton export sur excel
def on_enter(event):
    export_button.config(bg='#9a82fa', fg='white')

def on_leave(event):
    export_button.config(bg='white', fg='black')

# Bouton pour lancer l'exportation pour générer le rapport
export_button = tk.Button(root, text="Exporter \n vers Excel", command=export_to_excel, cursor="hand2", font=("Comic Sans MS", 13), bd=5, relief=tk.GROOVE, bg="white")
#export_button.place(x=480, y=360, width=130, height=60)
export_button.place(x=700, y=280, width=130, height=60)

# Événement de changer la couleur du bouton export sur Excel
export_button.bind("<Enter>", on_enter)
export_button.bind("<Leave>", on_leave)


#***********Les fonctions du bouton Dashbord
def on_enter(event):
    rapport_dashboard_button.config(bg='#9a82fa', fg='white')

def on_leave(event):
    rapport_dashboard_button.config(bg='white', fg='black')

# Bouton rapport des Dashbord
rapport_dashboard_button = tk.Button(root, text="Dashbord", command=rapport_dashboard, cursor="hand2", font=("Comic Sans MS", 13), bd=5, relief=tk.GROOVE, bg="white")
rapport_dashboard_button.place(x=700, y=360, width=130, height=60)

# Événement de changer la couleur du bouton Dashbord
rapport_dashboard_button.bind("<Enter>", on_enter)
rapport_dashboard_button.bind("<Leave>", on_leave)

def quitter():
    root.destroy()



#***********Les fonctions du bouton retour
#def on_enter(event):
 #   btn_retour_present.config(bg='midnight blue', fg='white')

#def on_leave(event):
 #   btn_retour_present.config(bg='white', fg='black')

#btn_retour_present = tk.Button(root, text="Tableau \nde Bord", command=retour, cursor="hand2", font=("Comic Sans MS", 13), bd=5, relief=GROOVE, bg="white")
#btn_retour_present.place(x=690, y=287, width=130, height=60)

# Événement de changer la couleur du bouton retour
#btn_retour_present.bind("<Enter>", on_enter)
#btn_retour_present.bind("<Leave>", on_leave)

#***********Les fonctions du bouton quitter
def on_enter(event):
    btn_quitter_present.config(bg='red', fg='white')

def on_leave(event):
    btn_quitter_present.config(bg='white', fg='red')

# Bouton quitter
btn_quitter_present = tk.Button(root, text="Quitter", command=quitter, cursor="hand2", font=("Comic Sans MS", 13), bd=5, relief=tk.GROOVE, fg="red", bg="white")
btn_quitter_present.place(x=880, y=310, width=130, height=60)
                            
#btn_quitter_present.place(x=690, y=287, width=130, height=60)

# Événement de changer la couleur du bouton quitter
btn_quitter_present.bind("<Enter>", on_enter)
btn_quitter_present.bind("<Leave>", on_leave)

# Lancement de la boucle principale Tkinter
root.mainloop()