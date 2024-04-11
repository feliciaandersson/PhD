# coding=utf-8

import logging
import os
import time
from datetime import datetime

import calculators
import hydra
from ase.db import connect
from omegaconf import DictConfig


def setup_logging():
    """Setup logging configurations."""
    log_format = "[%(asctime)s] {%(pathname)s:%(lineno)d} %(message)s  "
    logging.basicConfig(
        filename="logfile.log",
        level=logging.INFO,
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def format_time(timestamp):
    """Format time to a readable string."""
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def setup_start_time(label, db_path):
    """Set up the start time for logging.

    Args:
        label (str): The label for the job.
        db_path (str): The path of the database.

    Returns:
        start_time (float): The start time.
    """
    start_time = time.time()
    logging.info("-" * 80)
    logging.info(f"Starting a new job with label {label} at {format_time(start_time)}")
    logging.info(f"Path: {db_path}")

    return start_time


def set_up_database(db_path):
    """Set up the database connection.

    Args:
        db_path (str): The path of the database.

    Returns:
        structures_db (ase.db.Database): The database connection.
    """

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
    end_time = time.time()
    formatted_job_time = time.strftime("%H:%M:%S", time.gmtime(end_time - start))
    logging.info(f"Ending job with label {label} at {format_time(end_time)}.")
    logging.info(
        f"Job with label {label} started at {format_time(start)} and took {formatted_job_time}."
    )

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


def create_label(prefix, parameters, calc_type):
    """Create a label for a calculation.

    Args:
        prefix (str): The prefix for the label.
        parameters (list): The parameters for the label.
        calc_type (str): The type of calculation.

    Returns:
        label (str): The created label.
    """

    method_label = "_".join(p for p in parameters if p is not None)

    label = f"{prefix}_{method_label}_{calc_type}"

    while "__" in label:
        label = label.replace("__", "_")

    if label.startswith("_"):
        label = label[1:]

    return label


def run_calc(
    restart,
    calculator,
    atoms,
    label,
    calc_type,
    functional,
    dispersion_correction,
    basis_set,
    parametrization,
    kpoints,
    cutoff,
    lattice_opt,
):
    """Run a calculation using the specified calculator.

    Args:
        restart (bool): Whether to restart the calculation.
        calculator (str): The name of the calculator.
        atoms: The Atoms object retrieved from a database.
        label (str): The label of the structure.
        calc_type (str): The type of calculation (opt or sp).
        functional (str): The functional for the calculation.
        dispersion_correction (str): The dispersion correction method.
        basis_set (str): The basis set for the calculation.
        parametrization (str): The parametrization for the calculation.
        kpoints (tuple): The k-points for the calculation.
        cutoff (float): The cutoff energy for the calculation.
        lattice_opt (bool): Whether to perform lattice optimization.

    Returns:
        Atoms: The optimized Atoms object.
    """

    logging.info(f"\t\tPerforming an {calc_type} calculation in {calculator}")

    try:
        if calculator.lower() == "dftb":
            opt_atoms = calculators.DFTB_calculator(
                restart, atoms, label, calc_type, parametrization, kpoints, lattice_opt
            )
        elif calculator.lower() == "gaussian":
            opt_atoms = calculators.Gaussian_calculator(
                restart,
                atoms,
                label,
                calc_type,
                functional,
                dispersion_correction,
                basis_set,
            )
        elif calculator.lower() == "vasp":
            opt_atoms = calculators.VASP_calculator(
                restart,
                atoms,
                label,
                calc_type,
                functional,
                dispersion_correction,
                kpoints,
                cutoff,
                lattice_opt,
            )

    except Exception as e:
        logging.error(f"\t\tError in run_calc for {calculator} calculation: {str(e)}")
        return None

    return opt_atoms


def optimize_atoms(
    restart,
    input_db,
    opt_db,
    calculator,
    calc_type,
    label,
    functional,
    dispersion_correction,
    basis_set,
    parametrization,
    kpoints,
    cutoff,
    lattice_opt,
):
    """
    Optimize structures and save them to a new database.

    Args:
        restart (bool): Whether to restart the calculation.
        input_db (ase.db.Database): The input database with input structure Atoms objects.
        opt_db (ase.db.Database): The database with optimized structure Atoms objects.
        calculator (str): The name of the calculator.
        calc_type (str): The type of calculation (sp or opt).
        label (str): The label for the new structures.
        functional (str): The functional for the calculation.
        dispersion_correction (str): The dispersion correction method.
        basis_set (str): The basis set for the calculation.
        parametrization (str): The parametrization for the calculation.
        kpoints (tuple): The k-points for the calculation.
        cutoff (float): The cutoff energy for the calculation.
        lattice_opt (bool): Whether to perform lattice optimization.
    """

    for row in input_db.select():
        calculation_label = label
        logging.info("-" * 40)
        logging.info(f"Calculating {calculation_label}")

        create_folder(calculation_label)

        # Performs geometry optimisation:
        atoms = row.toatoms()
        opt_atoms = run_calc(
            restart,
            calculator,
            atoms,
            calculation_label,
            calc_type,
            functional,
            dispersion_correction,
            basis_set,
            parametrization,
            kpoints,
            cutoff,
            lattice_opt,
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
                name=calculation_label,
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
    """
    The main function to execute the job.

    Args:
        cfg (DictConfig): The configuration setup for the job.
    """

    job = cfg.job

    kpoints_label = "-".join(str(x) for x in job.kpoints) if job.kpoints else ""
    parametrization = (
        job.parametrization.upper() if job.parametrization is not None else None
    )
    method_parameters = [
        job.calculator,
        job.functional,
        job.dispersion_correction,
        job.basis_set,
        str(job.encut),
        parametrization,
        kpoints_label,
    ]

    label = create_label(job.prefix, method_parameters, job.calc_type)

    setup_logging()
    start = setup_start_time(label, cfg.paths.db_path)

    input_db_path = os.path.join(cfg.paths.db_path, cfg.paths.input_db_name)
    opt_db_path = os.path.join(
        cfg.paths.db_path, f"{job.prefix}_{job.calculator}_{job.calc_type}.db"
    )
    if os.path.exists(cfg.paths.output_path):
        output_path = cfg.paths.output_path
    else:
        output_path = os.path.abspath(os.path.join(cfg.paths.db_path, os.pardir))

    os.makedirs(output_path, exist_ok=True)
    os.chdir(output_path)
    logging.info(f"Output path: {output_path}")

    input_db = set_up_database(input_db_path)
    logging.info(f"Input database: {input_db_path}")
    opt_db = set_up_database(opt_db_path)
    logging.info(f"Output database: {opt_db_path}")

    optimize_atoms(
        restart=job.restart,
        input_db=input_db,
        opt_db=opt_db,
        calculator=job.calculator,
        calc_type=job.calc_type,
        label=label,
        functional=job.functional,
        dispersion_correction=job.dispersion_correction,
        parametrization=parametrization,
        basis_set=job.basis_set,
        kpoints=tuple(job.kpoints) if job.kpoints is not None else (),
        cutoff=job.encut,
        lattice_opt=job.lattice_opt,
    )

    end_time = setup_end_time(start, label)
    print(f"Ending job with label {label} at {format_time(end_time)}.")


if __name__ == "__main__":
    main()
