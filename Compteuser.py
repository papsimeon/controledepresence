import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
import re
import hashlib

class Compteuser:
    def __init__(self, root):
        self.root = root
        self.root.title("Ajouter un User")
        self.root.geometry("1920x1080+0+0")
        self.root.config(bg="lightgray")

        title = Label(self.root, text="GESTION DES UTILISATEURS", font=("Comic Sans MS", 20, "bold"), bg="white", fg="blue", anchor="w").place(x=459, y=20)

        # Champ de formulaire
        frame1 = Frame(self.root, bd=2, relief=GROOVE, bg="lightgray")
        frame1.place(x=300, y=100, width=750, height=528)

        title = Label(frame1, text="Ajouter User", font=("Comic Sans MS", 20, "bold"), bg="white", fg="Black").place(x=50, y=20)

        # Matricule
        aff_matricule = Label(frame1, text="Matricule", font=("Comic Sans MS", 18, "bold"), bg="lightgrey", fg="black").place(x=50, y=100)
        self.ecri_matricule = Entry(frame1, font=("Comic Sans MS", 15), bg="white")
        self.ecri_matricule.place(x=50, y=140, width=250)
        self.ecri_matricule.bind("<FocusOut>", self.remplir_nom_prenom)

        # Nom
        aff_nom = Label(frame1, text="Nom", font=("Comic Sans MS", 18, "bold"), bg="lightgrey", fg="black").place(x=370, y=100)
        self.ecri_nom = Entry(frame1, font=("Comic Sans MS", 15), bg="white")
        self.ecri_nom.place(x=370, y=140, width=250)

        # Prénom
        aff_prenom = Label(frame1, text="Prenom", font=("Comic Sans MS", 18, "bold"), bg="lightgrey", fg="black").place(x=50, y=175)
        self.ecri_prenom = Entry(frame1, font=("Comic Sans MS", 15), bg="white")
        self.ecri_prenom.place(x=50, y=210, width=250)

        # Login
        aff_login = Label(frame1, text="Login", font=("Comic Sans MS", 18, "bold"), bg="lightgrey", fg="black").place(x=370, y=175)
        self.ecri_login = Entry(frame1, font=("Comic Sans MS", 15), bg="white")
        self.ecri_login.place(x=370, y=210, width=250)

        # Password
        aff_password = Label(frame1, text="Password", font=("Comic Sans MS", 18, "bold"), bg="lightgrey", fg="black").place(x=50, y=250)
        self.ecri_password = Entry(frame1, show="*", font=("Comic Sans MS", 15), bg="white")
        self.ecri_password.place(x=50, y=290, width=250)

        # Confirmer le mot de passe
        aff_cfpassword = Label(frame1, text="Confirmer Password", font=("Comic Sans MS", 18, "bold"), bg="lightgrey", fg="black").place(x=370, y=250)
        self.ecri_cfpassword = Entry(frame1, show="*", font=("Comic Sans MS", 15), bg="white")
        self.ecri_cfpassword.place(x=370, y=290, width=250)

        # Accepter les termes et conditions
        self.var_chech = IntVar()
        chk = Checkbutton(frame1, variable=self.var_chech, onvalue=1, offvalue=0, text="J'accepte les conditions et les termes", cursor="hand2", font=("Comic Sans MS", 13), bg="lightgrey").place(x=50, y=350)

        # Bouton ajouter User
        btn_ajouter_user = tk.Button(frame1, text="Ajouter", command=self.creer, cursor="hand2", bd=4, font=("Comic Sans MS", 13), relief=GROOVE, bg="white",fg="blue")
        btn_ajouter_user.place(x=150, y=400, width=150, height=50)
        btn_ajouter_user.bind("<Enter>", lambda e: btn_ajouter_user.config(bg='blue', fg='white'))
        btn_ajouter_user.bind("<Leave>", lambda e: btn_ajouter_user.config(bg='white', fg='blue'))

        # Bouton Afficher User
        btn_afficher_user = tk.Button(frame1, text="Afficher", command=self.afficher_users, cursor="hand2", bd=4, font=("Comic Sans MS", 13), relief=GROOVE, bg="white",fg="blue")
        btn_afficher_user.place(x=415, y=400, width=150, height=50)
        btn_afficher_user.bind("<Enter>", lambda e: btn_afficher_user.config(bg='blue', fg='white'))
        btn_afficher_user.bind("<Leave>", lambda e: btn_afficher_user.config(bg='white', fg='blue'))


        # Bouton ajouter voir user
        #btn_voir_user = tk.Button(frame1, text="Afficher Users", command=self.afficher_users, cursor="hand2", bd=4, font=("Comic Sans MS", 13), relief=GROOVE, fg="midnight blue", bg="white")
        #btn_voir_user.place(x=490, y=400, width=150, height=50)
        #btn_voir_user.bind("<Enter>", lambda e: btn_voir_user.config(bg='midnight blue', fg='white'))
        #btn_voir_user.bind("<Leave>", lambda e: btn_voir_user.config(bg='white', fg='midnight blue'))

        # Bouton user connecter
        #btn_user_connecte = tk.Button(frame1, text="User connecté", command=self.users_connecter, cursor="hand2", bd=4, font=("Comic Sans MS", 13), relief=GROOVE, fg="midnight blue", bg="white")
        #btn_user_connecte.place(x=60, y=400, width=150, height=50)
        #btn_user_connecte.bind("<Enter>", lambda e: btn_user_connecte.config(bg='midnight blue', fg='white'))
        #btn_user_connecte.bind("<Leave>", lambda e: btn_user_connecte.config(bg='white', fg='midnight blue'))


        # Bouton connexion
        btn_connexion = tk.Button(frame1, text="Connexion", command=self.fenetre_login, font=("Comic Sans MS", 13), cursor="hand2", bd=4, relief=GROOVE, bg="white", fg='green')
        btn_connexion.place(x=550, y=20, width=120, height=50)
        btn_connexion.bind("<Enter>", lambda e: btn_connexion.config(bg='green', fg='white'))
        btn_connexion.bind("<Leave>", lambda e: btn_connexion.config(bg='white', fg='green'))

        # Bouton retour
        btn_retour_present = tk.Button(frame1, text="Retour", command=self.retour, cursor="hand2", font=("Comic Sans MS", 13), bd=4, relief=GROOVE, bg="white",fg="blue")
        btn_retour_present.place(x=210, y=467, width=120, height=50)
        btn_retour_present.bind("<Enter>", lambda e: btn_retour_present.config(bg='blue', fg='red'))
        btn_retour_present.bind("<Leave>", lambda e: btn_retour_present.config(bg='white', fg='blue'))

        # Bouton quitter
        btn_quitter = Button(frame1, text="Quitter", command=self.quitter, cursor="hand2", font=("Comic Sans MS", 13), bd=4, relief=GROOVE, fg="red", bg="white")
        btn_quitter.place(x=385, y=467, width=120, height=50)
        btn_quitter.bind("<Enter>", lambda e: btn_quitter.config(bg='red', fg='white'))
        btn_quitter.bind("<Leave>", lambda e: btn_quitter.config(bg='white', fg='red'))

    def valider_nom_prenom(self, nom, prenom):
        pattern = r"^(?!.*[ -]{2})(?!.*[ -]$)(?!^[ -])(?!.*[ -]{2}).*$"
        if not (re.match(r'^[A-Za-z\s-]+$', nom) and re.match(pattern, nom) and re.match(r'^[A-Za-z\s-]+$', prenom) and re.match(pattern, prenom)):
            return False
        return True

    def valider_matricule(self, matricule):
        if not re.match(r'^\d+$', matricule):
            return False
        return True

    def valider_login(self, login):
        if not re.match(r"^[A-Za-z]+$", login):
            return False
        return True

    def valider_password(self, password):
        if len(password) < 8 or not re.search(r'[A-Za-z]', password) or not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'[0-9]', password) or not re.search(r'[!@#$%^&*(),.?":{}|<>]', password) or re.search(r'[éèêùûôîçâ]', password):
            return False
        return True

    def griser_champs(self):
        self.ecri_matricule.config(state='disabled')
        self.ecri_nom.config(state='disabled')
        self.ecri_prenom.config(state='disabled')

    def remplir_nom_prenom(self, event):
        try:
            con = mysql.connector.connect(host="localhost", user="root", password="", database="bchcontrole")
            cur = con.cursor()
            cur.execute("SELECT nom, prenom FROM qragent WHERE matricule=%s", [self.ecri_matricule.get()])
            row = cur.fetchone()
            if row:
                self.ecri_nom.delete(0, END)
                self.ecri_nom.insert(0, row[0])
                self.ecri_prenom.delete(0, END)
                self.ecri_prenom.insert(0, row[1])
                self.griser_champs()
            else:
                messagebox.showerror("Erreur", "Matricule non trouvé", parent=self.root)
            con.close()
        except Exception as es:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération des données : {es}", parent=self.root)

    def hacher_password(self, password):
        # Utilisation de SHA-256 pour le hachage
        return hashlib.sha256(password.encode()).hexdigest()

    def creer(self):
        # Vérification des champs obligatoires
        if (self.ecri_matricule.get() == "" or self.ecri_nom.get() == "" or self.ecri_prenom.get() == "" or
            self.ecri_login.get() == "" or self.ecri_password.get() == "" or self.ecri_cfpassword.get() == ""):
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires", parent=self.root)
            return
        elif not self.valider_matricule(self.ecri_matricule.get()):
            messagebox.showerror("Erreur", "Le matricule ne doit contenir que des chiffres", parent=self.root)
            return
        elif not self.valider_nom_prenom(self.ecri_nom.get(), self.ecri_prenom.get()):
            messagebox.showerror("Erreur", "Le nom et le prénom ne doivent contenir que des lettres, des espaces ou des tirets, et pas de tirets en début ou en fin", parent=self.root)
            return
        elif not self.valider_login(self.ecri_login.get()):
            messagebox.showerror("Erreur", "Le login ne doit contenir que des lettres sans accents", parent=self.root)
            return
        elif not self.valider_password(self.ecri_password.get()):
            messagebox.showerror("Erreur", "Le mot de passe doit contenir au moins 8 caractères, avec des lettres majuscules, des lettres minuscules, des chiffres et des caractères spéciaux autorisés", parent=self.root)
            return
        elif self.ecri_password.get() != self.ecri_cfpassword.get():
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas", parent=self.root)
            return
        elif self.var_chech.get() == 0:
            messagebox.showerror("Erreur", "Veuillez accepter les termes et conditions", parent=self.root)
            return
        
        # Les variables sont maintenant définies après la validation des entrées utilisateur
        matricule = self.ecri_matricule.get()
        nom = self.ecri_nom.get()
        prenom = self.ecri_prenom.get()
        login = self.ecri_login.get()
        password = self.ecri_password.get()
        password_hache = self.hacher_password(password)

        try:
            # Connexion à la base de données
            con = mysql.connector.connect(host="localhost", user="root", password="", database="bchcontrole")
            cur = con.cursor()

            # Vérification de l'existence du matricule dans la table qragent
            cur.execute("SELECT * FROM qragent WHERE matricule=%s", (matricule,))
            row = cur.fetchone()

            if row:
                # Insertion dans la base de données
                cur.execute("INSERT INTO compteusers (matricule, nom, prenom, login, password) VALUES (%s, %s, %s, %s, %s)",
                            (matricule, nom, prenom, login, password_hache))
                con.commit()
                messagebox.showinfo("Succès", "Utilisateur ajouté avec succès", parent=self.root)
                self.vider_champs()
            else:
                messagebox.showerror("Erreur", "Le matricule n'existe pas dans qragent", parent=self.root)
            
            con.close()
        except Exception as es:
            messagebox.showerror("Erreur", f"Erreur de connexion: {str(es)}", parent=self.root)

  
    def vider_champs(self):
        self.ecri_matricule.config(state='normal')
        self.ecri_nom.config(state='normal')
        self.ecri_prenom.config(state='normal')
        self.ecri_matricule.delete(0, END)
        self.ecri_nom.delete(0, END)
        self.ecri_prenom.delete(0, END)
        self.ecri_login.delete(0, END)
        self.ecri_password.delete(0, END)
        self.ecri_cfpassword.delete(0, END)
        self.var_chech.set(0)

    def fenetre_login(self):
        self.root.destroy()
        import Login

    def quitter(self):
        self.root.destroy()

    def users_connecter(self):
        
        import LoginAttemps

    def afficher_users(self):
        
        import AfficherUsers

    def retour(self):
        self.root.destroy()
        import Menu

root = Tk()
obj = Compteuser(root)
root.mainloop()
