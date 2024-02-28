import numpy as np
import matplotlib.pyplot as plt
from ase.db import connect


def save_plot(plot_label, dpi=300):
    plt.savefig(plot_label, dpi=dpi)
    plt.show()


def make_plot(energies, label):
    linewidth = None
    if label == "GFN1":
        color = "dodgerblue"
    elif label == "GFN1 from GFN2":
        color = "deepskyblue"
    elif label == "GFN2":
        color = "darkred"
    elif label == "GFN2 from GFN1":
        color = "red"
    elif label == "B3LYP/aug-cc-PVDZ from GFN2":
        color = "purple"
        linewidth = 0.5
    elif label == "B3LYP/aug-cc-PVDZ from GFN1":
        color = "violet"
        linewidth = 0.5
    else:
        color = None

    plt.plot(
        energies,
        marker="o",
        linestyle="-",
        label=label,
        color=color,
        linewidth=linewidth,
    )
    plt.xlabel("Structure index")
    plt.ylabel("Relative energy (eV)")
    plt.title("Relative energy vs. iteration step")
    plt.grid(True)
    plt.ylim(0, 2)
    plt.legend()


# From GFN1:
db1 = "scan_parallel_x_DFTB_GFN1_sp_alternative2_7_points.db"
db2 = "scan_parallel_x_DFTB_GFN2_sp_alternative2_7_points_from_GFN1.db"
# From GFN2:
db3 = "scan_parallel_x_DFTB_GFN2_sp_alternative2_7_points.db"
db4 = "scan_parallel_x_DFTB_GFN1_sp_alternative2_7_points_from_GFN2.db"
db5 = "scan_parallel_x_gaussian_aug-cc-pvdz_sp_from_GFN2.db"

databases = [db1, db2, db3, db4, db5]

labels = [
    "GFN1",
    "GFN2 from GFN1",
    "GFN2",
    "GFN1 from GFN2",
    "B3LYP/aug-cc-PVDZ from GFN2",
]

all_relative_energies = []

for database in databases:
    db = connect(database)
    energies = []
    min_energy = 0

    for row in db.select():
        energies.append(row.energy)
        if row.energy < min_energy:
            min_energy = row.energy

    relative_energies = [energy - min_energy for energy in energies]
    all_relative_energies.append(relative_energies)


# Plotting all for comparison:
plt.figure()
for i, energies in enumerate(all_relative_energies[:]):
    make_plot(energies, labels[i])
save_plot(plot_label="Methods_comparison_all.png")
