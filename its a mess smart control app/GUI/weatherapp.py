import json
import urllib.request
import tkinter as tk
from tkinter import ttk


def fahrenheit(temp_celcius):
    return 32 + (1.8 * temp_celcius)


def gevoelstemperatuur(temp_celcius, windsnelheid, luchtvochtigheid):
    return temp_celcius - (luchtvochtigheid / 100) * windsnelheid


def weerrapport(temp_celcius, windsnelheid, luchtvochtigheid):
    gevoel_temp = gevoelstemperatuur(temp_celcius, windsnelheid, luchtvochtigheid)

    if gevoel_temp < 0 and windsnelheid > 10:
        return "Het is heel koud en het stormt! Verwarming helemaal aan!"
    elif gevoel_temp < 0 and windsnelheid <= 10:
        return "Het is behoorlijk koud! Verwarming aan op de benedenverdieping!"
    elif 0 <= gevoel_temp < 10 and windsnelheid > 12:
        return "Het is best koud en het waait; verwarming aan en roosters dicht!"
    elif 0 <= gevoel_temp < 10 and windsnelheid <= 12:
        return "Het is een beetje koud, elektrische kachel aan!"
    elif 10 <= gevoel_temp < 22:
        return "Heerlijk weer, niet te koud of te warm."
    else:
        return "Warm! Airco aan!"


locaties = {
    "Amsterdam": {"lat": 52.37, "lon": 4.89},
    "Den Haag": {"lat": 52.07, "lon": 4.31},
    "Utrecht": {"lat": 52.09, "lon": 5.12},
    "Arnhem": {"lat": 51.98, "lon": 5.91},
    "'s-Hertogenbosch": {"lat": 51.69, "lon": 5.30},
    "Zwolle": {"lat": 52.51, "lon": 6.09},
    "Leeuwarden": {"lat": 53.20, "lon": 5.79},
    "Groningen": {"lat": 53.21, "lon": 6.56},
    "Assen": {"lat": 52.99, "lon": 6.56},
    "Lelystad": {"lat": 52.51, "lon": 5.47},
    "Middelburg": {"lat": 51.50, "lon": 3.61},
    "Maastricht": {"lat": 50.85, "lon": 5.69}
}


def maak_weer_scherm(content_frame):
    tk.Label(content_frame, text="Kies een provinciehoofdstad:", fg="white", bg="#000000",
             font=("Arial", 12, "bold")).pack(anchor="w", padx=50, pady=5)

    gekozen_stad_var = tk.StringVar(value="Utrecht")

    # 2. Koppel de StringVar aan de Combobox via 'textvariable'
    stad_keuze = ttk.Combobox(content_frame, textvariable=gekozen_stad_var, values=list(locaties.keys()),
                              font=("Arial", 11), state="readonly", width=25)
    stad_keuze.pack(anchor="w", padx=50, pady=5)

    lbl_temp = tk.Label(content_frame, text="Temperatuur laden...", fg="gray", bg="#000000", font=("Arial", 11))
    lbl_temp.pack(anchor="w", padx=50, pady=2)

    lbl_wind = tk.Label(content_frame, text="Windsnelheid laden...", fg="gray", bg="#000000", font=("Arial", 11))
    lbl_wind.pack(anchor="w", padx=50, pady=2)

    lbl_advies = tk.Label(content_frame, text="", fg="cyan", bg="#000000", font=("Arial", 11, "italic"))
    lbl_advies.pack(anchor="w", padx=50, pady=10)

    def laad_weer_data(*args):
        gekozen_stad = gekozen_stad_var.get()
        if not gekozen_stad or gekozen_stad not in locaties:
            return

        lat = locaties[gekozen_stad]["lat"]
        lon = locaties[gekozen_stad]["lon"]

        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m,relative_humidity_2m"

            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                current = data["current"]

                temp = current["temperature_2m"]
                wind = current["wind_speed_10m"]
                vocht = current["relative_humidity_2m"]
                temp_f = fahrenheit(temp)

                rapport = weerrapport(temp, wind, vocht)

                lbl_temp.config(text=f"Weer in {gekozen_stad} — Temperatuur: {temp:.1f} °C ({temp_f:.1f} °F)",
                                fg="white")
                lbl_wind.config(text=f"Windsnelheid: {wind:.1f} m/s | Luchtvochtigheid: {vocht}%", fg="white")
                lbl_advies.config(text=f"Advies: {rapport}")
        except Exception as e:
            lbl_temp.config(text=f"Fout bij ophalen weergegevens: {e}", fg="red")

    gekozen_stad_var.trace_add("write", laad_weer_data)

    laad_btn = tk.Button(content_frame, text="Weer verversen", command=laad_weer_data, bg="#333333", fg="white",
                         font=("Arial", 10))
    laad_btn.pack(anchor="w", padx=50, pady=10)

    laad_weer_data()