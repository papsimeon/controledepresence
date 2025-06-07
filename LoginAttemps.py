import tkinter as tk
from tkinter import ttk
import mysql.connector

# Connexion à la base de données MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="bchcontrole"
)

def fetch_data():
    """Récupère les données de la table login_attempts"""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM login_attempts")
    rows = cursor.fetchall()
    return rows

def load_data():
    """Charge les données dans le Treeview"""
    for i in tree.get_children():
        tree.delete(i)
    rows = fetch_data()
    for row in rows:
        tree.insert("", "end", values=row)

root = tk.Tk()
root.title("Affichage des tentatives de connexion")
root.geometry("800x600")

# Configuration des colonnes
columns = ("ID", "Nom d'utilisateur", "Date et Heure", "Tentatives")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

# Ajout des barres de défilement
scrollbar_y = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
scrollbar_y.pack(side="right", fill="y")

scrollbar_x = ttk.Scrollbar(root, orient="horizontal", command=tree.xview)
scrollbar_x.pack(side="bottom", fill="x")

tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

tree.pack(expand=True, fill="both")

# Charger les données
load_data()

root.mainloop()
