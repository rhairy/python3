import dbm

# Create a 'n'ew empty database.
db = dbm.open('demo.dbm', 'n')

# Store some values in the database.
db['Randy'] = 'Good'
db['Gavin'] = 'Cool'
db['Jeremy'] = 'Techy'

# Cose the database.
db.close()
