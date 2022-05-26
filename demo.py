import psycopg2

# Connecting to a postgres database
connection = psycopg2.connect('dbname=mydb user=postgres port=5432 password=abc')

# To start interacting with the database using psycopg2
cursor = connection.cursor()

# Destroy table3 if it exists
cursor.execute('DROP TABLE IF EXISTS table3;')

# To execute a set of commands within a transaction to a database
cursor.execute('''
CREATE TABLE table3(
    id INTEGER PRIMARY KEY,
    completed BOOLEAN NOT NULL DEFAULT False
);
''')

cursor.execute('INSERT INTO table3 (id, completed) VALUES (%s, %s);', (1, True))

SQL = 'INSERT INTO table3 (id, completed) VALUES (%(id)s, %(completed)s);'
data =  {
    "id": 2,
    "completed": False
}

cursor.execute(SQL, data)

cursor.execute('INSERT INTO table3 (id, completed) VALUES (%s, %s);', (3, True))

cursor.execute('SELECT * from table3;')

result = cursor.fetchmany(2)

print('1st result', result)

result2 = cursor.fetchone()

print('2nd result', result2)

cursor.execute('SELECT * from table3;')

result3 = cursor.fetchone()

print('3rd result', result3)

result4 = cursor.fetchmany(2)

print('4th result', result4)

result5 = cursor.fetchone()

print('5th result', result5)

# To execute the transaction
connection.commit()

# Close out your connection and cursor to indicate the end of a session
connection.close()

cursor.close()