# widgets = gui elements buttons textboxes labels images
# windows = serves as a container for widgets

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import tkinter as tk
import weatherapp

window = tk.Tk()
window.geometry("1000x650")
window.title("Studentencheck - Dashboard")
window.config(background="#000000")

try:
    icon = ImageTk.PhotoImage(file="../PNG pictures/schoolsupplies.jpg")
    window.iconphoto(True, icon)
except Exception as e:
    print("Icoon kon niet geladen worden:", e)

window.rowconfigure(0, weight=1)
window.columnconfigure(1, weight=1)

sidebar = tk.Frame(window, bg="#1a1a1a", width=250)
sidebar.pack(side=tk.LEFT, fill=tk.Y)

content_frame = tk.Frame(window, bg="#000000")
content_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)


def toon_app(app_naam):
    for widget in content_frame.winfo_children():
        widget.destroy()

    titel = tk.Label(content_frame, text=app_naam, fg="white", bg="#000000", font=("Arial", 18, "bold"))
    titel.pack(pady=20, anchor="w", padx=50)

    if app_naam == "OV":
        tk.Label(content_frame, text="Actuele reisinformatie en vertrektijden.", fg="gray", bg="#000000",
                 font=("Arial", 12)).pack(anchor="w", padx=50)

    elif app_naam == "Calendar":
        tk.Label(content_frame, text="Je rooster en agenda-afspraken komen hier te staan.", fg="gray", bg="#000000",
                 font=("Arial", 12)).pack(anchor="w", padx=50)

    elif app_naam == "Weatherapp":
        weatherapp.maak_weer_scherm(content_frame)

    elif app_naam == "Timer":
        tk.Label(content_frame, text="Studeer-timer / Pomodoro klok.", fg="gray", bg="#000000",
                 font=("Arial", 12)).pack(anchor="w", padx=50)

    elif app_naam == "Notitieblok":
        tk.Label(content_frame, text="Typ hieronder je notities:", fg="white", bg="#000000", font=("Arial", 11)).pack(
            anchor="w", padx=50)
        notitie_veld = Text(content_frame, bg="#222222", fg="white", insertbackground="white", font=("Arial", 11),
                            width=65, height=18)
        notitie_veld.pack(pady=10, padx=50, anchor="w")

    elif app_naam == "To-do lijst":
        tk.Label(content_frame, text="Voeg een nieuwe taak toe:", fg="white", bg="#000000", font=("Arial", 11)).pack(
            anchor="w", padx=50)

        entry = ttk.Entry(content_frame, font=("Arial", 12), width=35)
        entry.pack(pady=5, padx=50, anchor="w")

        listbox = Listbox(content_frame, bg="#222222", fg="white", font=("Arial", 11), width=45, height=12)
        listbox.pack(pady=5, padx=50, anchor="w")

        def taak_toevoegen(event=None):
            taak = entry.get()
            if taak != "":
                listbox.insert(END, taak)
                entry.delete(0, END)

        def taak_verwijderen():
            try:
                geselecteerd_index = listbox.curselection()
                listbox.delete(geselecteerd_index)
            except:
                pass

        entry.bind("<Return>", taak_toevoegen)

        btn_frame = tk.Frame(content_frame, bg="#000000")
        btn_frame.pack(pady=5, padx=50, anchor="w")

        add_btn = tk.Button(btn_frame, text="Taak toevoegen", command=taak_toevoegen, bg="#333333", fg="white",
                            font=("Arial", 10))
        add_btn.pack(side=tk.LEFT, padx=(0, 10))

        del_btn = tk.Button(btn_frame, text="Verwijder geselecteerde taak", command=taak_verwijderen, bg="#552222",
                            fg="white", font=("Arial", 10))
        del_btn.pack(side=tk.LEFT)


apps_lijst = [
    "OV",
    "Calendar",
    "Weatherapp",
    "Timer",
    "Notitieblok",
    "To-do lijst"
]

for app in apps_lijst:
    knop = tk.Button(
        sidebar,
        text=app,
        command=lambda a=app: toon_app(a),
        bg="#333333",
        fg="white",
        font=("Arial", 11, "bold"),
        relief=FLAT,
        activebackground="#555555",
        activeforeground="white",
        anchor="w",
        padx=20
    )
    knop.pack(pady=8, padx=10, fill=tk.X)

toon_app("OV")

window.mainloop()