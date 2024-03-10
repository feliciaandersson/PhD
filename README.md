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
    │   └── opt.py
    ├── config/
    │   └── config.yaml
    ├── processing/
    │   └── scan.py
    ├── run.sh
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

  - **run.sh**: Shell script for executing the project.

  - **utils/**: Contains utility scripts.

    - **create_directory_tree.ipynb**: Jupyter notebook for creating a directory tree.


## Prerequisites

### Anaconda or Miniconda Installation:
   - If you haven't already, download and install Anaconda or Miniconda from the [official website](https://www.anaconda.com/products/distribution) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html).
   - Follow the installation instructions provided for your operating system.

## Installation

To install the necessary dependencies, create a conda environment using the 
provided `environment.yml` file:

```bash
conda env create -f environment.yml
```

To update the environment if you have made changes to the  `environment.yml` 
file, use:

```bash
conda env update -f environment.yml --prune
```

## Usage

### Setting Up Configuration (config.yaml)
Begin by configuring your job using the provided config.yaml file. 
Modify the parameters according to your specific requirements.
Save the modifications to the config.yaml file.

Below is a brief explanation of each parameter:

**job**:
- **prefix**: Prefix for job identification.
- **calculator**: The type of calculator to be used (for now, the supported calculators are VASP, Gaussian, and DFTB).
- **functional**: The functional used in calculations (e.g., PBE).
- **basis_set**: The basis set to be employed.
- **parametrization**: Parameterization (supported: GFN1, GFN2).
- **kpoints**: The k-point grid dimensions.
- **calc_type**: The type of calculation (either "opt" for optimization or "sp" for single-point).

**databases**:
- **db_path**: The path to the database directory.
- **input_db_name**: The name of the input database.


### Submitting the Job (run.sh)
At tetralith, use the provided batch script run.sh to submit your job to the SLURM queue. 
You can submit the job by executing the following command in the terminal:

```bash
sbatch run.sh
```

Monitor the job status using SLURM commands such as squeue.

```bash
squeue -u $USER
```