import re
from tkinter import *
import tkinter as tk
import qrcode
import mysql.connector
import os
from tkinter import ttk, messagebox
from tkcalendar import *

class Agent:
    def __init__(self, root):
        self.root = root
        self.root.title("Enregistrement des agents")
        self.root.geometry("1920x1080+0+0")
        self.root.config(bg="lightgray")
        self.root.focus_force()

# Connexion à la base de données MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="bchcontrole"
)
cursor = conn.cursor()

# Créer la table si elle n'existe pas
cursor.execute("""
    CREATE TABLE IF NOT EXISTS qragent (
        matricule VARCHAR(20) PRIMARY KEY,
        nom VARCHAR(50),
        prenom VARCHAR(50),
        service VARCHAR(50),
        mention VARCHAR(100)
    )
""")


def generer_qr_and_save():
    matricule = matricule_entry.get()
    nom = nom_entry.get()
    prenom = prenom_entry.get()
    service = service_label.get()
    mention = mention_label.get()

    if all([matricule, nom, prenom, service, mention]):
        if not valider_nom_prenom(nom, prenom):
            return

        if not valider_matricule(matricule):
            return

        # Vérifier si le matricule existe déjà
        cursor.execute("SELECT * FROM qragent WHERE matricule = %s", (matricule,))
        if cursor.fetchone() is not None:
            messagebox.showerror("Erreur", "Ce matricule est déjà utilisé")
            return

        # Enregistrement des données dans la base de données
        insert_query = "INSERT INTO qragent (matricule, nom, prenom, service, mention) VALUES (%s, %s, %s, %s, %s)"
        data = (matricule, nom, prenom, service, mention)
        
        cursor.execute(insert_query, data)
        conn.commit()
        reinitialiser_champs()

        # Générer le code QR avec les informations de l'agent
        contenu_qr = matricule, nom, prenom, service, mention
        #contenu_qr = f"Matricule: {matricule}\nNom: {nom}\nPrénom: {prenom}\nService: {service}\nMention: {mention}"
        qr = qrcode.make(contenu_qr)
        messagebox.showinfo("Succès", "Enregistrement effectué et le code QR a été généré avec succès.")
        qr.save(f"./CodeQR/{matricule}_{nom}_{prenom}_code_qr.png")
        update_image(f"./CodeQR/{matricule}_{nom}_{prenom}_code_qr.png")
        
        # Afficher les informations dans le tableau
        table_result.insert('', 'end', values=(matricule, nom, prenom, service, mention))
    else:
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")

def valider_nom_prenom(nom, prenom):
    def valider_chaine(chaine, champ):
        # Vérifier si la chaîne commence ou se termine par un espace ou un tiret
        if chaine.startswith((' ', '-')) or chaine.endswith((' ', '-')):
            messagebox.showerror("Erreur", f"Le champ '{champ}' ne doit pas commencer ou se terminer par un espace ou un tiret.")
            return False
        # Vérifier les espaces ou tirets successifs
        if re.search(r'[\s-]{2,}', chaine):
            messagebox.showerror("Erreur", f"Le champ '{champ}' ne doit pas contenir plus de deux espaces ou tirets successifs.")
            return False
        # Vérifier les espaces suivis de tirets ou tirets suivis d'espaces
        if re.search(r'[\s-]-|-[\s-]', chaine):
            messagebox.showerror("Erreur", f"Le champ '{champ}' ne doit pas contenir un espace suivi d'un tiret ou un tiret suivi d'un espace.")
            return False
        # Vérifier si la chaîne contient des caractères non alphabétiques
        if not re.match(r"^[A-Za-z\s-]+$", chaine):
            messagebox.showerror("Erreur", f"Le champ '{champ}' ne doit contenir que des lettres alphabétiques, des espaces ou des tirets.")
            return False
        return True
    
    return valider_chaine(nom, 'Nom') and valider_chaine(prenom, 'Prénom')

def valider_matricule(matricule):
    if not matricule.isdigit():
        messagebox.showerror("Erreur", "Le matricule ne doit contenir que des chiffres.")
        return False
    return True

def update_image(image_path):
    global qr_image
    qr_image = tk.PhotoImage(file=image_path)
    image_label.config(image=qr_image)

def afficher_agents():
    cursor.execute("SELECT * FROM qragent")
    result = cursor.fetchall()
    clear_table()
    for row_index, row in enumerate(result):
        table_result.insert("", tk.END, values=row)

def clear_table():
    table_result.delete(*table_result.get_children())

