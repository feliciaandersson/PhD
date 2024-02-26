# coding=utf-8

import calculators
from ase.db import connect
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.table import Table
import logging
import time


def setup_start_time(label):
    start_time = time.strftime("%H:%M:%S", time.localtime())
    start = time.time()
    logging.info(f"--------------------------------------------------------------")
    logging.info(f"Starting a new job with label {label} at {start_time}")
    time_limit = read_time_limit()
    logging.info(f"time limit: {time_limit}")

    return start_time, start


def setup_end_time(start, label):
    end_time = time.strftime("%H:%M:%S", time.localtime())
    end = time.time()
    logging.info(f"Ending job with label {label} at {end_time}.")
    logging.info(f"Job with label {label} took {end-start}.")

    return end_time


def setup_logging():
    log_format = "[%(asctime)s] {%(pathname)s:%(lineno)d} %(message)s  "
    logging.basicConfig(
        filename="logfile.log",
        level=logging.INFO,
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def read_time_limit():
    time_limit = os.environ.get("SLURM_TIME_LIMIT")
    if time_limit:
        return time_limit
    else:
        print("SLURM_TIME_LIMIT environment variable not set.")
        return None


def create_folder(calculation_label):

    try:
        logging.info(f"\t\t Makes output folders: {calculation_label}")
        output_folder = os.path.join("./outputs/", calculation_label)
        os.makedirs(output_folder, exist_ok=True)
        os.chdir(output_folder)

    except Exception as e:
        logging.info(
            f"\t\t Error in making output folder in optimize_atoms for {calculation_label}: {str(e)}"
        )


def run_calc(calculator, atoms, label, calc_type, specification):
    """
    Used to run the calculation using the specified calculator and atoms object.
    Returns the optimized atoms object.

    Args:
    - calc: the defined calculator.
    - atom: the atoms object retrieved from a database.
    - label (str): label of the structure.
    - calc_type (str): calculation type, opt or sp.
    - specification (str): parametrisation or basis set.
    """

    logging.info(f"\t\t Performing an {calc_type} calculation in {calculator}")

    try:
        if calculator.lower() == "dftb":
            opt_atoms = calculators.DFTB_calculator(
                atoms, label, calc_type, specification
            )
        elif calculator.lower() == "gaussian":
            opt_atoms = calculators.Gaussian_calculator(
                atoms, label, calc_type, specification
            )

    except Exception as e:
        logging.info(f"\t\t Error in run_calc for {calculator} calculation: {str(e)}")
        return None

    return opt_atoms


def optimize_atoms(input_db, opt_db, calculator, calc_type, label, specification):
    """
    Used to read the atoms objects in an input database, optimize the
    structures, and save the optimized structures to a new database.

    Checks if there is a unique ID assigned to each atoms object,
    If not, it assigns a unique ID to each atoms object.

    Args:
    - input_db (ASE db): the input database with input structure atoms objects.
    - opt_db (ASE db): the database with optimized structure atoms objects.
    - calculator (string): calculator name
    - calc_type (string): calculation type, sp (=single-point) or opt (=optimization)
    - label (string): The label for the new structures.
    """

    for row in input_db.select():
        name = row.name[13:-4]
        calculation_label = f"{name}_{label}"
        logging.info(f"-------------------------------")
        logging.info(f"Calculating {calculation_label}")

        # Creates a subfolder for each calculation to save output:
        create_folder(calculation_label)

        # Performs geometry optimisation:
        atoms = row.toatoms()
        opt_atoms = run_calc(
            calculator, atoms, calculation_label, calc_type, specification
        )

        os.chdir(os.path.join("..", ".."))

        if opt_atoms is not None:
            logging.info(f"\t\t Optimized {calculation_label}!")
        else:
            logging.info(
                f"\t\t Error in optimize_atoms for {calculation_label}: atoms is None."
            )

        # Saves the optimized structure and data to a database.
        # Checks if the foreign key is available, otherwise assigns a new one
        try:
            foreign_key = row.get("foreignkey", row.id)
            opt_db.write(
                opt_atoms,
                foreignkey=foreign_key,
                name=calculation_label,
                specification=specification,
                calc_type=calc_type,
            )
            logging.info(
                f"Wrote optimized structure to database {opt_db} with foreignkey {foreign_key}"
            )

        except Exception as e:
            logging.info(
                f"\t\t Error in writing to the database for {calculation_label}: {str(e)}"
            )


if __name__ == "__main__":

    # Initializes variables:
    prefix = "new_dimers"
    calculator = "gaussian"  # Change to either DFTB or Gaussian
    specification = "aug-cc-pvdz"  # Change to either GFN2 or basis set in Gaussian
    calc_type = "opt"  # Change to either sp (single-point) or opt (optimisation)
    label = f"{calculator}_{specification}_{calc_type}_1node"

    # Setting up databases:
    input_structures_db = connect(f"./db/{prefix}_DFTB_GFN2_opt_second_two.db")
    opt_db = connect(f"./db/{prefix}_{label}_test.db")

    # Performs the optimization:
    setup_logging()
    start_time, start = setup_start_time(label)
    print(f"Starting a new job with label {label} at {start_time}")

    optimize_atoms(
        input_db=input_structures_db,
        opt_db=opt_db,
        calculator=calculator,
        calc_type=calc_type,
        label=label,
        specification=specification,
    )

    end_time = setup_end_time(start, label)
    print(f"Ending job with label {label} at {end_time}")
