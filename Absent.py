from tkinter import *
import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import locale

# Définir la langue en français
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="bchcontrole"
    )
def verifier_absences():
    conn = connect_db()
    cursor = conn.cursor()

    start_date = '2024-07-16'
    current_date = datetime.now().date()

    # Vérifier les agents absents dans qragpresent jusqu'à 12h00 depuis le 16 juillet 2024
    query = """
    SELECT qragent.matricule, qragent.nom, qragent.prenom, qragent.service, qragent.mention, dates.date
    FROM qragent
    CROSS JOIN (
        SELECT CURDATE() as date
        UNION ALL
        SELECT DATE_ADD(CURDATE(), INTERVAL 1 DAY) as date
    ) as dates
    WHERE qragent.matricule NOT IN (
        SELECT qragpresent.matricule
        FROM qragpresent
        WHERE qragpresent.datepresence = dates.date
        AND qragpresent.heurearrivee <= '12:00:00'
    )
    AND dates.date BETWEEN %s AND %s
    """

    cursor.execute(query, (start_date, current_date))
    absents = cursor.fetchall()

    for absent in absents:
        matricule, nom, prenom, service, mention, datepresence = absent
        cursor.execute("""
        INSERT INTO qragabsent (matricule, nom, prenom, service, mention, statut, datepresence)
        VALUES (%s, %s, %s, %s, %s, 'Absent', %s)
        ON DUPLICATE KEY UPDATE statut='Absent'
        """, (matricule, nom, prenom, service, mention, datepresence))
    
    conn.commit()
    cursor.close()
    conn.close()

    messagebox.showinfo("Information", "Absences vérifiées et insérées dans qragabsent.")
    afficher_absents()

# Fonction pour supprimer les agents sélectionnés
def supprimer_agents():
    selected_items = table_absent.selection()
    if not selected_items:
        messagebox.showwarning("Avertissement", "Veuillez sélectionner un agent à supprimer.")
        return
    
    confirm = messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer les agents sélectionnés ?")
    if not confirm:
        return

    conn = connect_db()
    cursor = conn.cursor()

    for item in selected_items:
        values = table_absent.item(item, "values")
        matricule = values[0]
        datepresence = values[6]

        query = "DELETE FROM qragabsent WHERE matricule = %s AND datepresence = %s"
        cursor.execute(query, (matricule, datepresence))
        table_absent.delete(item)
    
    conn.commit()
    conn.close()
    messagebox.showinfo("Succès", "Agent(s) supprimé(s) avec succès.")

def afficher_absents():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM qragabsent")
    absents = cursor.fetchall()
    conn.close()

    for row in table_absent.get_children():
        table_absent.delete(row)
    
    for absent in absents:
        table_absent.insert("", "end", values=absent)
def rechercher_absents():
    critere = combobox_critere.get()
    valeur = entry_valeur.get()

    conn = connect_db()
    cursor = conn.cursor()

    query = f"SELECT * FROM qragabsent WHERE {critere} = %s"
    params = (valeur,)

    cursor.execute(query, params)
    absents = cursor.fetchall()
    conn.close()

    for row in table_absent.get_children():
        table_absent.delete(row)
    
    for absent in absents:
        table_absent.insert("", "end", values=absent)


