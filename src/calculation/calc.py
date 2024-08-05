# coding=utf-8

import logging
import os
import time
from datetime import datetime

import calculators
import hydra
from ase.db import connect
from ase.io import read, write
from omegaconf import DictConfig


def setup_from_config(job):
    """
    Setup configuration parameters from the job object.

    Args:
    - job: Configuration object with job parameters.

    Returns:
    - parametrization: Uppercased parametrization value or None.
    - method_parameters: List of method parameters for calculation.
    """

    kpoints_label = "-".join(str(x) for x in job.kpoints) if job.kpoints else ""
    parametrization = job.parametrization.upper() if job.parametrization else None
    lattice_opt = "lattice" if job.lattice_opt == "Yes" else "atomic"

    method_parameters = [
        job.calculator,
        job.functional,
        job.dispersion_correction,
        job.basis_set,
        str(job.encut),
        parametrization,
        kpoints_label,
        lattice_opt,
    ]
    
    return parametrization, lattice_opt, method_parameters
    
    
def setup_logging():
    """Setup logging configurations."""

    log_format = "[%(asctime)s] {%(pathname)s:%(lineno)d} %(message)s"
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
    """
    Setup start time for logging.
    Args:
    - label (str): Label for the job.
    - db_path (str): Path to the database.

    Returns:
    - float: Start time timestamp.
    """

    start_time = time.time()
    logging.info("-" * 80)
    logging.info(f"Starting a new job with label {label} at {format_time(start_time)}")
    logging.info(f"Path: {db_path}")

    return start_time


def set_up_database(db_path):
    """Set up a database connection from the db path."""
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
    method_label = "_".join(p for p in parameters if p is not None)

    label = f"{prefix}_{method_label}_{calc_type}"

    while "__" in label:
        label = label.replace("__", "_")

    if label.startswith("_"):
        label = label[1:]

    return label

