# -*- coding: utf-8 -*-
"""
Created on Fri May 17 00:31:04 2024

@author: Marieke Lau
"""

import numpy as np
import matplotlib.pyplot as plt

# parameters
V0 = 1e-6  # aangelegde spanning in Volt
d0 = 1e-6  # beginafstand tussen de platen in meter (1 micron)
k = 34  # veerconstante in N/m
m = 1.5682 * 10**-6  # massa in kilogram
epsilon_0 = 8.854187817e-12  # permittiviteit van de vrije ruimte in F/m
w = 1e-3  # breedte van de platen in meter (1 mm)
l = 1e-3  # lengte van de platen in meter (1 mm)

# berekening van kritische demping
b_krit = 2 * np.sqrt(k * m)
b = b_krit  # gebruik kritische demping voor optimalisatie

# inlezen van de positiebestanden
def lees_positiebestanden(file_path):
    tijden, posities = np.loadtxt(file_path, unpack=True)
    return tijden, posities

# afgeleiden berekenen voor snelheid en versnelling
def bereken_afgeleiden(tijden, waarden):
    afgeleiden = np.gradient(waarden, tijden)
    return afgeleiden

# respons van de resonator berekenen
def bereken_respons(tijden, versnellingen, m, b, k):
    x = np.zeros_like(versnellingen)
    v = np.zeros_like(versnellingen)
    dt = tijden[1] - tijden[0]
    for i in range(1, len(tijden)):
        a_res = versnellingen[i] - (b/m) * v[i-1] - (k/m) * x[i-1]
        v[i] = v[i-1] + a_res * dt
        x[i] = x[i-1] + v[i] * dt
    return x

# spanning berekenen als functie van positie
def bereken_spanning(x, V0, d0):
    return V0 * (1 + x / d0)

# kracht berekenen op basis van positie en spanning
def bereken_kracht(x, V0, d0, epsilon_0, w, l):
    return (1/2) * epsilon_0 * w * (l + x) * (V0**2) / ((d0 - x)**2)

# bestanden
pad_positie1 = r"C:\Users\marie\OneDrive\Documenten\TN jaar 1\Blok 4\Project\posities_1_Team_13.txt"
pad_positie2 = r"C:\Users\marie\OneDrive\Documenten\TN jaar 1\Blok 4\Project\posities_2_Team_13.txt"

# posities en tijden inlezen
tijden1, posities1 = lees_positiebestanden(pad_positie1)
tijden2, posities2 = lees_positiebestanden(pad_positie2)

# snelheden en versnellingen berekenen
snelheden1 = bereken_afgeleiden(tijden1, posities1)
versnellingen1 = bereken_afgeleiden(tijden1, snelheden1)

snelheden2 = bereken_afgeleiden(tijden2, posities2)
versnellingen2 = bereken_afgeleiden(tijden2, snelheden2)

# respons berekenen
respons1 = bereken_respons(tijden1, versnellingen1, m, b, k)
respons2 = bereken_respons(tijden2, versnellingen2, m, b, k)

# spanning berekenen op basis van respons
spanning1 = bereken_spanning(respons1, V0, d0)
spanning2 = bereken_spanning(respons2, V0, d0)

# kracht berekenen op basis van respons
kracht1 = bereken_kracht(respons1, V0, d0, epsilon_0, w, l)
kracht2 = bereken_kracht(respons2, V0, d0, epsilon_0, w, l)


# plotten van de resultaten
# voor het plotten van de spanning vervang je tot en met het einde van het plotten "kracht" voor "spanning"
def plot_versnelling_en_kracht(tijden, versnellingen, kracht, dataset_nummer):
    fig, ax1 = plt.subplots()

    color = 'tab:blue'
    ax1.set_xlabel('Tijd (s)')
    ax1.set_ylabel('Versnelling (m/s^2)', color=color)
    ax1.plot(tijden, versnellingen, color=color, label='Versnelling')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Kracht (N)', color=color)
    ax2.plot(tijden, kracht, linestyle='--', color=color, label='Kracht')
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    plt.title(f'Dataset {dataset_nummer}')
    fig.legend(loc='lower left')
    plt.show()