def afficher_absents_par_date(date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM qragabsent WHERE datepresence = %s", (date,))
    absents = cursor.fetchall()
    conn.close()

    for row in table_absent.get_children():
        table_absent.delete(row)
    
    for absent in absents:
        table_absent.insert("", "end", values=absent)

def afficher_absents_par_semaine(start_date, end_date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM qragabsent WHERE datepresence BETWEEN %s AND %s", (start_date, end_date))
    absents = cursor.fetchall()
    conn.close()

    for row in table_absent.get_children():
        table_absent.delete(row)
    
    for absent in absents:
        table_absent.insert("", "end", values=absent)

def afficher_absents_par_mois(year_month):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM qragabsent WHERE DATE_FORMAT(datepresence, '%%Y-%%m') = %s", (year_month,))
    absents = cursor.fetchall()
    conn.close()

    for row in table_absent.get_children():
        table_absent.delete(row)
    
    for absent in absents:
        table_absent.insert("", "end", values=absent)

def afficher_absents_par_annee(year):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM qragabsent WHERE YEAR(datepresence) = %s", (year,))
    absents = cursor.fetchall()
    conn.close()

    for row in table_absent.get_children():
        table_absent.delete(row)
    
    for absent in absents:
        table_absent.insert("", "end", values=absent)

def courbe_absences():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT nom, datepresence FROM qragabsent ORDER BY datepresence")
    absents = cursor.fetchall()
    conn.close()

    noms = [row[0] for row in absents]
    dates = [row[1] for row in absents]

    plt.plot(dates, noms, marker='o')
    plt.xlabel("Date de présence")
    plt.ylabel("Nom")
    plt.title("Courbe des absences des agents")
    plt.show()

def update_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%A %d %B %Y")
    time_label.config(text=current_time)
    date_label.config(text=current_date.capitalize())
    root.after(1000, update_time)  # Met à jour l'heure toutes les secondes


def imprimer_excel():
    # Récupérer les données affichées dans le tableau
    items = table_absent.get_children()
    data = [table_absent.item(item, "values") for item in items]

    if not data:
        messagebox.showwarning("Avertissement", "Aucune donnée à imprimer.")
        return

    # Création d'un DataFrame à partir des données
    columns = ["Matricule", "Nom", "Prenom", "Service", "Mention", "Statut", "Date de présence"]
    df = pd.DataFrame(data, columns=columns)

    # Exporter vers un fichier Excel
    file_name = f"Absents_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    try:
        df.to_excel(file_name, index=False)
        messagebox.showinfo("Succès", f"Les données ont été exportées avec succès dans le fichier {file_name}.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'exportation : {e}")


# Création de l'interface Tkinter
root = tk.Tk()
root.title("Gestion des Absences")
root.geometry("1920x1080+0+0")
#root.config(bg="lightgray")

# Titre de l'application
title = tk.Label(root, text="GESTION D'ABSENCE DES AGENTS", font=("Comic Sans MS", 15, "bold"), bg="#9a82fa", fg="black", anchor="w")
title.pack(pady=10)

# En-tête avec la date et l'heure
header_frame = tk.Frame(root)
header_frame.place(x=990, y=70)


# Label pour afficher la date
date_label = tk.Label(header_frame, font=("Comic Sans MS", 15, "bold"), fg="black")
date_label.pack(side=tk.TOP)

# Label pour afficher l'heure
time_label = tk.Label(header_frame, font=("Comic Sans MS", 17, "bold"), fg="black")
time_label.pack(side=tk.TOP)

# Démarrer la mise à jour de la date et de l'heure
update_time()

#***********Les fonctions du bouton pour la vérification et affichage 
def on_enter(event):
    btn_verifier.config(bg='white', fg='black')

def on_leave(event):
    btn_verifier.config(bg='#9a82fa', fg='black')

# Boutons de vérification et affichage
btn_verifier = tk.Button(root, text="Vérifier Absences", command=verifier_absences,font=("Comic Sans MS", 10),cursor="hand2",bd=2, relief=GROOVE, bg="#9a82fa", fg="black")
btn_verifier.pack(pady=5)


#Evenement de changer la couleur du bouton Afficher Absents
btn_verifier.bind("<Enter>", on_enter)
btn_verifier.bind("<Leave>", on_leave)


#***********Les fonctions du bouton Afficher Absents
def on_enter(event):
    btn_afficher.config(bg='white', fg='black')

def on_leave(event):
    btn_afficher.config(bg='#9a82fa', fg='black')

# Boutons pour Afficher les Absents
btn_afficher = tk.Button(root, text="Afficher Absents", command=afficher_absents,font=("Comic Sans MS", 10),cursor="hand2",bd=2, relief=GROOVE, bg="#9a82fa", fg="black")
btn_afficher.pack(pady=5)

#Evenement de changer la couleur du bouton Afficher Absents
btn_afficher.bind("<Enter>", on_enter)
btn_afficher.bind("<Leave>", on_leave)

# Frame de recherche
frame_recherche = tk.Frame(root)
frame_recherche.pack(pady=10)

title = Label(root, text="Rechercher par ",font=("Comic Sans MS", 11), anchor="w").place(x=320, y=160)

# Combobox pour choisir le critère de recherche
combobox_critere = ttk.Combobox(frame_recherche, values=["matricule", "nom", "service", "mention"], state="readonly",font=("Comic Sans MS", 10))
combobox_critere.grid(row=0, column=0, padx=5)
combobox_critere.set("matricule")

# Entrée pour la valeur de recherche
entry_valeur = tk.Entry(frame_recherche)
entry_valeur.grid(row=0, column=1, padx=5)

#***********Les fonctions du bouton Rechercher
def on_enter(event):
    btn_rechercher.config(bg='white', fg='black')

def on_leave(event):
    btn_rechercher.config(bg='#9a82fa', fg='black')
 
# Bouton de recherche
btn_rechercher = tk.Button(frame_recherche, text="Rechercher", command=rechercher_absents,font=("Comic Sans MS", 10),cursor="hand2",bd=2, relief=GROOVE, bg="#9a82fa", fg="black")
btn_rechercher.grid(row=0, column=2, padx=5)

#Evenement de changer la couleur du bouton Rechercher
btn_rechercher.bind("<Enter>", on_enter)
btn_rechercher.bind("<Leave>", on_leave)


# Table pour afficher les absents
frame_table = tk.Frame(root)
frame_table.place(x=1, y=200, width=1338, height=290)

scroll_x = tk.Scrollbar(frame_table, orient="horizontal")
scroll_y = tk.Scrollbar(frame_table, orient="vertical")

table_absent = ttk.Treeview(frame_table, columns=("Matricule", "Nom", "Prenom", "Service", "Mention", "Statut", "Date de présence"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

scroll_x.pack(side="bottom", fill="x")
scroll_y.pack(side="right", fill="y")

scroll_x.config(command=table_absent.xview)
scroll_y.config(command=table_absent.yview)

table_absent.heading("Matricule", text="Matricule")
table_absent.heading("Nom", text="Nom")
table_absent.heading("Prenom", text="Prenom")
table_absent.heading("Service", text="Service")
table_absent.heading("Mention", text="Mention")
table_absent.heading("Statut", text="Statut")
table_absent.heading("Date de présence", text="Date d'absence")
table_absent.place(x=1, y=150, width=1338, height=285)

table_absent['show'] = 'headings'

table_absent.pack()
#Tableau des boutons
title = Label(root, text="Rechercher par : ", font=("Comic Sans MS", 15),bg="white", fg="black", anchor="w").place(x=5, y=490)

frame_filtre_presents = Frame(root, bd=3, relief=RIDGE, bg="lightgray")
frame_filtre_presents.place(x=5, y=520, width=1258, height=87)

def update_time():
    # Code pour mettre à jour l'heure
    pass

# Appel de la fonction après 1000 ms (1 seconde)
root.after(1000, update_time)
try:
    # Code qui pourrait échouer
    root.after(1000, update_time)
except Exception as e:
    print(f"Une erreur est survenue : {e}")


def quitter():
    root.destroy()

def retour():
    root.destroy()
    import Dashboard

# Sélection de la date
def select_date():
    top = tk.Toplevel(root)
    cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack()

    def get_date():
        date = cal.get_date()
        afficher_absents_par_date(date)
        top.destroy()

    btn_get_date = tk.Button(top, text="OK", command=get_date)
    btn_get_date.pack()


#***********Les fonctions du bouton bouton Date
def on_enter(event):
    btn_date.config(bg='white', fg='black')

def on_leave(event):
    btn_date.config(bg='#9a82fa', fg='black')


btn_date = tk.Button(frame_filtre_presents, text="Date", command=select_date,cursor="hand2",bd=4,font=("Comic Sans MS", 10), relief=GROOVE, fg="black",bg="#9a82fa")
btn_date.place(x=90, y=17, width=130, height=50)

#evenement de changer la couleur du bouton date 
btn_date.bind("<Enter>", on_enter)
btn_date.bind("<Leave>", on_leave)

# Sélection de la semaine
def select_week():
    top = tk.Toplevel(root)
    tk.Label(top, text="Du").pack()
    cal_start = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd')
    cal_start.pack()

    tk.Label(top, text="Au").pack()
    cal_end = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd')
    cal_end.pack()

    def get_week():
        start_date = cal_start.get_date()
        end_date = cal_end.get_date()
        afficher_absents_par_semaine(start_date, end_date)
        top.destroy()

    btn_get_week = tk.Button(top, text="OK", command=get_week,cursor="hand2",bd=4, relief=GROOVE, bg="white")
    btn_get_week.pack()


#***********Les fonctions du bouton bouton semaine
def on_enter(event):
    btn_semaine.config(bg='white', fg='black')

def on_leave(event):
    btn_semaine.config(bg='#9a82fa', fg='black')

#btn_semaine
btn_semaine = tk.Button(frame_filtre_presents, text="Semaine", command=select_week,cursor="hand2",bd=4,font=("Comic Sans MS", 10), relief=GROOVE, fg="black",bg="#9a82fa")
btn_semaine.place(x=325, y=17,width=130, height=50)

#evenement de changer la couleur du bouton btn_semaine 
btn_semaine.bind("<Enter>", on_enter)
btn_semaine.bind("<Leave>", on_leave)

# Sélection du mois et de l'année
def select_month_year():
    top = tk.Toplevel(root)
    tk.Label(top, text="Sélectionner Mois et Année").pack()
    cal_month_year = Calendar(top, selectmode='day', date_pattern='yyyy-mm')
    cal_month_year.pack()

    def get_month_year():
        year_month = cal_month_year.get_date()[:7]  # yyyy-mm
        afficher_absents_par_mois(year_month)
        top.destroy()

    btn_get_month_year = tk.Button(top, text="OK", command=get_month_year)
    btn_get_month_year.pack()



# Sélection de l'année
def select_year():
    top = tk.Toplevel(root)
    tk.Label(top, text="Sélectionner Année").pack()
    cal_year = Calendar(top, selectmode='day', date_pattern='yyyy')
    cal_year.pack()

    def get_year():
        year = cal_year.get_date().split('-')[0]
        afficher_absents_par_annee(year)
        top.destroy()

    btn_get_year = tk.Button(top, text="OK", command=get_year)
    btn_get_year.pack()



#***********Les fonctions du bouton courbe
#def on_enter(event):
    #btn_courbe.config(bg='white', fg='black')

#def on_leave(event):
    #btn_courbe.config(bg='midnight blue', fg='white')

#****************Bouton pour afficher la courbe des absences
#btn_courbe = tk.Button(frame_filtre_presents, text="Courbe Absences", command=courbe_absences,cursor="hand2",font=("Comic Sans MS", 10),bd=4, relief=GROOVE, fg="white",bg="midnight blue")
#btn_courbe.place(x=530, y=17, width=130, height=50)

#************evenement de changer la couleur du bouton courbe 
#btn_courbe.bind("<Enter>", on_enter)
#btn_courbe.bind("<Leave>", on_leave)

#***********Les fonctions du bouton supprimer
#def on_enter(event):
    #btn_supprimer_present.config(bg='white', fg='black')

#def on_leave(event):
    #btn_supprimer_present.config(bg='midnight blue', fg='white')

#btn_supprimer_present = tk.Button(frame_filtre_presents, text="Supprimer",command=supprimer_agents, cursor="hand2",font=("Comic Sans MS", 10),bd=4, relief=GROOVE, fg="white",bg="midnight blue")
#btn_supprimer_present.place(x=670, y=17, width=130, height=50)

#evenement de changer la couleur du bouton supprimer
#btn_supprimer_present.bind("<Enter>", on_enter)
#btn_supprimer_present.bind("<Leave>", on_leave)

#*************Bouton pour imprimer en Excel
btn_imprimer = tk.Button(frame_filtre_presents, text="Exporté Excel", command=imprimer_excel, font=("Comic Sans MS", 10), cursor="hand2", bd=2, relief=GROOVE,fg="black", bg="#9a82fa")
btn_imprimer.place(x=570, y=17, width=130, height=50)

 #Ajouter des événements pour changer les couleurs au survol
def on_enter_imprimer(event):
    btn_imprimer.config(bg='white', fg='black')

def on_leave_imprimer(event):
    btn_imprimer.config(bg='#9a82fa', fg='black')

btn_imprimer.bind("<Enter>", on_enter_imprimer)
btn_imprimer.bind("<Leave>", on_leave_imprimer)


#***********Les fonctions du bouton Dashboard
def on_enter(event):
    btn_retour_present.config(bg='white', fg='black')

def on_leave(event):
    btn_retour_present.config(bg='#9a82fa', fg='black')

btn_retour_present = tk.Button(frame_filtre_presents, text="Dashboard",command=retour,cursor="hand2",font=("Comic Sans MS", 10),bd=4, relief=GROOVE, fg="black",bg="#9a82fa")
btn_retour_present.place(x=800, y=17, width=130, height=50)

#evenement de changer la couleur du bouton Tableau \nde Bord
btn_retour_present.bind("<Enter>", on_enter)
btn_retour_present.bind("<Leave>", on_leave)


#***********Les fonctions du bouton quitter
def on_enter(event):
    btn_quitter_present.config(bg='red', fg='white')

def on_leave(event):
    btn_quitter_present.config(bg='#9a82fa', fg='black')

#Bouton quitter
btn_quitter_present = tk.Button(frame_filtre_presents, text="Quitter",command=quitter,cursor="hand2",font=("Comic Sans MS", 10),bd=4, relief=GROOVE, fg="black",bg="#9a82fa")
btn_quitter_present.place(x=1025, y=17, width=130, height=50)

#evenement de changer la couleur du bouton quitter
btn_quitter_present.bind("<Enter>", on_enter)
btn_quitter_present.bind("<Leave>", on_leave)


root.mainloop()