#!/bin/bash

#SBATCH -A naiss2023-1-37
#SBATCH --mail-type=BEGIN,END
#SBATCH --mail-user=felicia.e.andersson@kemi.uu.se
#SBATCH --cpus-per-task=32
#SBATCH --ntasks-per-node=1
#SBATCH --job-name=dimers
#SBATCH --nodes=1
#SBATCH -t 00:00:30

# Set neccessary requirements
ulimit -s unlimited
export OMP_STACKSIZE=8G

# Load the Gaussian module
module load Gaussian/16.C.01-avx2-nsc1-bdist

# run optimization
opt.py