# plotten van dataset 1
plot_versnelling_en_kracht(tijden1, versnellingen1, kracht1, 1)

# plotten van dataset 2
plot_versnelling_en_kracht(tijden2, versnellingen2, kracht2, 2)


# Methode om de reactietijd te kwantificeren
def kwantificeer_reactietijd(tijden, respons):
    max_pos = np.max(respons)
    min_pos = np.min(respons)
    threshold = 0.9 * (max_pos - min_pos) + min_pos
    reactietijd = tijden[np.where(respons >= threshold)][0]
    return reactietijd

# Originele reactietijd
originele_reactietijd1 = kwantificeer_reactietijd(tijden1, respons1)
originele_reactietijd2 = kwantificeer_reactietijd(tijden2, respons2)

print(f"Originele reactietijd dataset 1: {originele_reactietijd1} s")
print(f"Originele reactietijd dataset 2: {originele_reactietijd2} s")

# Optimalisatie van de reactietijd door k en b te variëren
def optimaliseer_reactietijd(tijden, versnellingen, m, V0, d0, originele_reactietijd, factor):
    beste_k = k
    beste_b = b
    beste_reactietijd = originele_reactietijd
    for k_var in np.linspace(k, 2*k, 100):
        for b_var in np.linspace(b, 2*b, 100):
            respons = bereken_respons(tijden, versnellingen, m, b_var, k_var)
            reactietijd = kwantificeer_reactietijd(tijden, respons)
            if reactietijd < beste_reactietijd and reactietijd <= originele_reactietijd / factor:
                beste_reactietijd = reactietijd
                beste_k = k_var
                beste_b = b_var
    return beste_k, beste_b, beste_reactietijd

factor = 2 # We willen minstens 2 keer zo snel reageren
beste_k1, beste_b1, beste_reactietijd1 = optimaliseer_reactietijd(tijden1, versnellingen1, m, V0, d0, originele_reactietijd1, factor)
beste_k2, beste_b2, beste_reactietijd2 = optimaliseer_reactietijd(tijden2, versnellingen2, m, V0, d0, originele_reactietijd2, factor)

print(f"Beste k en b voor dataset 1: k = {beste_k1}, b = {beste_b1}, reactietijd = {beste_reactietijd1} s")
print(f"Beste k en b voor dataset 2: k = {beste_k2}, b = {beste_b2}, reactietijd = {beste_reactietijd2} s")

# Respons met geoptimaliseerde parameters berekenen
geoptimaliseerde_respons1 = bereken_respons(tijden1, versnellingen1, m, beste_b1, beste_k1)
geoptimaliseerde_respons2 = bereken_respons(tijden2, versnellingen2, m, beste_b2, beste_k2)

# Geoptimaliseerde spanning berekenen op basis van respons
geoptimaliseerde_spanning1 = bereken_spanning(geoptimaliseerde_respons1, V0, d0)
geoptimaliseerde_spanning2 = bereken_spanning(geoptimaliseerde_respons2, V0, d0)

# Plotten van de geoptimaliseerde resultaten
# op dit moment zal de code dus niet werken maar als je de spanning en kracht verwisseld zal hij het uitstekend doen.
plot_versnelling_en_spanning(tijden1, versnellingen1, geoptimaliseerde_spanning1, 'Geoptimaliseerd 1')
plot_versnelling_en_spanning(tijden2, versnellingen2, geoptimaliseerde_spanning2, 'Geoptimaliseerd 2')


# Opdracht 4 tm line 176
# Simulatie instellingen
x_values = np.linspace(-1e-6, 1e-6, 500)  # verplaatsing van -1 micron tot 1 micron

# berekening van de uitgangsspanning
V_out = V0 * (1 + x_values / d0)

# plotten van de resultaten
plt.figure()
plt.plot(x_values, V_out, label='Uitgangsspanning')
plt.xlabel('Verplaatsing van de massa (m)')
plt.ylabel('Uitgangsspanning (V)')
plt.title('Spanning vs. Massa-positie')
plt.legend()
plt.grid(True)
plt.show()