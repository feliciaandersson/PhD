#!/bin/bash

#SBATCH -A <your_account_name>
#SBATCH --time=01:00:00  # Replace with an appropriate time limit
#SBATCH --job-name=job_name  # Replace with a descriptive job name
#SBATCH --mail-user=<your_email_adress>

#SBATCH --mail-type=BEGIN,END
#SBATCH --cpus-per-task=32
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=1
#SBATCH --output=slurm-%x.%j.out

# Set neccessary requirements
ulimit -s unlimited
export OMP_STACKSIZE=8G

# Load the Gaussian module
module load Gaussian/16.C.01-avx2-nsc1-bdist

# Set paths and run the VASP module
export VASP_COMMAND='mpprun vasp_std'
export VASP_PP_PATH=/proj/teoroo/users/x_felan/VASP/input/
module add VASP/5.4.4.16052018-nsc2-intel-2018a-eb

# Run the calculation
python ./calculation/opt.py