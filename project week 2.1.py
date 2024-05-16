# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 08:56:17 2024

@author: marie
"""

import numpy as np
import matplotlib.pyplot as plt


# parameters
k = 34  # veerconstante in N/m
m = 1.5682*10**-6  # massa in kilogram
b = 0.03651 # b-waarde


# inlezen van de positiebestanden
def lees_positiebestand(file_path):
    tijden, posities = np.loadtxt(file_path, unpack=True)
    return tijden, posities

# afgeleiden berekenen voor snelheid en versnelling
def bereken_afgeleiden(tijden, waarden):
    afgeleiden = np.gradient(waarden, tijden)
    return afgeleiden

# respons van de resonator berekenen
def bereken_respons(tijden, versnellingen, m, b, k):
    # differentiaalvergelijking oplossen
    # discrete benadering van de respons:
    x = np.zeros_like(versnellingen)
    v = np.zeros_like(versnellingen)
    dt = tijden[1] - tijden[0]
    for i in range(1, len(tijden)):
        a_res = versnellingen[i] - (b/m) * v[i-1] - (k/m) * x[i-1]
        v[i] = v[i-1] + a_res * dt
        x[i] = x[i-1] + v[i] * dt
    return x

# bestanden
pad_positie1 = r"C:\Users\marie\OneDrive\Documenten\TN jaar 1\Blok 4\Project\posities_1_Team_13.txt"
pad_positie2 = r"C:\Users\marie\OneDrive\Documenten\TN jaar 1\Blok 4\Project\posities_2_Team_13.txt"

# posities en tijden inlezen
tijden1, posities1 = lees_positiebestand(pad_positie1)
tijden2, posities2 = lees_positiebestand(pad_positie2)

# snelheden en versnellingen berekenen
snelheden1 = bereken_afgeleiden(tijden1, posities1)
versnellingen1 = bereken_afgeleiden(tijden1, snelheden1)

snelheden2 = bereken_afgeleiden(tijden2, posities2)
versnellingen2 = bereken_afgeleiden(tijden2, snelheden2)

# respons berekenen
respons1 = bereken_respons(tijden1, versnellingen1, m, b, k)
respons2 = bereken_respons(tijden2, versnellingen2, m, b, k)


fig, ax1 = plt.subplots()

color = 'tab:blue'
ax1.set_xlabel('Tijd (s)')
ax1.set_ylabel('Versnelling (m/s^2)', color=color)
ax1.plot(tijden1, versnellingen1, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # Exemplaar maken van een tweede as die dezelfde x-as deelt

color = 'tab:red'
ax2.set_ylabel('Respons',  color=color)
ax2.plot(tijden1, respons1, linestyle='--', color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # Anders wordt het rechter y-label iets bijgesneden
plt.title('dataset 1')
plt.show()


fig, ax3 = plt.subplots()

color = 'tab:blue'
ax3.set_xlabel('Tijd (s)')
ax3.set_ylabel('Versnelling (m/s^2)', color=color)
ax3.plot(tijden2, versnellingen2, color=color)
ax3.tick_params(axis='y', labelcolor=color)

ax4 = ax3.twinx()  # Exemplaar maken van een tweede as die dezelfde x-as deelt
color = 'tab:red'
ax4.set_ylabel('Respons', color=color) 
ax4.plot(tijden2, respons2, linestyle='--', color=color)
ax4.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # Anders wordt het rechter y-label iets bijgesneden
plt.title('dataset 2')
plt.show()

