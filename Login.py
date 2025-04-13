from tkinter import*
from tkinter import ttk, messagebox
import tkinter as tk
from tkcalendar import *
from pymysql import cursors
from tkinter import Tk, Frame, Label
import os
import sys
import mysql.connector
from PIL import Image, ImageTk

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        #self.root.geometry("1500x780+230+250")
        self.root.geometry("1920x1080+0+0")
        self.root.config(bg="lightgray")
        self.root.focus_force()

        title = Label(self.root, text="CONTROLE DE PRESENCE DES AGENTS", font=("Comic Sans MS", 25, "bold"),bg="white", fg="blue", anchor="w").place(x=300, y=30)

        login_frame = Frame(self.root, bg="lightgray",bd=3,relief=GROOVE)
        login_frame.place(x=460, y=130, width=370, height=500)


        # Charger l'image depuis le chemin spécifié
        #image d'authentification
        #image_path = "assets/bccok.jpg"
        image_path = resource_path('assets/bccok.jpg')
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)

        image = image.resize((250, 300), Image.Resampling.LANCZOS) 
        photo = ImageTk.PhotoImage(image)

        # Créer un widget Label pour afficher l'image au milieu
        label_image = Label(image=photo, bg="lightgray")
        label_image.bch = photo
        label_image.place(relx=0.2, rely=0.6, anchor="center")

        title = Label(login_frame, text="Authentification", font=("Comic Sans MS", 25, "bold"), bg="lightgray", fg="blue")
        title.pack(side=TOP, fill=X)

        #login
        lbl_login = Label(login_frame, text="Login", font=("Comic Sans MS", 25, "bold"), bg="lightgray",fg="black").place(x=145, y=80)

        # Champ de saisie de login
        self.txt_login = Entry(login_frame, font=("Comic Sans MS", 20), bg="white")
        self.txt_login.place(x=55, y=130, width=260,height=35)

        #Mot de passe
        lbl_password = Label(login_frame, text="Password", font=("Comic Sans MS", 25, "bold"), bg="lightgray",fg="black").place(x=95, y=200, width=200)

        # Champ de saisie du mot de passe
        self.txt_password = Entry(login_frame, show="*", font=("Comic Sans MS", 20), bg="white")
        self.txt_password.place(x=55, y=250, width=260,height=35)

        
        #***********Les fonctions du bouton connexion
        def on_enter(event):
            btn_connexion.config(bg='green', fg='white')

        def on_leave(event):
            btn_connexion.config(bg='white', fg='green')

        # Boutons connexion
        btn_connexion = tk.Button(login_frame, text="Connexion", command=self.connexion,font=("Comic Sans MS", 13),cursor="hand2",bd=4, relief=GROOVE, bg="white",fg='green')
        btn_connexion.place(x=130, y=340,width=120, height=50)

        #Evenement de changer la couleur du bouton connexion
        btn_connexion.bind("<Enter>", on_enter)
        btn_connexion.bind("<Leave>", on_leave)


        #***********Les fonctions du bouton quitter
        def on_enter(event):
            btn_quitter.config(bg='red', fg='white')

        def on_leave(event):
            btn_quitter.config(bg='white', fg='red')

            #Bouton quitter
        btn_quitter = Button(login_frame, text="Quitter",command=self.quitter, cursor="hand2", font=("Comic Sans MS", 13), bd=4, relief=GROOVE,fg="red",bg="white")
        btn_quitter.place(x=130, y=430, width=120, height=50)

        #evenement de changer la couleur du bouton quitter
        btn_quitter.bind("<Enter>", on_enter)
        btn_quitter.bind("<Leave>", on_leave)

        # image akieni
        #image_path = resource_path('assets/bchz.jpg')
        image_path = resource_path('assets/akieni.png')
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)

        image = image.resize((230, 280), Image.Resampling.LANCZOS) 
        photo = ImageTk.PhotoImage(image)

        # Créer un widget Label pour afficher l'image au milieu
        label_image = Label(image=photo, bg="lightgray")
        label_image.bch = photo
        label_image.place(relx=0.8, rely=0.6, anchor="center")


        # Utilisation de resource_path pour accéder à l'image
    image_path = resource_path('assets/bccok.jpg')
    image = Image.open(image_path)

    print("Chemin de l'image : ", image_path)  # Ajoutez ceci pour déboguer

    def connexion(self):
        # Les champs obligatoires
        if self.txt_login.get() == "" or self.txt_password.get() == "" :
            messagebox.showerror("Erreur", "Veuillez remplir les deux champs", parent=self.root)
        else:
            try:
                con = mysql.connector.connect(host="localhost", user="root", password="", database="bchcontrole")
                cur = con.cursor()
                cur.execute("select * from compteusers where login=%s and password=%s",(self.txt_login.get(), self.txt_password.get()))
                row = cur.fetchone()

                if row == None:
                    messagebox.showerror("Erreur", "Invalide ! Verifie le login et le mot de passe", parent=self.root)
                else:

                    self.root.destroy()
                    import Menu
                    con.close()

            #Les cas d'exception pour identifier l'erreur
            except Exception as ex:
                messagebox.showerror("Erreur", f"Erreur de connexion: {str(ex)}", parent=self.root)

     #Fonction reinitialiser
    def rein(self):
        self.ecri_question.current(0)
        self.ecri_reponse.delete(0, END)
        self.ecri_nouveaupass.delete(0, END)

    #Fonction de l'appel de la fenetre menu
    def fenetre_compte(self):
        self.root.destroy()
        import Menu

    def quitter(self):
        self.root.destroy()

root=Tk()
obj = Login(root)
root.mainloop()