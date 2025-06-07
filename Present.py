from tkinter import *
import tkinter as tk
import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
#from fpdf import FPDF
from tkinter import messagebox
import pandas as pd
from tkcalendar import Calendar
import matplotlib.pyplot as plt
from datetime import datetime, time
import locale

# Définir la langue en français
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

hiddenimports=['mysql.connector']


def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="bchcontrole"
    )

#fonction supprimer_agents
def supprimer_agents():
    selected_items = table_present.selection()
    if not selected_items:
        messagebox.showwarning("Avertissement", "Veuillez sélectionner un agent à supprimer.")
        return
    
    confirm = messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer les agents sélectionnés ?")
    if not confirm:
        return

    conn = connect_db()
    cursor = conn.cursor()

    for item in selected_items:
        values = table_present.item(item, "values")
        matricule = values[0]
        datepresence = values[7]

        query = "DELETE FROM qragpresent WHERE matricule = %s AND datepresence = %s"
        cursor.execute(query, (matricule, datepresence))
        table_present.delete(item)
    
    conn.commit()
    conn.close()
    messagebox.showinfo("Succès", "Agent(s) supprimé(s) avec succès.")

def afficher_presents():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM qragpresent")
    presents = cursor.fetchall()
    conn.close()

    for row in table_present.get_children():
        table_present.delete(row)
    
    for present in presents:
        table_present.insert("", "end", values=present)

def rechercher_presents():
    
    critere = combobox_critere_present.get()
    valeur = entry_valeur_present.get()

    conn = connect_db()
    cursor = conn.cursor()

    query = f"SELECT * FROM qragpresent WHERE {critere} = %s"
    params = (valeur,)

    cursor.execute(query, params)
    presents = cursor.fetchall()
    conn.close()

    for row in table_present.get_children():
        table_present.delete(row)
    
    for present in presents:
        table_present.insert("", "end", values=present)

