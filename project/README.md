# Calculation

## Hydra Configuration File:
(config.yaml)

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