# coding=utf-8

import os
import logging
import time

import hydra
from omegaconf import DictConfig, OmegaConf

import calculators
from ase.db import connect
from ase.io import read


def setup_logging():
    """Setup logging configurations."""
    log_format = "[%(asctime)s] {%(pathname)s:%(lineno)d} %(message)s  "
    logging.basicConfig(
        filename="logfile.log",
        level=logging.INFO,
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def setup_start_time(label):
    """Setup start time for logging.

    Args:
    - label (str): Label for the job.
    """
    start_time = time.strftime("%H:%M:%S", time.localtime())
    start = time.time()
    logging.info("-" * 80)
    logging.info(f"Starting a new job with label {label} at {start_time}")

    return start

def set_up_database(db_path):
    
    if db_path:
        structures_db = connect(db_path)
        logging.info(f"Database read: {structures_db}")
    else:
        raise ValueError("Input and output database path must be provided.")
    
    return structures_db

def setup_end_time(start, label):
    """
    Setup end time for logging.

    Args:
    - start (float): Start time.
    - label (str): Label for the job.
    """
    end_time = time.strftime("%H:%M:%S", time.localtime())
    end = time.time()
    logging.info(f"Ending job with label {label} at {end_time}.")
    logging.info(f"Job with label {label} took {end-start}.")

    return end_time


def create_folder(calculation_label):
    """
    Create output folder for calculation.

    Args:
    - calculation_label (str): Label for the calculation.
    """

    try:
        logging.info(f"\t\tMakes output folders: {calculation_label}")
        output_folder = os.path.join("./outputs/", calculation_label)
        os.makedirs(output_folder, exist_ok=True)
        os.chdir(output_folder)

    except Exception as e:
        logging.error(
            f"\t\tError in making output folder for {calculation_label}: {str(e)}"
        )


def run_calc(calculator, atoms, label, calc_type, functional, basis_set, parametrization, kpts):
    """
    Run the calculation using the specified calculator.

    Args:
    - calculator (str): Name of the calculator.
    - atoms: Atoms object retrieved from a database.
    - label (str): Label of the structure.
    - calc_type (str): Calculation type, opt or sp.
    - specification (str): Parametrisation or basis set.

    Returns:
    - opt_atoms: Optimized atoms object.
    """

    logging.info(f"\t\tPerforming an {calc_type} calculation in {calculator}")

    try:
        if calculator.lower() == "dftb":
            opt_atoms = calculators.DFTB_calculator(
                atoms, label, calc_type, parametrization, kpts,
            )
        elif calculator.lower() == "gaussian":
            opt_atoms = calculators.Gaussian_calculator(
                atoms, label, calc_type, functional, basis_set
            )
        elif calculator.lower() == "vasp":
            opt_atoms = calculators.VASP_calculator(
                atoms, label, calc_type, functional
            )
            
    except Exception as e:
        logging.error(f"\t\tError in run_calc for {calculator} calculation: {str(e)}")
        return None

    return opt_atoms


def optimize_atoms(input_db, opt_db, calculator, calc_type, label, functional, basis_set, parametrization, kpts):
    """
    Optimize structures and save them to a new database.

    Args:
    - input_db: Input database with input structure atoms objects.
    - opt_db: Database with optimized structure atoms objects.
    - calculator (str): Calculator name.
    - calc_type (str): Calculation type, sp (=single-point) or opt (=optimization).
    - label (str): Label for the new structures.
    - specification (str): Parametrisation or basis set.
    """

    for row in input_db.select():
        name = getattr(row, "name", "")
        calculation_label = f"{name}_{label}"
        logging.info("-" * 40)
        logging.info(f"Calculating {calculation_label}")

        create_folder(calculation_label)

        # Performs geometry optimisation:
        atoms = row.toatoms()
        opt_atoms = run_calc(calculator, 
                             atoms, 
                             calculation_label, 
                             calc_type, 
                             functional, 
                             basis_set, 
                             parametrization,
                             kpts,
                             )

        os.chdir(os.path.join("..", ".."))

        if opt_atoms is not None:
            logging.info(f"\t\tOptimized {calculation_label}!")
        else:
            logging.error(
                f"\t\tError in optimize_atoms for {calculation_label}: atoms is None."
            )

        # Saves the optimized structure and data to a database.
        # Checks if the foreign key is available, otherwise assigns a new one
        try:
            foreign_key = row.get("foreignkey", row.id)
            opt_db.write(
                opt_atoms,
                foreignkey=foreign_key,
                name = calculation_label,
                functional = functional, 
                basis_set = basis_set, 
                parametrization = parametrization,
                calc_type=calc_type,
            )
            logging.info(
                f"Wrote optimized structure to database {opt_db} with "
                f"foreignkey {foreign_key}"
            )

        except Exception as e:
            logging.error(
                f"\t\tError in writing to the database for "
                f"{calculation_label}: {str(e)}"
            )


@hydra.main(version_base=None, config_path="../config/", config_name="config.yaml")
def main(cfg: DictConfig) -> None:

    job = cfg.job
    databases = cfg.databases
    calculator = job.calculator
    functional = job.functional
    basis_set = job.basis_set
    kpts = job.kpts
    parametrization = job.parametrization
    calc_type = job.calc_type
    label = job.label
    input_db_path = databases.input_db_path
    opt_db_path = databases.opt_db_path
    
    setup_logging()
    input_db = set_up_database(input_db_path)
    opt_db = set_up_database(opt_db_path)

    start = setup_start_time(label)
    
    optimize_atoms(
        input_db=input_db,
        opt_db=opt_db,
        calculator=calculator,
        calc_type=calc_type,
        label=label,
        functional = functional,
        basis_set = basis_set,
        parametrization = parametrization,
        kpts = kpts,
    )

    end_time = setup_end_time(start, label)
    print(f"Ending job with label {label} at {end_time}")


if __name__ == "__main__":
    main()
