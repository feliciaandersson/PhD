# Project in Advanced Scientific Computing with Python

## Overview
This project focuses on enhancing code readability and reproducibility while incorporating testing, documentation, and organization using GitHub. The primary objectives include enhancing the organization of project files and directories, providing clear instructions for conda environment setup, maintaining consistent code formatting, integrating GitHub actions for automated tasks, documenting, and implementing testing procedures.

My research focuses on Computational Chemistry. Thus, my project will be particularly tailored for tasks within this area, using the Atomic Simulation Environment ([ASE](https://wiki.fysik.dtu.dk/ase/)).

## Goals
This is a list of all the things I would like to do, in a somewhat prioritized order. Due to time limitations, I might not be able to finish them all within the timeline of this course.

- [ ] Organize project files and directories logically for better project management and collaboration.

- [ ] Improve reproducibility by creating clear instructions for environment setup, using conda.

- [ ] Enhance code readability through consistent code formatting, where I plan to try out [Ruff](https://github.com/astral-sh/ruff).

- [ ] Improve documentation for clear instructions on how to use my code.

- [ ] Transfer existing or partially completed analysis scripts to Jupyter notebooks for better and more interactive visualization. Evaluate their efficiency, readability, and structure.

- [ ] Incorporate GitHub actions.

- [ ] Implement testing procedures to ensure code reliability.






# Results from the Project

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