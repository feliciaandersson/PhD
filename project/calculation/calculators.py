# coding=utf-8

from ase.calculators.dftb import Dftb
from ase.calculators.gaussian import Gaussian, GaussianOptimizer
import os
from ase.optimize import LBFGS
from ase.io.trajectory import Trajectory
from ase.io import read


def DFTB_calculator(atoms, label, calc_type, specification):

    calc = Dftb(
        atoms=atoms,
        Driver_="GeometryOptimization",
        Driver_Optimiser="Rational {}",
        Hamiltonian_="xTB",
        Hamiltonian_Method=f"{specification}-xTB",
        # Hamiltonian_MaxSCCIterations=500,
        # Hamiltonian_SCCTolerance=1e-5,
        label=label,
    )

    atoms.calc = calc
    atoms.get_potential_energy()

    return atoms


def Gaussian_calculator(atoms, label, calc_type, specification):

    # Check if Gaussian executable is provided as an environment variable
    gaussian_executable = os.environ.get("ASE_GAUSSIAN_COMMAND")

    if not gaussian_executable:
        gaussian_executable = "g16"

    calc = Gaussian(
        label=label,
        mem="12GB",
        nprocshared="12",
        xc="B3LYP",
        basis=specification,
        empiricaldispersion="GD3",
        scf="maxcycle=200",
        chk=label + ".chk",
        pop="chelpg",
        command=f"{gaussian_executable} < PREFIX.com > PREFIX.log",
    )

    atoms.calc = calc

    if calc_type.lower() == "opt":
        opt = GaussianOptimizer(atoms)
        opt.run(steps=500)

    elif calc_type.lower() == "sp":
        atoms.get_potential_energy()

    return atoms
