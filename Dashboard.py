import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import mysql.connector

# Connexion à la base de données
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="bchcontrole"
)

# Récupération des données pour les graphiques
cursor = db.cursor()

# Répartition des présences par service
cursor.execute("SELECT service, COUNT(*) FROM qragpresent GROUP BY service")
data_presence_service = cursor.fetchall()
services = [row[0] for row in data_presence_service]
presence_counts = [row[1] for row in data_presence_service]

# Répartition des absences par service
cursor.execute("SELECT service, COUNT(*) FROM qragabsent GROUP BY service")
data_absence_service = cursor.fetchall()
services_abs = [row[0] for row in data_absence_service]
absence_counts = [row[1] for row in data_absence_service]

# Répartition des absences par mention
cursor.execute("SELECT mention, COUNT(*) FROM qragabsent GROUP BY mention")
data_absence_mention = cursor.fetchall()
mentions = [row[0] for row in data_absence_mention]
absence_by_mention = [row[1] for row in data_absence_mention]

# Répartition des présences par mention
cursor.execute("SELECT mention, COUNT(*) FROM qragpresent GROUP BY mention")
data_presence_mention = cursor.fetchall()
presence_by_mention = [row[1] for row in data_presence_mention]

# Évolution des heures d'arrivée par mention
cursor.execute("SELECT mention, AVG(TIME_TO_SEC(heurearrivee)) FROM qragpresent GROUP BY mention")
data_hours = cursor.fetchall()
hours_by_mention = [row[1] / 3600 for row in data_hours]  # Conversion en heures

# Fonction générique pour afficher un graphique
def display_pie_chart(values, labels, title, row, column):
    fig = Figure(figsize=(5, 3), dpi=100)
    ax = fig.add_subplot(111)
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.set_title(title)

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().grid(row=row, column=column, padx=10, pady=10)

def display_bar_chart(values, labels, title, row, column, horizontal=False):
    fig = Figure(figsize=(5, 3), dpi=100)
    ax = fig.add_subplot(111)
    if horizontal:
        ax.barh(labels, values, color="blue")
    else:
        ax.bar(labels, values, color="green")
    ax.set_title(title)

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().grid(row=row, column=column, padx=10, pady=10)

def display_line_chart(x, y, title, row, column):
    fig = Figure(figsize=(5, 3), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(x, y, marker='o', linestyle='-', color='orange')
    ax.set_title(title)

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().grid(row=row, column=column, padx=10, pady=10)

# Création de la fenêtre principale
root = tk.Tk()
root.title("Dashboard")
root.geometry("1920x1080+0+0")
root.configure(bg="white")

# Ajout du titre
title = tk.Label(root, text="Dashboard", font=("Comic Sans MS", 20, "bold"), bg="white", fg="black")
title.pack(pady=20)

# Ajout d'un Canvas avec Scrollbars
canvas = tk.Canvas(root, bg="white")
scroll_y = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scroll_x = tk.Scrollbar(root, orient="horizontal", command=canvas.xview)

frame = tk.Frame(canvas, bg="white")

# Configuration des scrollbars
canvas.create_window((0, 0), window=frame, anchor="nw")
canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

scroll_y.pack(side="right", fill="y")
scroll_x.pack(side="bottom", fill="x")
canvas.pack(fill="both", expand=True)

# Mise à jour de la taille du Canvas
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

frame.bind("<Configure>", on_frame_configure)

# Fig 1 : Répartition des Présences par Service
display_pie_chart(presence_counts, services, "Répartition des Présences par Service", 1, 0)

# Fig 2 : Répartition des Absences par Service
display_pie_chart(absence_counts, services_abs, "Répartition des Absences par Service", 1, 1)

# Fig 3 : Répartition des Absences par Mention
display_line_chart(mentions, absence_by_mention, "Répartition des Absences par Mention", 2, 0)

# Fig 4 : Répartition des Présences par Mention
display_bar_chart(presence_by_mention, mentions, "Répartition des Présences par Mention", 2, 1, horizontal=True)

# Fig 5 : Évolution des Heures d'Arrivée par Mention
display_bar_chart(hours_by_mention, mentions, "Évolution des Heures d'Arrivée par Mention", 3, 0)

# Fig 6 : Indicateur de Performance
display_pie_chart([70, 30], ["Atteint", "Restant"], "Indicateur de Performance (70%)", 3, 1)

# Lancement de la fenêtre
root.mainloop()
