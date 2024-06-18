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


# Loop over each database file in the specified directory
for db_file in /home/felicia/Cellulose/machine_learning_project/training/structure_opts/4_2*.db; do
    python ./calculation/opt.py $(cat <<EOF
        job.prefix=$(basename $db_file .db)
        job.calculator=DFTB
        job.functional=
        job.dispersion_correction=
        job.basis_set=
        job.parametrization=GFN2
        job.kpoints=
        job.encut=
        job.lattice_opt=
        job.calc_type=sp

        paths.output_path=
        paths.db_path=/home/felicia/Cellulose/calculations/DFTB/DFTB_crystals/beta/beta_B/db
        paths.input_db_name=$db_file
EOF
)
done