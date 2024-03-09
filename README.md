# Project in Advanced Scientific Computing with Python

## Overview
This project focuses on enhancing code readability and reproducibility while incorporating testing, documentation, and organization using GitHub. The primary objectives include enhancing the organization of project files and directories, providing clear instructions for conda environment setup, maintaining consistent code formatting, integrating GitHub actions for automated tasks, documenting, and implementing testing procedures.

My research focuses on Computational Chemistry. Thus, my project will be particularly tailored for tasks within this area, using the Atomic Simulation Environment ([ASE](https://wiki.fysik.dtu.dk/ase/)).

## Goals
This is a list of all the things I would like to do, in a somewhat prioritized order. Due to time limitations, I might not be able to finish them all within the timeline of this course.

- [x] Organize project files and directories logically for better project management and collaboration.

- [ ] Improve reproducibility by creating clear instructions for environment setup, using conda.

- [x] Enhance code readability through consistent code formatting, where I plan to try out [Ruff](https://github.com/astral-sh/ruff).

- [ ] Improve documentation for clear instructions on how to use my code.

- [ ] Transfer existing or partially completed analysis scripts to Jupyter notebooks for better and more interactive visualization. Evaluate their efficiency, readability, and structure.

- [ ] Incorporate GitHub actions.

- [ ] Implement testing procedures to ensure code reliability.






# Results from the Project


### File tree

```
root/
│
├── environment.yaml
├── README.md
└── project/
    ├── analysis/
    │   ├── plot_relative_energies.ipynb
    │   └── scan.py
    ├── calculation/
    │   ├── calculators.py
    │   └── opt.py
    ├── config/
    │   └── config.yaml
    └── run.sh
```

### File Descriptions

- **environment.yaml**: This file contains the specifications for creating a conda environment with all the necessary dependencies for the project.

- **README.md**: This is the README file providing an overview of the project, its goals, and instructions for setup and usage.

- **project/**: This directory contains the components of the project.

  - **analysis/**: Contains scripts and notebooks for preparation of data, data analysis and visualization.
    - **plot_relative_energies.ipynb**: Jupyter notebook for plotting relative energies.
    - **scan.py**: Script for performing scans.
  
  - **calculation/**: Includes scripts for performing calculations.
    - **calculators.py**: Script for defining different calculators.
    - **opt.py**: Script for calculations.
  
  - **config/**: Contains configuration files.
    - **config.yaml**: Configuration file for the project.

- **run.sh**: Shell script for executing the project.

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

### Hydra Configuration File (config.yml):

Configuration file for running calculation jobs using Hydra.

Configuration options:
- job.prefix: Descriptive name for the project.
- job.calculator: Choice of calculator (e.g., 'gaussian', 'dftb', 'vasp').
- job.specification: Specification of level of theory 
  (e.g., 'aug-cc-pvdz', 'GFN2').
- job.calc_type: Type of calculation ('opt' for optimization, 
  'sp' for single-point).
- job.label: Label for the job (constructed dynamically).
- databases.input_db_path: Path to the input database with initial structures.
- databases.opt_db_path: Path to the output database where optimized structures 
  will be saved.

## 