# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 08:56:17 2024

@author: marie
"""

import numpy as np
import matplotlib.pyplot as plt


# parameters
k = 34  # veerconstante in N/m
m = 1.5682*10**-3  # massa in kilogram
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

fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(14, 6))

# Eerste subplot
ax1.plot(tijden1, versnellingen1, label='Versnelling')
ax1.set_xlabel('Tijd (s)')
ax1.set_ylabel('Versnelling (m/s^2)')
ax1.set_title('Versnelling van Dataset 1')
ax1.legend()

# Tweede subplot
ax2.plot(tijden1, respons1, label='Respons', linestyle='--', color='red')
ax2.set_xlabel('Tijd (s)')
ax2.set_ylabel('Respons')
ax2.set_title('Respons van Dataset 1')
ax2.legend()

# Derde subplot
ax3.plot(tijden2, versnellingen2, label='Versnelling')
ax3.set_xlabel('Tijd (s)')
ax3.set_ylabel('Versnelling (m/s^2)')
ax3.set_title('Versnelling van Dataset 2')
ax3.legend()

# Vierde subplot
ax4.plot(tijden2, respons2, label='Respons', linestyle='--', color='red')
ax4.set_xlabel('Tijd (s)')
ax4.set_ylabel('Respons')
ax4.set_title('Respons van Dataset 2')
ax4.legend()

plt.tight_layout()
plt.show()

