import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
from tkinter import*
from tkinter import ttk, messagebox
from tkcalendar import *


def afficher_donnees():
    try:
        # Connexion à la base de données
        con = mysql.connector.connect(host="localhost", user="root", password="", database="bchcontrole")
        cur = con.cursor()
        
        # Exécution de la requête pour récupérer les données de la table `compteusers`
        cur.execute("SELECT * FROM compteusers")
        rows = cur.fetchall()
        
        # Suppression des anciennes données dans le tableau
        for row in tree.get_children():
            tree.delete(row)
        
        # Insertion des nouvelles données dans le tableau
        for row in rows:
            tree.insert("", tk.END, values=row)
        
        con.close()
    except Exception as ex:
        messagebox.showerror("Erreur", f"Erreur lors de la récupération des données: {str(ex)}", parent=root)

def tentative():
    import LoginAttemps

# Configuration de la fenêtre principale Tkinter
root = tk.Tk()
root.title("Affichage des utilisateurs")
root.geometry("600x400")
root.geometry("1920x1080+0+0")

title = Label(root, text="CONTROLE DE PRESENCE DES AGENTS", font=("Comic Sans MS", 20, "bold"), bg="white", fg="midnight blue", anchor="w").place(x=150, y=20)


# Création d'un tableau (Treeview) pour afficher les données
columns = ("matricule", "nom", "prenom", "login", "password")
tree = ttk.Treeview(root, columns=columns, show='headings')

tree.heading("matricule", text="Matricule")
tree.heading("nom", text="Nom")
tree.heading("prenom", text="Prénom")
tree.heading("login", text="Login")
tree.heading("password", text="Password")

# Ajustement de la largeur des colonnes

tree.column("matricule", width=100)
tree.column("nom", width=100)
tree.column("prenom", width=100)
tree.column("login", width=100)
tree.column("password", width=100)

# Placement du tableau dans la fenêtre
tree.pack(fill=tk.BOTH, expand=True)


        #***********Les fonctions du bouton connexion
def on_enter(event):
    btn_refresh.config(bg='green', fg='white')

def on_leave(event):
    btn_refresh.config(bg='white', fg='green')

        # Boutons btn Afficher
btn_refresh = tk.Button(root, text="Afficher", command=afficher_donnees,font=("Comic Sans MS", 13),cursor="hand2",bd=4, relief=GROOVE, bg="white",fg='green')
btn_refresh.place(x=560, y=430, width=120, height=50)

# Boutons btn Tentative
#btn_tentative_user = tk.Button(root, text="Tentative",command=tentative, cursor="hand2", bd=4, font=("Comic Sans MS", 13), relief=GROOVE, fg="black", bg="white")
#btn_tentative_user.place(x=590, y=430, width=150, height=50)
#btn_tentative_user.bind("<Enter>", lambda e: btn_tentative_user.config(bg='black', fg='white'))
#btn_tentative_user.bind("<Leave>", lambda e: btn_tentative_user.config(bg='white', fg='black'))


        #Evenement de changer la couleur du bouton btn refresh
btn_refresh.bind("<Enter>", on_enter)
btn_refresh.bind("<Leave>", on_leave)

# Bouton pour rafraîchir l'affichage des données btn refresh
#btn_refresh = tk.Button(root, text="Rafraîchir", command=afficher_donnees)
#btn_refresh.pack(pady=10)



# Lancement de l'application
root.mainloop()
