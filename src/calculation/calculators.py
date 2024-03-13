# coding=utf-8

import os

from ase.calculators.dftb import Dftb
from ase.calculators.gaussian import Gaussian, GaussianOptimizer
from ase.calculators.vasp import Vasp


def DFTB_calculator(atoms, label, calc_type, parametrization, kpts, lattice_opt):
    """
    Run a DFTB calculation.

    Args:
        atoms (ase.Atoms): The atomic structure for the calculation.
        label (str): Label for the calculation.
        calc_type (str): Type of calculation, either 'opt' for optimization or 'sp' for single-point.
        parametrization (str): Parametrization used in the calculation.
        kpts (tuple): k-points used in the calculation.
        lattice_opt (str): Flag indicating whether lattice optimization is enabled.

    Returns:
        ase.Atoms: The atomic structure with calculation results.
    """

    common_params = {
        "atoms": atoms,
        "kpts": (1, 1, 1),
        "label": label,
        "Hamiltonian_": "xTB",
        "Hamiltonian_Method": f"{parametrization}-xTB",
        # Hamiltonian_MaxSCCIterations=500,
        # Hamiltonian_SCCTolerance=1e-5,
    }

    opt_params = {
        "Driver_": "GeometryOptimization",
        "Driver_Optimiser": "Rational {}",
        "Driver_LatticeOpt": "No",
    }

    if calc_type.lower() == "opt":
        calc_params = {**common_params, **opt_params}
    else:
        calc_params = {**common_params}

    calc = Dftb(**calc_params)
    atoms.calc = calc
    atoms.get_potential_energy()

    return atoms


def Gaussian_calculator(atoms, label, calc_type, functional, basis_set):
    """
    Run a Gaussian calculation.

    Args:
        atoms (ase.Atoms): The atomic structure for the calculation.
        label (str): Label for the calculation.
        calc_type (str): Type of calculation, either 'opt' for optimization or 'sp' for single-point.
        functional (str): Functional used in the calculation.
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


def VASP_calculator(atoms, label, calc_type, functional, kpts, lattice_opt):
    """
    Run a VASP calculation.

    Args:
        atoms (ase.Atoms): The atomic structure for the calculation.
        label (str): Label for the calculation.
        calc_type (str): Type of calculation, either 'opt' for optimization or 'sp' for single-point.
        functional (str): Type of functional for the calculation.
        lattice_opt (str): Flag indicating whether lattice optimization is enabled.

    Returns:
        ase.Atoms: The atomic structure with calculation results.
    """

    nsw = 500 if calc_type.lower() == "opt" else 1
    # gga = "PE" if functional.upper() == "PBE" else ""
    isif = 3 if lattice_opt == "yes" else 2

    calc = Vasp(
        atoms=atoms,
        label=label,
        txt="vasp_out",
        command="mpprun vasp_std",
        algo="normal",
        xc=functional,
        prec="ACCURATE",
        istart=1,
        icharg=1,
        ispin=1,
        ivdw=11,
        kpts=kpts,
        lorbit=None,
        ediff=0.1e-06,
        ediffg=-0.1e-2,
        nelm=600,
        encut=550.000000,
        sigma=0.05,
        ismear=0,
        nsw=nsw,
        ibrion=2,
        isif=isif,
    )

    atoms.calc = calc
    atoms.get_potential_energy()

    return atoms
