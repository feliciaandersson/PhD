# Project in Advanced Scientific Computing with Python

## Overview
This project focuses on enhancing code readability and reproducibility while incorporating testing, documentation, and organization using GitHub. The primary objectives include enhancing the organization of project files and directories, providing clear instructions for conda environment setup, maintaining consistent code formatting, integrating GitHub actions for automated tasks, documenting, and implementing testing procedures.

My research focuses on Computational Chemistry. Thus, my project will be particularly tailored for tasks within this area, using the Atomic Simulation Environment ([ASE](https://wiki.fysik.dtu.dk/ase/)) at the supercomputer cluster ([Tetralith](https://www.nsc.liu.se/systems/tetralith/))

## Goals
This is a list of all the things I would like to do, in a somewhat prioritized order. Due to time limitations, I might not be able to finish them all within the timeline of this course.

- [x] Organize project files and directories logically for better project management and collaboration.

- [x] Improve reproducibility by creating clear instructions for environment setup, using conda.

- [x] Enhance code readability through consistent code formatting, where I plan to try out [Ruff](https://github.com/astral-sh/ruff).

- [x] Improve documentation for clear instructions on how to use my code.

- [x] Transfer existing or partially completed analysis scripts to Jupyter notebooks for better and more interactive visualization. Evaluate their efficiency, readability, and structure.

- [ ] ~~Incorporate GitHub actions.~~

- [ ] ~~Implement testing procedures to ensure code reliability.~~






# Results from the Project


### File tree

```
root/
├── environment.yaml
├── README.md
└── src/
    ├── analysis/
    │   └── plot_relative_energies.ipynb
    ├── calculation/
    │   ├── __pycache__/
    │   ├── calculators.py
    │   └── calc.py
    ├── config/
    │   └── config.yaml
    ├── processing/
    │   └── scan.py
    ├── run.sh
    ├── manual_run.sh
    └── utils/
        └── create_directory_tree.ipynb
```

### File Descriptions

- **environment.yaml**: This file contains the specifications for creating a Conda environment with all the necessary dependencies for the project.

- **README.md**: This is the README file providing an overview of the project, its goals, and instructions for setup and usage.

- **src/**: This directory contains the source code of the project.

  - **analysis/**: Contains scripts and notebooks for data preparation, analysis, and visualization.

    - **plot_relative_energies.ipynb**: Jupyter notebook for plotting relative energies.

  - **calculation/**: Includes scripts for performing calculations.

    - **calculators.py**: Script for defining different calculators.
    - **opt.py**: Script for calculations.

  - **config/**: Contains configuration files.

    - **config.yaml**: Configuration file for the project.

  - **processing/**: Contains scripts for processing data.

    - **scan.py**: Script for performing scans.

  - **run.sh**: Shell script for executing the project, submitting it to a SLURM queue.
  - **manual_run.sh**: Shell script for executing the project without submitting it to a SLURM queue.

  - **utils/**: Contains utility scripts.

    - **create_directory_tree.ipynb**: Jupyter notebook for creating a directory tree.


## Prerequisites

### Anaconda or Miniconda Installation:
   - If you haven't already, download and install Anaconda or Miniconda from the [official website](https://www.anaconda.com/products/distribution) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html).
   - Follow the installation instructions provided for your operating system.

## Installation

To install the necessary dependencies, create a conda environment using the 
provided `environment.yaml` file:

```bash
conda env create -f environment.yaml
```

To update the environment if you have made changes to the  `environment.yaml` 
file, use:

```bash
conda env update -f environment.yaml --prune
```

## Usage

### Setting up Hydra Configuration (config.yaml)
Begin by configuring your job using the provided config.yaml file.
The parameters are modified according to your specific requirements in the run.sh script.
Below is a brief explanation of each parameter in the config file:

**job**:
- **Restart:** Specify whether to restart the calculation (`True` or `False`). Default is `False`.
- **Prefix:** Prefix for job identification.
- **Calculator:** Choose the calculator type (`DFTB`, `Gaussian`, `Vasp`).
- **Functional:** Specify the functional used in calculations (`PBE`, `RPBE`, `PBEsol`, `B3LYP`, or calculator-specific options).
- **Basis Set:** Define the basis set to be employed.
- **Parametrization:** Specify the parametrization for DFTB (`GFN1`, `GFN2`).
- **K-points:** Define the k-points for the calculation (e.g., `[1, 1, 1]`).
- **Energy Cutoff (`encut`):** Specify the energy cutoff for VASP. Default is `500`.
- **Lattice Optimization (`lattice_opt`):** Choose between `"yes"` or `"no"`.
- **Dispersion Correction:** Specify if dispersion correction is applied.
- **calc_type**: The type of calculation (either "opt" for optimization or "sp" for single-point).

**paths**:
- **Output Path:** Specify the output path. By default, it's the parent directory of `db_path`.
- **Database Path (`db_path`):** The path to the database directory.
- **Input Database Name (`input_db_name`):** The name of the input database.


### Submitting the Job to the SLURM queue(run.sh)
To submit your job to the SLURM queue on Tetralith, use the provided bash job script `run.sh`.
You may need to customize certain details in the script. At the minimum, ensure to specify the 
name of the account you use to perform computations, as well as an appropriate job time and job name.
Modify the config prameters to fit your requirements.

You can submit the job by executing the following command in the terminal:

```bash
sbatch run.sh
```

Monitor the job status using SLURM commands such as squeue.

```bash
squeue -l -u $USER
```

### Executing the code with Python
If you want to run the code at a computer that does not use the SLURM queue,
there is a bash script `manual_run.sh`, which works similar to `run.sh`.
You can start the job by executing the following command in a terminal:

```bash
bash manual_run.sh
```

or similarly, you can execute it using python (this is not recommended 
unless you do not have to change the config file between jobs):

```python
python opt.py
```
