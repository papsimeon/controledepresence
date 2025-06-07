from tkinter import*
from tkinter import ttk, messagebox
import tkinter as tk
from tkcalendar import *
from pymysql import cursors
from tkinter import Tk, Frame, Label, PhotoImage
import os
import mysql.connector
from PIL import Image, ImageTk  # Importation de Image et ImageTk depuis PIL

class loginAg:
    def __init__(self, root):
        self.root = root
        self.root.title("Authentification Users")
        #self.root.geometry("1500x780+230+250")
        self.root.geometry("1920x1080+0+0")
        self.root.config(bg="lightgray")
        self.root.focus_force()

        title = Label(self.root, text="CONTROLE DE PRESENCE DES AGENTS", font=("Comic Sans MS", 25, "bold"),bg="white", fg="black", anchor="w").place(x=310, y=30)

        login_frame = Frame(self.root, bg="lightgray",bd=10,relief=GROOVE)
        login_frame.place(x=430, y=120, width=430, height=510)

        title = Label(login_frame, text="Ceci est reservé aux Users\nVerification", font=("Comic Sans MS", 20, "bold"), bg="lightgray", fg="midnight blue")
        title.place(x=20,y=10)
        # login
        lbl_login = Label(login_frame, text="Login", font=("Comic Sans MS", 23, "bold"), bg="lightgray", fg="black").place(x=170,y=120)

        # Champ de saisie du login
        self.txt_login=Entry(login_frame, font=("Comic Sans MS", 18), bg="white")
        self.txt_login.place(x=48, y=170, width=320)

        lbl_password = Label(login_frame, text="Password", font=("Comic Sans MS", 20, "bold"), bg="lightgray", fg="black").place(x=100,y=220, width=200)

        #Champ de saisie du mot de passe
        self.txt_password = Entry(login_frame, show="*", font=("Comic Sans MS", 18), bg="white")
        self.txt_password.place(x=48, y=270, width=320)


        #***********Les fonctions du bouton connexion
        def on_enter(event):
            btn_connexion.config(bg='green', fg='white')

        def on_leave(event):
            btn_connexion.config(bg='white', fg='green')

        # Boutons connexion
        btn_connexion = tk.Button(login_frame, text="Connexion", command=self.connexion,font=("Comic Sans MS", 13),cursor="hand2",bd=4, relief=GROOVE, bg="white",fg='green')
        btn_connexion.place(x=150, y=340,width=120, height=50)

        #Evenement de changer la couleur du bouton connexion
        btn_connexion.bind("<Enter>", on_enter)
        btn_connexion.bind("<Leave>", on_leave)


        #***********Les fonctions du bouton retour
        def on_enter(event):
            btn_retour.config(bg='midnight blue', fg='white')

        def on_leave(event):
            btn_retour.config(bg='white', fg='black')

            #Bouton retour
        btn_retour = Button(login_frame, text="Marquer présence",command=self.retour, cursor="hand2", font=("Comic Sans MS", 11), bd=4, relief=GROOVE,fg="black",bg="white")
        btn_retour.place(x=80, y=420, width=135)

        #evenement de changer la couleur du bouton retour
        btn_retour.bind("<Enter>", on_enter)
        btn_retour.bind("<Leave>", on_leave)

        #***********Les fonctions du bouton quitter
        def on_enter(event):
            btn_quitter.config(bg='red', fg='white')

        def on_leave(event):
            btn_quitter.config(bg='white', fg='red')

            #Bouton quitter
        btn_quitter = Button(login_frame, text="Quitter",command=self.quitter, cursor="hand2", font=("Comic Sans MS", 11), bd=4, relief=GROOVE,fg="red",bg="white")
        btn_quitter.place(x=245, y=420, width=135)

        #evenement de changer la couleur du bouton quitter
        btn_quitter.bind("<Enter>", on_enter)
        btn_quitter.bind("<Leave>", on_leave)
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
                    #messagebox.showinfo("Success", "Bienvenu")
                    self.root.destroy()
                    import Accueilqrcode
                    con.close()

            #Les cas d'exception pour identifier l'erreur
            except Exception as ex:
                messagebox.showerror("Erreur", f"Erreur de connexion: {str(ex)}", parent=self.root)

        #Fonction reinitialiser
    def rein(self):
        self.ecri_question.current(0)
        self.ecri_reponse.delete(0, END)
        self.ecri_nouveaupass.delete(0, END)

    def quitter(self):
        self.root.destroy()

    def retour(self):
        self.root.destroy()
        import Agpresent

root=Tk()
obj = loginAg(root)
root.mainloop()