def run_calc(
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
    """
    Run the calculation using the specified calculator.

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
    - opt_atoms: Optimized atoms object.
    """

    logging.info(f"\t\tPerforming an {calc_type} calculation in {calculator}")

    try:
        if calculator.lower() == "dftb":
            opt_atoms = calculators.DFTB_calculator(
                atoms, label, calc_type, parametrization, kpoints, lattice_opt
            )
        elif calculator.lower() == "gaussian":
            opt_atoms = calculators.Gaussian_calculator(
                atoms, label, calc_type, functional, dispersion_correction, basis_set
            )
        elif calculator.lower() == "vasp":
            opt_atoms = calculators.VASP_calculator(
                atoms,
                label,
                calc_type,
                functional,
                dispersion_correction,
                kpoints,
                cutoff,
                lattice_opt,
            )
        else:
            raise ValueError(f"Unsupported calculator: {calculator}")

    except Exception as e:
        logging.error(f"\t\tError in run_calc for {calculator} calculation: {str(e)}")
        return None

    return opt_atoms

def save_to_database(row, opt_atoms, calculation_label, calc_type, opt_db, counter):

    try:
        foreign_key = counter if row is None else row.get("foreignkey", row.id)
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


def optimize_atoms(
    input_atom,
    row,
    opt_db,
    calculator,
    calc_type,
    calculation_label,
    functional,
    dispersion_correction,
    basis_set,
    parametrization,
    kpoints,
    cutoff,
    lattice_opt,
    counter,
):
    """
    Optimize structures and save them to a new database.

    Args:
    - input_atom: Atom object to be optimized.
    - row: Database row for the current atom (used for foreign key).
    - opt_db: Database object to save the optimized structures.
    - calculator (str): Calculator name.
    - calc_type (str): Calculation type, either "sp" for single-point or "opt" for optimization.
    - calculation_label (str): Label for the calculation.
    - functional (str): Functional used for the calculation.
    - dispersion_correction (str): Dispersion correction applied.
    - basis_set (str): Basis set used.
    - parametrization (str): Parametrization used.
    - kpoints (tuple): K-points used for the calculation.
    - cutoff (float): Cutoff energy for the calculation.
    - lattice_opt (str): Type of lattice optimization ("lattice" or "atomic").
    - counter (int): Counter for unique labeling.
    """
            
    logging.info("-" * 40)
    logging.info(f"Calculating {calculation_label}")
    
    create_folder(calculation_label)
    
    opt_atoms = run_calc(
        calculator,
        input_atom,
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
        
    if opt_atoms is not None:
        logging.info(f"\t\tOptimized {calculation_label}!")
    else:
        logging.error(
            f"\t\tError in optimize_atoms for {calculation_label}: atoms is None."
        )

    save_to_database(row, opt_atoms, calculation_label, calc_type, opt_db, counter)

    os.chdir(os.path.join("..", ".."))

    if opt_atoms is not None:
        logging.info(f"\t\tOptimized {calculation_label}!")
    else:
        logging.error(
            f"\t\tError in optimize_atoms for {calculation_label}: atoms is None."
        )


@hydra.main(version_base=None, config_path="../config/", config_name="config.yaml")
def main(cfg: DictConfig) -> None:
    
    # Create environment:
    job = cfg.job
    parametrization, lattice_opt_type, method_parameters = setup_from_config(job)
    label = create_label(job.prefix, method_parameters, job.calc_type)
    setup_logging()
    start = setup_start_time(label, cfg.paths.db_path)

    # Set up databases:
    input_db_path = os.path.join(cfg.paths.db_path, cfg.paths.input_db_name)
    if job.calculator == "dftb":
        opt_db_path = os.path.join(cfg.paths.db_path, f"{job.prefix}_{job.calculator}_{parametrization}_{job.calc_type}_{lattice_opt_type}.db")
    else:
        opt_db_path = os.path.join(cfg.paths.db_path, f"{job.prefix}_{job.calculator}_{job.calc_type}_{lattice_opt_type}.db")
    opt_db = set_up_database(opt_db_path)
    logging.info(f"Output database: {opt_db_path}")
    
    # Set up output path:
    if os.path.exists(cfg.paths.output_path):
        output_path = cfg.paths.output_path
    else:
        output_path = os.path.abspath(os.path.join(cfg.paths.db_path, os.pardir))

    os.makedirs(output_path, exist_ok=True)
    os.chdir(output_path)
    logging.info(f"Output path: {output_path}")
    
    # Perform calculation:
    input_atoms = []
    calculation_labels = []
    rows = []

    if input_db_path.endswith(".db"):
        logging.info(f"Input database: {input_db_path}")
        input_db = set_up_database(input_db_path)
        for i, row in enumerate(input_db.select(), start=1):
            input_atoms.append(row.toatoms())
            calculation_labels.append(f"{i}_{label}")
            rows.append(row) 

    elif input_db_path.endswith(".traj"):
        logging.info(f"Input trajectory: {input_db_path}")
        input_atoms = read(input_db_path, index=":")
        for i, atom in enumerate(input_atoms, start=1):
            calculation_labels.append(f"{i}_{label.replace('.traj', '')}")

    else:
        logging.info(f"Input file: {input_db_path}")
        input_atoms.append(read(input_db_path))
        label = label.replace('.xyz', '').replace('.vasp','')
        calculation_labels.append(f"{label}")

    for i, (atom, label) in enumerate(zip(input_atoms, calculation_labels)):
        optimize_atoms(
            input_atom=atom,
            row=rows[i] if rows else None,
            opt_db=opt_db,
            calculator=job.calculator,
            calc_type=job.calc_type,
            calculation_label=label,
            functional=job.functional,
            dispersion_correction=job.dispersion_correction,
            basis_set=job.basis_set,
            parametrization=parametrization,
            kpoints=tuple(job.kpoints) if job.kpoints is not None else (),
            cutoff=job.encut,
            lattice_opt=job.lattice_opt,
            counter=i+1,
            )

    setup_end_time(start, label)
    print(f"Ending job with label {label}.")


if __name__ == "__main__":
    main()
