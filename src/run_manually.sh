#!/bin/bash

# Set neccessary requirements
ulimit -s unlimited
export OMP_STACKSIZE=8G

# Run the calculation
python ./calculation/opt.py $(cat <<EOF
    job.prefix=a_descrptive_name
    job.calculator="calculator"
    job.functional="functional"
    job.dispersion_correction="disp_corr"
    job.basis_set=""
    job.parametrization="parametrization"
    job.kpoints=[1,1,1]
    job.encut=500
    job.lattice_opt="no"
    job.calc_type=opt

    paths.output_path=
    paths.db_path=./db/
    paths.input_db_name=database.db
EOF
)