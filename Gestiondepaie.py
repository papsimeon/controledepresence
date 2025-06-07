import tkinter as tk
from tkinter import ttk, messagebox
from fpdf import FPDF
import mysql.connector
from tkinter import messagebox
import mysql.connector
from datetime import datetime

# Fonction pour la connexion à la base de données
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="bchcontrole"
    )


# Configuration de la connexion à la base de données
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="bchcontrole"
)
cursor = conn.cursor()

# Fonction pour calculer la paie
def calculer_paie(matricule, mois):
    try:
        # Récupérer le salaire de base de l'agent
        cursor.execute("SELECT salaire_base FROM qragent WHERE matricule = %s", (matricule,))
        result = cursor.fetchone()
        if not result:
            raise ValueError("Agent non trouvé")
        salaire_base = result[0]

        # Définir les paramètres
        jours_travailles_theoriques = 20
        heures_par_jour = 8
        salaire_journalier = salaire_base / jours_travailles_theoriques

        # Récupérer les jours travaillés
        cursor.execute("""
            SELECT COUNT(DISTINCT datepresence) 
            FROM qragentpresent 
            WHERE matricule = %s AND MONTH(datepresence) = %s
        """, (matricule, mois))
        jours_travailles = cursor.fetchone()[0]  # Consommer le résultat

        # Calculer les absences
        absences = jours_travailles_theoriques - jours_travailles

        # Calculer les heures supplémentaires
        cursor.execute("""
            SELECT SUM(TIMESTAMPDIFF(HOUR, heurearrivee, heurefin) - %s)
            FROM qragentpresent 
            WHERE matricule = %s AND MONTH(datepresence) = %s AND TIMESTAMPDIFF(HOUR, heurearrivee, heurefin) > %s
        """, (heures_par_jour, matricule, mois, heures_par_jour))
        heures_supplementaires = cursor.fetchone()[0] or 0  # Consommer le résultat

        # Calcul du salaire brut
        salaire_brut = (jours_travailles * salaire_journalier) + (heures_supplementaires * (salaire_journalier / heures_par_jour))

        # Déduction pour absences
        deduction_absences = absences * salaire_journalier

        # Calcul du salaire net
        salaire_net = salaire_brut - deduction_absences

        # Insérer les données dans la table paie
        cursor.execute("""
            INSERT INTO paie (matricule, mois, jours_travailles, heures_supplementaires, absences, salaire_brut, salaire_net, date_paiement)
            VALUES (%s, %s, %s, %s, %s, %s, %s, CURDATE())
        """, (matricule, mois, jours_travailles, heures_supplementaires, absences, salaire_brut, salaire_net))
        conn.commit()

        messagebox.showinfo("Succès", "Calcul de paie effectué avec succès")

    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")

    finally:
        cursor.close()
        conn.close()



# Fonction pour générer le bulletin PDF
def generer_bulletin_paie(matricule, mois):
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        # Récupérer les informations de paie
        cursor.execute("""
            SELECT * FROM paie WHERE matricule = %s AND mois = %s
        """, (matricule, mois))
        paie = cursor.fetchone()
        if not paie:
            messagebox.showerror("Erreur", "Aucune donnée de paie trouvée pour cet employé.")
            return

        # Récupérer les informations de l'employé
        cursor.execute("SELECT * FROM qragent WHERE matricule = %s", (matricule,))
        agent = cursor.fetchone()

        # Générer le PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Bulletin de Paie", ln=True, align='C')
        pdf.cell(200, 10, txt=f"Mois : {mois}", ln=True, align='C')

        pdf.ln(10)
        pdf.cell(100, 10, txt=f"Employé : {agent['nom']} {agent['prenom']} - Matricule : {agent['matricule']}", ln=True)
        pdf.cell(100, 10, txt=f"Jours travaillés : {paie['jours_travailles']}", ln=1)
        pdf.cell(100, 10, txt=f"Absences : {paie['absences']}", ln=1)
        pdf.cell(100, 10, txt=f"Salaire brut : {paie['salaire_brut']:.2f} FCFA", ln=1)
        pdf.cell(100, 10, txt=f"Salaire net : {paie['salaire_net']:.2f} FCFA", ln=1)

        # Enregistrer le fichier
        filename = f"Bulletin_{agent['matricule']}_{mois}.pdf"
        pdf.output(filename)
        messagebox.showinfo("Succès", f"Bulletin de paie généré : {filename}")

    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")
    finally:
        db.close()

# Interface graphique
def interface_paie():
    def on_calculer():
        matricule = entry_matricule.get()
        mois = entry_mois.get()
        if matricule and mois:
            calculer_paie(matricule, mois)
        else:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")

    def on_generer():
        matricule = entry_matricule.get()
        mois = entry_mois.get()
        if matricule and mois:
            generer_bulletin_paie(matricule, mois)
        else:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")

    root = tk.Tk()
    root.title("Gestion de Paie")

    # Labels et champs d'entrée
    tk.Label(root, text="Matricule :").grid(row=0, column=0, padx=10, pady=10)
    entry_matricule = tk.Entry(root)
    entry_matricule.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(root, text="Mois (YYYY-MM) :").grid(row=1, column=0, padx=10, pady=10)
    entry_mois = tk.Entry(root)
    entry_mois.grid(row=1, column=1, padx=10, pady=10)

    # Boutons
    btn_calculer = tk.Button(root, text="Calculer la Paie", command=on_calculer)
    btn_calculer.grid(row=2, column=0, padx=10, pady=10)

    btn_generer = tk.Button(root, text="Générer le Bulletin", command=on_generer)
    btn_generer.grid(row=2, column=1, padx=10, pady=10)

    root.mainloop()

# Lancer l'interface
interface_paie()