def reinitialiser_champs():
    matricule_entry.delete(0, END)
    nom_entry.delete(0, END)
    prenom_entry.delete(0, END)
    service_label.set("Direction Générale")
    mention_label.set("Agent Bch")

def gerer_modification():
    selected_item = table_result.selection()
    if not selected_item:
        messagebox.showwarning("Avertissement", "Veuillez sélectionner un agent à modifier.")
        return

    agent_details = table_result.item(selected_item, 'values')
    matricule_entry.delete(0, END)
    matricule_entry.insert(0, agent_details[0])

    nom_entry.delete(0, END)
    nom_entry.insert(0, agent_details[1])

    prenom_entry.delete(0, END)
    prenom_entry.insert(0, agent_details[2])

    service_label.set(agent_details[3])
    mention_label.set(agent_details[4])

    generer_btn.config(command=lambda: sauvegarder_modification(selected_item))

def sauvegarder_modification(selected_item):
    matricule = matricule_entry.get()
    nom = nom_entry.get()
    prenom = prenom_entry.get()
    service = service_label.get()
    mention = mention_label.get()

    if all([matricule, nom, prenom, service, mention]):
        if not valider_nom_prenom(nom, prenom):
            return

        # Modification dans la base de donnée
        update_query = """
            UPDATE qragent
            SET nom = %s, prenom = %s, service = %s, mention = %s
            WHERE matricule = %s
        """
        data = (nom, prenom, service, mention, matricule)
        cursor.execute(update_query, data)
        conn.commit()

        # Modification de la table
        table_result.item(selected_item, values=(matricule, nom, prenom, service, mention))

        # Generer et sauvegarde du nouveau qr code, overwriting the old one
        contenu_qr = f"Matricule: {matricule}\nNom: {nom}\nPrénom: {prenom}\nService: {service}\nMention: {mention}"
        qr = qrcode.make(contenu_qr)
        global nouveau_code_qr_agent

        nouveau_code_qr_agent = f"./CodeQR/{matricule}_{nom}_{prenom}_code_qr.png"
        qr.save(nouveau_code_qr_agent)

        # Modification de l'image QR code
        update_image(nouveau_code_qr_agent)

        messagebox.showinfo("Succès", "Les informations de l'agent ont été mises à jour avec succès.")

        # Reset the command of the button to the original one
        generer_btn.config(command=generer_qr_and_save)

        # reinitialiser les champs
        reinitialiser_champs()
    else:
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")

def quitter():
    root.destroy()

def retour():    
    root.destroy()
    import Agpresent


def supprimer_agent():
    selected_item = table_result.selection()
    if not selected_item:
        messagebox.showwarning("Avertissement", "Veuillez sélectionner un agent à supprimer.")
        return

    confirmation = messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer cet agent ?")
    if confirmation:
        try:
            matricule = table_result.item(selected_item, 'values')[0]
            delete_query = "DELETE FROM qragent WHERE matricule = %s"
            cursor.execute(delete_query, (matricule,))
            conn.commit()

            if cursor.rowcount > 0:
                table_result.delete(selected_item)
                messagebox.showinfo("Succès", "L'agent a été supprimé avec succès.")
            else:
                messagebox.showwarning("Avertissement", "Aucun enregistrement supprimé de la base de données.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression de l'agent : {e}")

def search_agents():
    search_value = search_entry.get().strip().lower()
    search_field = search_entry.get()
    
    if not search_value:
        messagebox.showwarning("Attention", "Veuillez entrer une valeur de recherche.")
        return
    
    search_query = search_entry.get()

    cursor.execute("SELECT * FROM qragent WHERE nom LIKE %s", (f"%{search_query}%",))
    result = cursor.fetchall()
    clear_table()
    for row_index, row in enumerate(result):
        table_result.insert("", tk.END, values=row)

root = tk.Tk()
root.title("Enregistrement et Génération de Qr code pour les agents")
root.geometry("1920x1080+0+0")

#Title
title = Label(text="GESTION DES AGENTS", font=("Comic Sans MS", 20, "bold"), bg="white", fg="blue", anchor="w").place(x=450, y=5)

#cadre d'enregistrement des agents et du Qr code 
Gestion_Frame = Frame(root, bd=3, relief=GROOVE, bg="lightgray")
Gestion_Frame.place(x=10, y=72, width=610, height=570)

gestion_title = Label(Gestion_Frame, text="INFORMATION DE L'AGENT", font=("Comic Sans MS", 18, "bold"), bg="lightgray", fg="blue")
gestion_title.place(x=20, y=2)

