from tkinter import *
from tkinter import ttk, messagebox
import tkinter as tk
import mysql.connector

class LoginAdmin:
    def __init__(self, root):
        self.root = root
        self.root.title("Authentification Admin")
        self.root.geometry("1920x1080+0+0")
        self.root.config(bg="lightgray")
        self.root.focus_force()

        title = Label(self.root, text="AUTHENTIFICATION DE L'ADMINISTRATEUR", font=("Comic Sans MS", 20, "bold"), bg="white", fg="blue", anchor="w").place(x=300, y=30)

        login_frame = Frame(self.root, bg="lightgray", bd=10, relief=GROOVE)
        login_frame.place(x=430, y=120, width=430, height=510)

        title = Label(login_frame, text="Ceci est réservé à l'admin\nAutentification", font=("Comic Sans MS", 20, "bold"), bg="lightgray", fg="blue")
        title.place(x=20, y=10)

        lbl_login = Label(login_frame, text="Login", font=("Comic Sans MS", 23, "bold"), bg="lightgray", fg="black").place(x=170, y=120)

        self.txt_login = Entry(login_frame, font=("Comic Sans MS", 20), bg="white")
        self.txt_login.place(x=48, y=170, width=320)

        lbl_password = Label(login_frame, text="Password", font=("Comic Sans MS", 20, "bold"), bg="lightgray", fg="black").place(x=100, y=220, width=200)

        self.txt_password = Entry(login_frame, show="*", font=("Comic Sans MS", 20), bg="white")
        self.txt_password.place(x=48, y=270, width=320)

        # Fonction pour changer la couleur des boutons
        def on_enter(event):
            event.widget.config(bg='green', fg='white')

        def on_leave(event):
            event.widget.config(bg='white', fg='green')

        # Bouton connexion
        btn_connexion = tk.Button(login_frame, text="Connexion", command=self.connexion, font=("Comic Sans MS", 13), cursor="hand2", bd=4, relief=GROOVE, bg="white", fg='green')
        btn_connexion.place(x=150, y=340, width=120, height=50)
        btn_connexion.bind("<Enter>", on_enter)
        btn_connexion.bind("<Leave>", on_leave)

        # Bouton retour
        btn_retour = Button(login_frame, text="Retour", command=self.retour, cursor="hand2", font=("Comic Sans MS", 11), bd=4, relief=GROOVE, fg="black", bg="white")
        btn_retour.place(x=50, y=420, width=140)
        btn_retour.bind("<Enter>", on_enter)
        btn_retour.bind("<Leave>", on_leave)

        # Bouton quitter
        btn_quitter = Button(login_frame, text="Quitter", command=self.quitter, cursor="hand2", font=("Comic Sans MS", 11), bd=4, relief=GROOVE, fg="red", bg="white")
        btn_quitter.place(x=230, y=420, width=140)
        btn_quitter.bind("<Enter>", on_enter)
        btn_quitter.bind("<Leave>", on_leave)

    def connexion(self):
        login = self.txt_login.get()
        password = self.txt_password.get()

        if login == "Akieni" and password == "@Kieni":
            self.root.destroy()
            import Compteuser  # Assurez-vous que ce fichier existe et est correctement importé
        else:
            messagebox.showerror("Erreur", "Ceci est réservé à l'admin", parent=self.root)

    def quitter(self):
        self.root.destroy()

    def retour(self):
        self.root.destroy()
        import Menu  # Assurez-vous que ce fichier existe et est correctement importé

root = Tk()
obj = LoginAdmin(root)
root.mainloop()
