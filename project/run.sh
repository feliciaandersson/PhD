#!/bin/bash

#SBATCH -A naiss2023-1-37
#SBATCH --mail-type=BEGIN,END
#SBATCH --mail-user=felicia.e.andersson@kemi.uu.se
#SBATCH --cpus-per-task=32
#SBATCH --ntasks-per-node=1
#SBATCH --job-name=vasp
#SBATCH --nodes=1
#SBATCH --time=00:01:00

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