def afficher_presents_par_date(date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM qragpresent WHERE datepresence = %s", (date,))
    presents = cursor.fetchall()
    conn.close()

    for row in table_present.get_children():
        table_present.delete(row)
    
    for present in presents:
        table_present.insert("", "end", values=present)

def afficher_presents_par_semaine(start_date, end_date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM qragpresent WHERE datepresence BETWEEN %s AND %s", (start_date, end_date))
    presents = cursor.fetchall()
    conn.close()

    for row in table_present.get_children():
        table_present.delete(row)
    
    for present in presents:
        table_present.insert("", "end", values=present)

def afficher_presents_par_mois(year_month):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM qragpresent WHERE DATE_FORMAT(datepresence, '%%Y-%%m') = %s", (year_month,))
    presents = cursor.fetchall()
    conn.close()

    for row in table_present.get_children():
        table_present.delete(row)
    
    for present in presents:
        table_present.insert("", "end", values=present)

def afficher_presents_par_annee(year):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM qragpresent WHERE YEAR(datepresence) = %s", (year,))
    presents = cursor.fetchall()
    conn.close()

    for row in table_present.get_children():
        table_present.delete(row)
    
    for present in presents:
        table_present.insert("", "end", values=present)

def courbe_presents():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT nom, datepresence FROM qragpresent ORDER BY datepresence")
    presents = cursor.fetchall()
    conn.close()

    noms_presents = [row[0] for row in presents]
    dates_presents = [row[1] for row in presents]

    plt.figure(figsize=(10, 6))
    plt.plot(dates_presents, noms_presents, marker='o')
    plt.xlabel("Date de présence")
    plt.ylabel("Nom")
    plt.title("Courbe des présences des agents")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def update_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%A %d %B %Y")
    time_label.config(text=current_time)
    date_label.config(text=current_date.capitalize())
    root.after(1000, update_time)  # Met à jour l'heure toutes les secondes



def imprimer_excel():
    # Récupérer les données affichées dans le tableau
    items = table_present.get_children()
    data = [table_present.item(item, "values") for item in items]

    if not data:
        messagebox.showwarning("Avertissement", "Aucune donnée à imprimer.")
        return

    # Création d'un DataFrame à partir des données
    columns = ["Matricule", "Nom", "Prenom", "Service", "Mention", "Statut","Heure d'arrivee", "Date de présence","Heure de fin"]
    df = pd.DataFrame(data, columns=columns)

    # Exporter vers un fichier Excel
    #file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    file_name = f"Presents_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    try:
        #df.to_excel(file_path, index=False)
        df.to_excel(file_name, index=False)
        messagebox.showinfo("Succès", f"Les données ont été exportées avec succès dans le fichier {file_name}.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'exportation : {e}")


# Fonction appelée par le bouton Quitter
def quitter():
    root.destroy()

def retour():
    root.destroy()
    import Absent

# Création de l'interface Tkinter
root = tk.Tk()
root.title("Gestion des Présences")
root.geometry("1920x1080+0+0")
#root.config(bg="lightgray")

# Titre de l'application
title = tk.Label(root, text="GESTION DE PRESENCE DES AGENTS", font=("Comic Sans MS", 20, "bold"), bg="#9a82fa", fg="black", anchor="w")
title.pack(pady=10)

# En-tête avec la date et l'heure
header_frame = tk.Frame(root)
header_frame.place(x=1030, y=60)

# Label pour afficher la date
date_label = tk.Label(header_frame, font=("Comic Sans MS", 15, "bold"), fg="black")
date_label.pack(side=tk.TOP)

# Label pour afficher l'heure
time_label = tk.Label(header_frame, font=("Comic Sans MS", 17, "bold"), fg="black")
time_label.pack(side=tk.TOP)

# Démarrer la mise à jour de la date et de l'heure
update_time()

#***********Les fonctions du bouton afficher_presents
def on_enter(event):
    btn_afficher_presents.config(bg='white', fg='black')

def on_leave(event):
    btn_afficher_presents.config(bg='#9a82fa', fg='black')

# Boutons pour affichage des présents
btn_afficher_presents = tk.Button(root, text="Afficher Présents", command=afficher_presents,font=("Comic Sans MS", 10),cursor="hand2",bd=2, relief=GROOVE,bg="#9a82fa", fg="black")
btn_afficher_presents.pack(pady=5)

#Evenement de changer la couleur du bouton afficher_presents
btn_afficher_presents.bind("<Enter>", on_enter)
btn_afficher_presents.bind("<Leave>", on_leave)


# Frame de recherche pour les présents
frame_recherche_presents = tk.Frame(root)
frame_recherche_presents.pack(pady=10)
title = Label(root, text="Rechercher par ",font=("Comic Sans MS", 10), anchor="w").place(x=325, y=118)

# Combobox pour choisir le critère de recherche des présents
combobox_critere_present = ttk.Combobox(frame_recherche_presents, values=["matricule"], state="readonly",font=("Comic Sans MS", 10))
combobox_critere_present.grid(row=0, column=0, padx=5)
combobox_critere_present.set("matricule")



# Entrée pour la valeur de recherche des présents
entry_valeur_present = tk.Entry(frame_recherche_presents)
entry_valeur_present.grid(row=0, column=1, padx=5)


#***********Les fonctions du bouton Rechercher
def on_enter(event):
    btn_rechercher_presents.config(bg='white', fg='black')

def on_leave(event):
    btn_rechercher_presents.config(bg='#9a82fa', fg='black')
 
# Bouton de recherche des présents
btn_rechercher_presents = tk.Button(frame_recherche_presents, text="Rechercher", command=rechercher_presents,font=("Comic Sans MS", 10),cursor="hand2",bd=2, relief=GROOVE, bg="#9a82fa", fg="black")
btn_rechercher_presents.grid(row=0, column=2, padx=5)

#Evenement de changer la couleur du bouton Rechercher
btn_rechercher_presents.bind("<Enter>", on_enter)
btn_rechercher_presents.bind("<Leave>", on_leave)


#******************************Cadre d'affichage des agents**********

# Table pour afficher les présents
table_present = ttk.Treeview(root, columns=("matricule", "nom", "prenom", "service", "mention", "statut","heurearrivee", "datepresence", "heurefin"), show="headings")
table_present.heading("matricule", text="Matricule")
table_present.heading("nom", text="Nom")
table_present.heading("prenom", text="Prenom")
table_present.heading("service", text="Service")
table_present.heading("mention", text="Mention")
table_present.heading("statut", text="Statut")
table_present.heading("heurearrivee", text="Heure d'Arrivée")
table_present.heading("datepresence", text="Date de Présence")
table_present.heading("heurefin", text="Heure de depart")
table_present.place(x=1, y=150, width=1269, height=335)

# Scrollbars pour la table des présents
scroll_x_present = ttk.Scrollbar(table_present, orient="horizontal", command=table_present.xview)
scroll_x_present.pack(side="bottom", fill="x")
table_present.configure(xscrollcommand=scroll_x_present.set)

scroll_y_present = ttk.Scrollbar(table_present, orient="vertical", command=table_present.yview)
scroll_y_present.pack(side="right", fill="y")
table_present.configure(yscrollcommand=scroll_y_present.set)

#***************Tableau des boutons
title = Label(root, text="Rechercher par : ", font=("Comic Sans MS", 15),bg="white", fg="black", anchor="w").place(x=5, y=490)

frame_filtre_presents = Frame(root, bd=3, relief=RIDGE, bg="lightgray")
frame_filtre_presents.place(x=5, y=520, width=1258, height=87)

#*************Définir l'année sélectionnée
def selectionner_annee():
    def definir_annee():
        annee_selectionnee = spin_annee.get()
        afficher_presents_par_annee(annee_selectionnee)
        fenetre_annee.destroy()

    fenetre_annee = tk.Toplevel(root)
    frame_annee = tk.Frame(fenetre_annee)
    frame_annee.pack(pady=10)

    spin_annee = tk.Spinbox(frame_annee, from_=2000, to=2100, width=4)
    spin_annee.pack(side="left", padx=5)
    spin_annee.delete(0, "end")
    spin_annee.insert(0, datetime.now().year)

    btn_definir_annee = tk.Button(fenetre_annee, text="OK", command=definir_annee)
    btn_definir_annee.pack()

# Bouton pour filtrer par année
#btn_annee = tk.Button(frame_filtre_presents, text="Année", command=selectionner_annee, font=("Comic Sans MS", 10),cursor="hand2",bd=2, relief=GROOVE, bg="white")
#btn_annee.grid(row=0, column=3, padx=5)

#Evenement de changer la couleur du bouton Annee
#btn_annee.bind("<Enter>", on_enter)
#btn_annee.bind("<Leave>", on_leave)

#***********Les fonctions du bouton date
def on_enter(event):
    btn_date_present.config(bg='white', fg='black')

def on_leave(event):
    btn_date_present.config(bg='#9a82fa', fg='black')

btn_date_present = tk.Button(frame_filtre_presents, text="Date", command=lambda: select_date(afficher_presents_par_date),font=("Comic Sans MS", 10), cursor="hand2",bd=4, relief=GROOVE, bg="#9a82fa", fg="black") 
btn_date_present.place(x=90, y=17, width=130, height=50)

#Evenement de changer la couleur du bouton date
btn_date_present.bind("<Enter>", on_enter)
btn_date_present.bind("<Leave>", on_leave)


#***********Les fonctions du bouton semaine
def on_enter(event):
    btn_semaine_present.config(bg='white', fg='black')

def on_leave(event):
    btn_semaine_present.config(bg='#9a82fa', fg='black')

#bouton semaine
btn_semaine_present = tk.Button(frame_filtre_presents, text="Semaine", command=lambda: select_week(afficher_presents_par_semaine),font=("Comic Sans MS", 10), cursor="hand2",bd=4, relief=GROOVE, fg="black",bg="#9a82fa")
btn_semaine_present.place(x=325, y=17,width=130, height=50)

#Evenement de changer la couleur du bouton semaine
btn_semaine_present.bind("<Enter>", on_enter)
btn_semaine_present.bind("<Leave>", on_leave)

#***********Les fonctions du bouton de la courbe
#def on_enter(event):
    #btn_courbe_present.config(bg='white', fg='black')

#def on_leave(event):
    #btn_courbe_present.config(bg='black', fg='white')

#*******************Bouton Courbe
#btn_courbe_present = tk.Button(frame_filtre_presents, text="Courbe", command=courbe_presents,cursor="hand2",font=("Comic Sans MS", 10),bd=4, relief=GROOVE, fg="white",bg="midnight blue")
#btn_courbe_present.place(x=530, y=17, width=130, height=50)

#*******************Evenement de changer la couleur du bouton courbe
#btn_courbe_present.bind("<Enter>", on_enter)
#btn_courbe_present.bind("<Leave>", on_leave)


#***********Les fonctions du bouton supprimer
#def on_enter(event):
 #   btn_supprimer_present.config(bg='white', fg='red')

#def on_leave(event):
 #   btn_supprimer_present.config(bg='midnight blue', fg='white')

#**********Bouton supprimer
#btn_supprimer_present = tk.Button(frame_filtre_presents, text="Supprimer",command=supprimer_agents,cursor="hand2",font=("Comic Sans MS", 10),bd=4, relief=GROOVE, fg="white",bg="midnight blue")
#btn_supprimer_present.place(x=670, y=17, width=130, height=50)

#*********************Evenement de changer la couleur du bouton supprimer
#btn_supprimer_present.bind("<Enter>", on_enter)
#btn_supprimer_present.bind("<Leave>", on_leave)

#*************Bouton pour imprimer en Excel
btn_imprimer = tk.Button(frame_filtre_presents, text="Exporté Excel", command=imprimer_excel, font=("Comic Sans MS", 10), cursor="hand2", bd=2, relief=GROOVE,fg="black",bg="#9a82fa")
btn_imprimer.place(x=560, y=17, width=130, height=50)

 #Ajouter des événements pour changer les couleurs au survol
def on_enter_imprimer(event):
    btn_imprimer.config(bg='white', fg='black')

def on_leave_imprimer(event):
    btn_imprimer.config(bg='#9a82fa', fg='black')

btn_imprimer.bind("<Enter>", on_enter_imprimer)
btn_imprimer.bind("<Leave>", on_leave_imprimer)


#***********Les fonctions du bouton Absent
def on_enter(event):
    btn_retour_present.config(bg='white', fg='black')

def on_leave(event):
    btn_retour_present.config(bg='#9a82fa', fg='black')

btn_retour_present = tk.Button(frame_filtre_presents, text="Absent(s)",command=retour ,cursor="hand2",font=("Comic Sans MS", 10),bd=4, relief=GROOVE, fg="black",bg="#9a82fa")
btn_retour_present.place(x=800, y=17, width=130, height=50)

#evenement de changer la couleur du bouton Absent
btn_retour_present.bind("<Enter>", on_enter)
btn_retour_present.bind("<Leave>", on_leave)


#***********Les fonctions du bouton quitter
def on_enter(event):
    btn_quitter_present.config(bg='red', fg='white')

def on_leave(event):
    btn_quitter_present.config(bg='#9a82fa', fg='black')

#Bouton quitter
btn_quitter_present = tk.Button(frame_filtre_presents, text="Quitter",command=quitter, cursor="hand2", font=("Comic Sans MS", 10), bd=4, relief=tk.GROOVE,fg="black",bg="#9a82fa")
btn_quitter_present.place(x=1025, y=17, width=130, height=50)

#evenement de changer la couleur du bouton quitter
btn_quitter_present.bind("<Enter>", on_enter)
btn_quitter_present.bind("<Leave>", on_leave)

#*******************************************


# Fonctions de sélection de date, semaine, mois et année pour les présents et absents
def select_date(callback):
    top = tk.Toplevel(root)
    cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack()

    def get_date():
        date = cal.get_date()
        callback(date)
        top.destroy()

    btn_get_date = tk.Button(top, text="OK", command=get_date)
    btn_get_date.pack()

def select_week(callback):
    top = tk.Toplevel(root)
    tk.Label(top, text="Sélectionner Date de Début").pack()
    cal_start = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd')
    cal_start.pack()

    tk.Label(top, text="Sélectionner Date de Fin").pack()
    cal_end = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd')
    cal_end.pack()

    def get_week():
        start_date = cal_start.get_date()
        end_date = cal_end.get_date()
        callback(start_date, end_date)
        top.destroy()

    btn_get_week = tk.Button(top, text="OK", command=get_week)
    btn_get_week.pack()

def select_month_year(callback):
    top = tk.Toplevel(root)
    tk.Label(top, text="Sélectionner Mois et Année").pack()
    cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm')

    # Customisation du widget Calendar pour sélectionner le mois et l'année
    cal._top_cal.configure(background='white', foreground='black', font=('Arial', 12))
    cal.pack()

    def get_month_year():
        year_month = cal.get_date()[:7]  # yyyy-mm
        callback(year_month)
        top.destroy()

    btn_get_month_year = tk.Button(top, text="OK", command=get_month_year)
    btn_get_month_year.pack()

def select_year(callback):
    top = tk.Toplevel(root)
    tk.Label(top, text="Sélectionner Année").pack()
    cal_year = Calendar(top, selectmode='day', date_pattern='yyyy')

    # Customisation du widget Calendar pour sélectionner l'année
    cal_year._top_cal.configure(background='white', foreground='black', font=('Arial', 12))
    cal_year.pack()

    def get_year():
        year = cal_year.get_date().split('-')[0]
        callback(year)
        top.destroy()

    btn_get_year = tk.Button(top, text="OK", command=get_year)
    btn_get_year.pack()

def courbe_presents():
    
    
    pass



root.mainloop()
