import mysql.connector

# Set up the connection details
config = {
  'user': 'root',
  'password': 'wase2022',
  'host': '34.89.81.147',
  'database': 'saniWASE_datasets',
  'port': 3306,
#   'ssl_ca': '/path/to/ca.pem' # Optional, for SSL encryption
}

# Connect to the MySQL server
cnx = mysql.connector.connect(**config)

# Execute a query
cursor = cnx.cursor()
query = 'SELECT * FROM gascomp_flowmeter'
cursor.execute(query)

# Retrieve the results
for row in cursor.fetchall():
    print(row)

# Close the connection
cnx.close()