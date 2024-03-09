# coding=utf-8

import os

from ase.calculators.dftb import Dftb
from ase.calculators.gaussian import Gaussian, GaussianOptimizer
from ase.calculators.vasp import Vasp
from ase.io import read
from ase.io.trajectory import Trajectory
from ase.optimize import LBFGS


def DFTB_calculator(atoms, label, calc_type, parametrization, kpts):
    """
    Run DFTB calculation.

    Args:
        atoms (ase.Atoms): The atomic structure for the calculation.
        label (str): Label for the calculation.
        calc_type (str): Type of calculation, either 'opt' for optimization or 'sp' for single-point.
        specification (str): Parametrization used in the calculation.

    Returns:
        ase.Atoms: The atomic structure with calculation results.
    """

    calc = Dftb(
        atoms=atoms,
        Driver_="GeometryOptimization",
        Driver_Optimiser="Rational {}",
        Hamiltonian_="xTB",
        Driver_LatticeOpt="No",
        kpts=(1, 1, 1),
        Hamiltonian_Method=f"{parametrization}-xTB",
        # Hamiltonian_MaxSCCIterations=500,
        # Hamiltonian_SCCTolerance=1e-5,
        label=label,
    )

    atoms.calc = calc
    atoms.get_potential_energy()

    return atoms


def Gaussian_calculator(atoms, label, calc_type, functional, basis_set):
    """
    Run Gaussian calculation.

    Args:
        atoms (ase.Atoms): The atomic structure for the calculation.
        label (str): Label for the calculation.
        calc_type (str): Type of calculation, either 'opt' for optimization or 'sp' for single-point.
        functional (str): functional used in the calculation.
        basis_set (str): Basis set used in the calculation.

    Returns:
        ase.Atoms: The atomic structure with calculation results.
    """

    # Check if Gaussian executable is provided as an environment variable
    gaussian_executable = os.environ.get("ASE_GAUSSIAN_COMMAND")

    if not gaussian_executable:
        gaussian_executable = "g16"

    calc = Gaussian(
        label=label,
        mem="12GB",
        nprocshared="12",
        xc=functional,
        basis=basis_set,
        empiricaldispersion="GD3",
        scf="maxcycle=200",
        chk=f"{label}.chk",
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


def VASP_calculator(atoms, label, calc_type, functional):
    """
    Run VASP calculation.

    Args:
        atoms (ase.Atoms): The atomic structure for the calculation.
        label (str): Label for the calculation.
        calc_type (str): Type of calculation, either 'opt' for optimization or 'sp' for single-point.
        functional (str): Type of functional for the calculation.
    Returns:
        ase.Atoms: The atomic structure with calculation results.
    """

    nsw = 500 if calc_type.lower() == "opt" else 1

    calc = Vasp(
        atoms=atoms,
        label=label,
        txt="vasp_out",
        command="mpprun vasp_std",
        algo="normal",
        gga="PE",
        prec="ACCURATE",
        istart=1,
        icharg=1,
        ispin=1,
        ivdw=11,
        lorbit=None,
        ediff=0.1e-06,
        ediffg=-0.1e-2,
        nelm=600,
        encut=550.000000,
        sigma=0.05,
        ismear=0,
        nsw=nsw,
        ibrion=2,
        isif=2,
    )

    atoms.calc = calc
    atoms.get_potential_energy()

    return atoms
