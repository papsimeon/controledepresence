from tkinter import*
from tkinter import ttk, messagebox
import tkinter as tk
from tkcalendar import *
from pymysql import cursors
from tkinter import Tk, Frame, Label, PhotoImage
import os
import mysql.connector
from PIL import Image, ImageTk
from datetime import datetime
import locale
import sys

# Définir la langue en français
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

#locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

root = tk.Tk()
root.geometry("500x500")
root.title("Menu")
root.geometry("1920x1080+0+0")
root.config(bg="white")
root.focus_force()

def menu():
    def ferme_menu():
        menu_frame.destroy()
        menu_btn.config(text="≡")
        menu_btn.config(command=menu)

    
    menu_frame = tk.Frame(root, bg="#9a82fa")

    #Les boutons
    #qrcode = tk.Button(menu_frame,command=codeqr, text="Par Qr code",cursor="hand2", font=("Comic Sans MS", 15, 'bold'), bg="white", fg="midnight blue",bd="0",activebackground="white").place(x=20, y=20)
    ag = tk.Button(menu_frame,command=gesagents, text="Ges Agents",cursor="hand2", font=("Comic Sans MS", 15, 'bold'), bg="white", fg="black",bd="0",activebackground="white").pack(fill=X, pady=3)
    
    #biometrie = tk.Button(menu_frame, command=acclbiometrie, text="Biometrie", cursor="hand2", font=("Comic Sans MS", 15, 'bold'), bg="white", fg="black", bd="0", activebackground="white")
    #biometrie.pack(fill=X, pady=10)
    #biometrie.config(state="disabled")

    Dash = tk.Button(menu_frame,command=dashboards, text="Dashbord",cursor="hand2", font=("Comic Sans MS", 15, 'bold'), bg="white", fg="black",bd="0",activebackground="white").pack(fill=X, pady=3)
    rap = tk.Button(menu_frame,command=gesrapports, text="Rapport",cursor="hand2", font=("Comic Sans MS", 15, 'bold'), bg="white", fg="black",bd="0",activebackground="white").pack(fill=X, pady=3)
    User = tk.Button(menu_frame,command=verificationuser, text="User",cursor="hand2", font=("Comic Sans MS", 15, 'bold'), bg="white", fg="black", bd="0",activebackground="white").pack(fill=X, pady=3)

    Quittez = tk.Button(menu_frame,command=quitter, text="Quitter",cursor="hand2", font=("Comic Sans MS", 15, 'bold'), bg="white", fg="black", bd="0",activebackground="white").pack(fill=X, pady=3)

    # cadre verticale
    hauteur = root.winfo_height()
    menu_frame.place(x=0, y=50, height=260, width=170)
    menu_btn.config(cursor="hand2",text="X")
    menu_btn.config(command=ferme_menu)

def update_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%A %d %B %Y")
    time_label.config(text=current_time)
    date_label.config(text=current_date.capitalize())
    root.after(1000, update_time)  # Met à jour l'heure toutes les secondes

entete_frame = tk.Frame(root, bg="#9a82fa", highlightbackground="white", highlightthickness=1)

#Bouton des 3 barres pour scroller le menu
menu_btn = tk.Button(entete_frame,cursor="hand2",text="≡", font=('bold', 19),bg="#9a82fa", fg="black",bd=0,activebackground="blue", activeforeground="white", command=menu)
menu_btn.pack(side=tk.LEFT,anchor=tk.W)

#Menu
menu_label = tk.Label(entete_frame,text="Menu", font=("Comic Sans MS", 15, 'bold'),bg="#9a82fa", fg="black")
menu_label.pack(side=tk.LEFT)

#cadre Horizontal la ou c'est écrit menu
entete_frame.pack(side=tk.TOP, fill=tk.X)
entete_frame.pack_propagate(False)
entete_frame.config(height=50)

#image bch
#image_path = "./assets/bchz.jpg"
image_path = resource_path("assets/akieni.png")
image = Image.open(image_path)
photo = ImageTk.PhotoImage(image)


image = image.resize((300, 320), Image.Resampling.LANCZOS)
photo = ImageTk.PhotoImage(image)

# Créer un widget Label pour afficher l'image au milieu 
label_image = Label(image=photo, bg="white")
label_image.bch = photo 
label_image.place(relx=0.5, rely=0.5, anchor="center")

gestion_title = tk.Label(entete_frame, text="Controle de présence", font=("Comic Sans MS", 22, "bold"), bg="#9a82fa",fg="black")
gestion_title.place(x=470, y=1)

# En-tête avec la date et l'heure
header_frame = tk.Frame(root, bg="white")
header_frame.place(x=970, y=60)

# Label pour afficher la date
date_label = tk.Label(header_frame, font=("Comic Sans MS", 16, "bold"), bg="white", fg="black")
date_label.pack(side=tk.TOP)

# Label pour afficher l'heure
time_label = tk.Label(header_frame, font=("Comic Sans MS", 17, "bold"), bg="white", fg="black")
time_label.pack(side=tk.TOP)

# Démarrer la mise à jour de la date et de l'heure
update_time()

def verificationuser():
    root.destroy()
    import LoginAdmin

#Fonction pour faire appel a la fenetre Accueil qr code
def gesagents():
    
    import Agent

def dashboards():
    
    import Dashboard

def gesrapports():
    
    import Rapport



def quitter():
    root.destroy()
    


root.mainloop()