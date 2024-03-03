# coding=utf-8

import os
import logging
import time

import hydra
from omegaconf import DictConfig, OmegaConf

import calculators
from ase.db import connect


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
    logging.info(f"--------------------------------------------------------------")
    logging.info(f"Starting a new job with label {label} at {start_time}")

    return start


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
        name = row.name[13:-4]
        calculation_label = f"{name}_{label}"
        logging.info(f"-------------------------------")
        logging.info(f"Calculating {calculation_label}")

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


@hydra.main(version_base=None, config_path="../config/", config_name="config.yaml")
def my_app(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))
    # log.info("Info level message")
    # log.debug("Debug level message")

    # Access configuration parameters
    job = cfg.job
    databases = cfg.databases

    prefix = job.prefix
    calculator = job.calculator
    specification = job.specification
    calc_type = job.calc_type
    label = job.label
    input_db_path = databases.input_db_path
    opt_db_path = databases.opt_db_path

    # Setting up databases:
    input_structures_db = connect(input_db_path)
    opt_db = connect(opt_db_path)

    # Performs the optimization:
    setup_logging()
    start = setup_start_time(label)

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


if __name__ == "__main__":
    my_app()
