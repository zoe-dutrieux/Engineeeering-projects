import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def calcul_vitesse(Uinf, Usup, Pe, Ps, L, h1, h2, mu1, mu2):
    h = h1 + h2  # hauteur totale
    dpdx = (Ps - Pe) * 1e5 / L  # Pa/m
    G = dpdx

    # Calcul de A1 (formule exacte)
    num = Usup - Uinf - G * ((h1 + h2)**2 / (2 * mu2) + h1**2 * (1/(2*mu1) - 1/(2*mu2)))
    den = (mu1 / mu2) * (h1 + h2) + h1 * (1 - mu1 / mu2)
    A1 = num / den
    A2 = (mu1 / mu2) * A1

    # B1 (en bas, y = 0)
    B1 = Uinf - A1 * 0 - (G / (2 * mu1)) * 0**2  # simplifie à B1 = Uinf

    # B2 pour continuité en y = h1
    u1_h1 = (G / (2 * mu1)) * h1**2 + A1 * h1 + B1
    B2 = u1_h1 - (G / (2 * mu2)) * h1**2 - A2 * h1

    # Création des listes y et u
    y_vals = []
    u_vals = []
    N = 200
    for i in range(N):
        y = h * i / (N - 1)
        y_vals.append(y)

        if y <= h1:
            u = (G / (2 * mu1)) * y**2 + A1 * y + B1
        else:
            u = (G / (2 * mu2)) * y**2 + A2 * y + B2

        u_vals.append(u)

    # Pression (linéaire en x)
    x_vals = []
    p_vals = []
    Np = 100
    for i in range(Np):
        x = L * i / (Np - 1)
        P = Pe * 1e5 + G * x  # en Pa
        x_vals.append(x)
        p_vals.append(P / 1e5)  # en bar

    return y_vals, u_vals, x_vals, p_vals


def update_plot(event=None):
    Uinf = sliders['Uinf'].get()
    Usup = sliders['Usup'].get()
    Pe = sliders['Pe'].get()
    Ps = sliders['Ps'].get()
    h1 = sliders['h1'].get()
    h2 = sliders['h2'].get()
    mu1 = sliders['μ1'].get()
    mu2 = sliders['μ2'].get()
    L = sliders['L'].get()

    y, u, x, P = calcul_vitesse(Uinf, Usup, Pe, Ps, L, h1, h2, mu1, mu2)

    ax1.clear()
    ax1.plot(y, u)
    ax1.set_title("Profil de vitesse")
    ax1.set_xlabel("y (m)")
    ax1.set_ylabel("Vitesse (m/s)")
    ax1.invert_yaxis()
    ax1.grid()

    ax2.clear()
    ax2.plot(x, P)
    ax2.set_title("Profil de pression")
    ax2.set_xlabel("x (m)")
    ax2.set_ylabel("Pression (bar)")
    ax2.grid()

    canvas.draw()

# Interface graphique
root = tk.Tk()
root.title("Simulation Écoulement Stratifié entre Plaques")

frame = ttk.Frame(root)
frame.pack(side=tk.LEFT, padx=10, pady=10)

sliders = {}
parametres = [
    ("Uinf", 0, 10, 2),
    ("Usup", 0, 10, 5),
    ("Pe", 0, 5, 2),
    ("Ps", 0, 5, 1),
    ("h1", 0.01, 0.1, 0.03),
    ("h2", 0.01, 0.1, 0.02),
    ("μ1", 0.001, 0.02, 0.01),
    ("μ2", 0.001, 0.02, 0.005),
    ("L", 0.1, 5, 1)
]

for name, vmin, vmax, val in parametres:
    ttk.Label(frame, text=name).pack()
    scale = tk.Scale(frame, from_=vmin, to=vmax, resolution=0.001, orient=tk.HORIZONTAL, command=update_plot)
    scale.set(val)
    scale.pack(fill=tk.X)
    sliders[name] = scale

# Graphiques
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

update_plot()
root.mainloop()
