#%% 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#%%
# Load the data
path_dis = r"../results/r_py/Dissociation_corve_results.xlsx"
diss_curve = pd.read_excel(path_dis, header=0, skiprows=[1])
diss_curve['DOC_mg_l'] = diss_curve['DOC (SHM)'] *12.01* 1000

# %%
# Köhler 2014
# 2[Ca2+ ]+2[Mg2+ ]+[Na+ ]+[K+ ]+[H+ ] +[NH4+ ]- 2[SO42+ ]- [Cl- ]- [NO3- ] - [F- ]- [OH- ] - [HCO3- ] -2[CO32- ] - [H A2- ] - 2[HA2- ] - 3[A3- ] = 0
#%%

import numpy as np
import matplotlib.pyplot as plt

# Given values for first dissociation line
pKa1_1 = 3.8
pKa2_1 = 4.7
pKa3_1 = 5.5
SD_1 = 7  # μeq/mg TOC
TOC = 10  # mg/l

Ka1_1 = 10**(-pKa1_1)
Ka2_1 = 10**(-pKa2_1)
Ka3_1 = 10**(-pKa3_1)

# Given values for second dissociation line
pKa1_2 = 3.04
pKa2_2 = 4.51
pKa3_2 = 6.46
SD_2 = 8.6  # μeq/mg TOC

Ka1_2 = 10**(-pKa1_2)
Ka2_2 = 10**(-pKa2_2)
Ka3_2 = 10**(-pKa3_2)

# pH range
pH = np.linspace(2, 10, 500)
H = 10**(-pH)

# Total concentration of acid in mol/L for each dissociation line
Atot_1 = (10**-6)*(TOC * SD_1/3)  # mol/L
Atot_2 = (10**-6)* (TOC * SD_2/3)  # mol/L

# Concentrations of each species for first dissociation line
H3A_1 = Atot_1 / (1 + (Ka1_1 / H) + (Ka1_1 * Ka2_1 / H**2) + (Ka1_1 * Ka2_1 * Ka3_1 / H**3))
H2A_1 = Ka1_1 * H3A_1 / H
HA_1 = Ka2_1 * H2A_1 / H
A_1 = Ka3_1 * HA_1 / H

# Concentrations of each species for second dissociation line
H3A_2 = Atot_2 / (1 + (Ka1_2 / H) + (Ka1_2 * Ka2_2 / H**2) + (Ka1_2 * Ka2_2 * Ka3_2 / H**3))
H2A_2 = Ka1_2 * H3A_2 / H
HA_2 = Ka2_2 * H2A_2 / H
A_2 = Ka3_2 * HA_2 / H

# Calculate total negative charge per mg TOC
charge_1 = 10**6 * (H2A_1 + 2 * HA_1 + 3 * A_1) / TOC # μeq/mg TOC
charge_2 = 10**6 * (H2A_2 + 2 * HA_2 + 3 * A_2) / TOC  # μeq/mg TOC

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(pH, charge_1, label='Köhler 2014', color='teal')
plt.plot(pH, charge_2, label='Köhler Hruska 2014', color='orange')
plt.xlabel('pH')
plt.ylabel('Charge (μeq/mg TOC)')
plt.title('OA-/TOC vs. pH')
plt.grid(True)
plt.xlim(3, 8)
plt.legend()
plt.tight_layout()
plt.show()


# %%
#%% 
#Graph the dissociation curve

plt.figure(figsize=(10, 6))
# For each unique adom_doc, plot Z-(6)(aq) on the y-axis and pH on the x-axis
unique_adom_docs = [1.65, 1.9, 2.2, 2]

for adom_doc in unique_adom_docs:
    subset = diss_curve[diss_curve['adom_doc'] == adom_doc]
    subset = subset.sort_values(by='pH')
    subset['OMCD'] = -1 * subset['Z-(6)(aq)']*1000000 / diss_curve['DOC_mg_l']
    plt.plot(subset['pH'], subset['OMCD'], label=f'adom_doc: {adom_doc}')

plt.xlabel('pH')
plt.ylabel('OA-/TOC (mekv/g of C)')
plt.title('Dissociation Curve VM just DOC')
plt.plot(pH, charge_1, label='Köhler 2014')
plt.plot(pH, charge_2, label='Köhler Hruska 2014')
plt.legend()
plt.xlim(3, 8)
plt.grid(True)


# %%