matricule_label = tk.Label(Gestion_Frame, text="Matricule", font=("Comic Sans MS", 20, 'bold'), bg="lightgray", fg="black")
matricule_label.place(x=5, y=50)
matricule_entry = tk.Entry(Gestion_Frame, font=("Comic Sans MS", 15), bg="white", fg="black", bd=2)
matricule_entry.place(x=5, y=95, width=230, height=30)

nom_label = tk.Label(Gestion_Frame, text="Nom", font=("Comic Sans MS", 20, 'bold'), bg="lightgray", fg="black")
nom_label.place(x=5, y=125)
nom_entry = tk.Entry(Gestion_Frame, font=("Comic Sans MS", 15), bg="white", fg="black", bd=2)
nom_entry.place(x=5, y=165, width=230, height=30)

prenom_label = tk.Label(Gestion_Frame, text="Prénom", font=("Comic Sans MS", 20, 'bold'), bg="lightgray", fg="black")
prenom_label.place(x=5, y=205)
prenom_entry = tk.Entry(Gestion_Frame, font=("Comic Sans MS", 15), bg="white", fg="black", bd=2)
prenom_entry.place(x=5, y=245, width=230, height=30)

service_label = tk.Label(Gestion_Frame, text="Dir/dep/ser", font=("Comic Sans MS", 20, 'bold'), bg="lightgray", fg="black")
service_label.place(x=310, y=50)
service_label = ttk.Combobox(Gestion_Frame, font=("Comic Sans MS", 15), state="readonly")
service_label["values"] = ("Dir Generale","RH","Juridique","Logistique","Audit interne",
                           "Admin Systeme","Securite des SI","Dev Logiciel","Com et Marketing")
service_label.place(x=300, y=95, width=230, height=30)
service_label.current(0)

mention_label = tk.Label(Gestion_Frame, text="Mention", font=("Comic Sans MS", 20, 'bold'), bg="lightgray", fg="black")
mention_label.place(x=310, y=125)
mention_label = ttk.Combobox(Gestion_Frame, font=("Comic Sans MS", 15), state="readonly")
mention_label["values"] = ("Agent Akieni", "Prestateur","Stagiaire")
mention_label.place(x=300, y=165, width=230, height=30)
mention_label.current(0)

#Les boutons

#***********Les fonctions du bouton Enregistrer et generer qr code
def on_enter(event):
    generer_btn.config(bg='green', fg='white')

def on_leave(event):
    generer_btn.config(bg='white', fg='green')

# Boutons Enregistrer et generer qr code
generer_btn = tk.Button(Gestion_Frame, text="Enrg et Générer qr", command=generer_qr_and_save,font=("Comic Sans MS", 14),cursor="hand2",bd=4, relief=GROOVE, bg="white",fg='green')
generer_btn.place(x=10, y=300,width=180, height=40)

#Evenement de changer la couleur du bouton Enregistrer et generer qr code
generer_btn.bind("<Enter>", on_enter)
generer_btn.bind("<Leave>", on_leave)


#***********Les fonctions du bouton modifier
def on_enter(event):
    modifier_btn.config(bg='blue', fg='white')

def on_leave(event):
    modifier_btn.config(bg='white', fg='blue')

#Bouton modifier
modifier_btn = tk.Button(Gestion_Frame, text="Modifier",command=gerer_modification ,cursor="hand2",font=("Comic Sans MS", 14),bd=4, relief=GROOVE,bg="white",fg="blue")
modifier_btn.place(x=10, y=350, width=180, height=40)

#evenement de changer la couleur du bouton modifier
modifier_btn.bind("<Enter>", on_enter)
modifier_btn.bind("<Leave>", on_leave)



#***********Les fonctions du bouton supprimer
def on_enter(event):
    supprimer_btn.config(bg='blue', fg='red')

def on_leave(event):
    supprimer_btn.config(bg='white', fg='blue')

#Bouton supprimer
supprimer_btn = tk.Button(Gestion_Frame, text="Supprimer",command=supprimer_agent,cursor="hand2",font=("Comic Sans MS", 14),bd=4, relief=GROOVE, bg="white",fg="blue")
supprimer_btn.place(x=10, y=400, width=180, height=40)

#Evenement de changer la couleur du bouton supprimer
supprimer_btn.bind("<Enter>", on_enter)
supprimer_btn.bind("<Leave>", on_leave)


#***********Les fonctions du bouton retour
def on_enter(event):
    retour_btn.config(bg='blue', fg='white')

