# coding=utf-8

from ase.db import connect
from ase.io import read, write

def separate(atoms):
    indices = range(len(atoms))
    indices_1 = [i for i in indices if atoms.positions[i, 0] < 1]
    indices_2 = [i for i in indices if atoms.positions[i, 0] >= 1]
    print(f"Indices in atoms_1: {len(indices_1)}")
    print(f"Indices in atoms_2: {len(indices_2)}")
    atoms_1 = atoms[indices_1]
    atoms_2 = atoms[indices_2]

    return atoms_1, atoms_2

def scan(atoms_1, atoms_2, displacement, num_closer, num_away, coordinate):
    
    coordinate_indices = {'x': 0, 'y': 1, 'z': 2}
    scanning_points = []
    coordinate_index = coordinate_indices[coordinate]
    print(f"Displacement in the {coordinate} direction.")
    
    start_position = num_closer * displacement
    atoms_1.positions[:, coordinate_index] += start_position
    print(f"Starting position: {start_position} closer than the optimised structure.")

    for iteration in range(num_closer + num_away + 1):
        atoms_1.positions[:, coordinate_index] -= (1 + iteration) * displacement
        atoms_combined = atoms_1 + atoms_2
        scanning_points.append(atoms_combined.copy())
        print(f"{iteration}: {atoms_1.positions[0, coordinate_index]}")
        
    return scanning_points

def save_to_db(scan_db, scanning_points):
    for iteration, scanning_point in enumerate(scanning_points):
        scan_db.write(atoms = scanning_point, name = iteration)

if __name__ == "__main__":
    label = "parallel_x_along_x_6_points"
    
    scan_db = connect(f"./{label}_scan_input.db")
    
    structure = "parallel_x.xyz"
    atoms = read(structure)
    
    atoms_1, atoms_2 = separate(atoms)
    
    coordinate = "x"
    displacement = 0.5
    num_closer = 0
    num_away = 6
    scanning_points = scan(atoms_1, atoms_2, displacement, num_closer, num_away, coordinate)
    
    save_to_db(scan_db, scanning_points)