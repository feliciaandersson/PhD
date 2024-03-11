from ase.db import connect

# delete rows in an ASE database
db_path = "db_name.db"
db = connect(db_path)
db.delete(range(1, 10))