def on_leave(event):
    retour_btn.config(bg='white', fg='blue')

retour_btn = tk.Button(Gestion_Frame, text="Marquer Présence",command=retour ,cursor="hand2",font=("Comic Sans MS", 14),bd=4, relief=GROOVE,bg="white",fg="blue")
retour_btn.place(x=10, y=450, width=180, height=40)

#evenement de changer la couleur du bouton Marquer presence
retour_btn.bind("<Enter>", on_enter)
retour_btn.bind("<Leave>", on_leave)


#***********Les fonctions du bouton quitter
def on_enter(event):
    quitter_btn.config(bg='red', fg='white')

def on_leave(event):
    quitter_btn.config(bg='white', fg='red')

#Bouton quitter
quitter_btn = tk.Button(Gestion_Frame, text="Quitter",command=quitter, cursor="hand2", font=("Comic Sans MS", 14), bd=4, relief=tk.GROOVE, fg="red",bg="white")
quitter_btn.place(x=10, y=500, width=180, height=40)

#evenement de changer la couleur du bouton quitter
quitter_btn.bind("<Enter>", on_enter)
quitter_btn.bind("<Leave>", on_leave)


#Cadre du Qr code
image_frame = Frame(root, bd=3, relief=GROOVE, bg="white")
image_frame.place(x=270, y=350, width=310, height=280)

image_label = Label(image_frame, text="Pas de QR Code\n disponible", font=("Comic Sans MS", 20), bg="white", fg="black", width=250, height=250)
image_label.pack(expand=True)

#Cadre de la recherche
search_frame = Frame(root, bd=4, relief=RIDGE, bg="lightgray")
search_frame.place(x=625, y=72, width=638, height=60)

search_label = Label(search_frame, text="Rech par Nom:", font=("Comic Sans MS", 15), bg="lightgray", fg="blue")
search_label.place(x=3, y=10)

search_entry = Entry(search_frame, font=("Comic Sans MS", 15), width=15, bd=5, relief=GROOVE)
search_entry.place(x=150, y=10,width=150, height=40)


#***********Les fonctions du bouton recherche
def on_enter(event):
    search_button.config(bg='blue', fg='white')

def on_leave(event):
    search_button.config(bg='white', fg='blue')

# Bouton recherche
search_button = tk.Button(search_frame, text="Rechercher",command=search_agents ,cursor="hand2",font=("Comic Sans MS", 14),bd=5, relief=GROOVE,bg="white", fg="blue")
search_button.place(x=310, y=10, width=150, height=40)

#evenement de changer la couleur du bouton recherche
search_button.bind("<Enter>", on_enter)
search_button.bind("<Leave>", on_leave)

#***********Les fonctions du bouton Afficher
def on_enter(event):
    afficher_btn.config(bg='blue', fg='white')

def on_leave(event):
    afficher_btn.config(bg='white', fg='blue')

# Bouton Afficher
afficher_btn = tk.Button(search_frame, text="Afficher",command=afficher_agents ,cursor="hand2",font=("Comic Sans MS", 14),bd=5, relief=GROOVE,bg="white",fg="blue")
afficher_btn.place(x=470, y=10, width=150, height=40)

#evenement de changer la couleur du bouton Afficher
afficher_btn.bind("<Enter>", on_enter)
afficher_btn.bind("<Leave>", on_leave)



#***********************Cadre d'affichage des agents**************
table_frame = Frame(root, bd=4, relief=RIDGE, bg="lightgray")
table_frame.place(x=625, y=130, width=638, height=510)

scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
scroll_y = Scrollbar(table_frame, orient=VERTICAL)
table_result = ttk.Treeview(table_frame, columns=("matricule", "nom", "prenom", "service", "mention"),
                            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
scroll_x.pack(side=BOTTOM, fill=X)
scroll_y.pack(side=RIGHT, fill=Y)
scroll_x.config(command=table_result.xview)
scroll_y.config(command=table_result.yview)

table_result.heading("matricule", text="Matricule")
table_result.heading("nom", text="Nom")
table_result.heading("prenom", text="Prénom")
table_result.heading("service", text="Service")
table_result.heading("mention", text="Mention")
table_result['show'] = 'headings'
table_result.column("matricule", width=100)
table_result.column("nom", width=150)
table_result.column("prenom", width=150)
table_result.column("service", width=100)
table_result.column("mention", width=100)
table_result.pack(fill=BOTH, expand=1)

afficher_agents()
root.mainloop()