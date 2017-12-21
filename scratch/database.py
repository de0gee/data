import sqlite3
import os
import time 

try:
  os.remove('test2.db')
except:
  pass

table_name1 = 'my_table_1'  # name of the table to be created
table_name2 = 'my_table_2'  # name of the table to be created
new_field = 'my_1st_column' # name of the column
field_type = 'INTEGER'  # column data type

# Connecting to the database file
conn = sqlite3.connect('test2.db' )
c = conn.cursor()

# Creating a new SQLite table with 1 column
c.execute('CREATE TABLE {tn} ({nf} {ft})'\
        .format(tn=table_name1, nf=new_field, ft=field_type))

# Creating a second table with 1 column and set it as PRIMARY KEY
# note that PRIMARY KEY column must consist of unique values!
c.execute('CREATE TABLE {tn} ({nf} {ft} PRIMARY KEY)'\
        .format(tn=table_name2, nf=new_field, ft=field_type))

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()



table_name = 'my_table_2'   # name of the table to be created
id_column = 'my_1st_column' # name of the PRIMARY KEY column
new_column1 = 'my_2nd_column'  # name of the new column
new_column2 = 'my_3nd_column'  # name of the new column
column_type = 'TEXT' # E.g., INTEGER, TEXT, NULL, REAL, BLOB
default_val = 'Hello World' # a default value for the new column rows

# Connecting to the database file
conn = sqlite3.connect('test2.db' )
c = conn.cursor()


# A) Adding a new column without a row value
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name, cn=new_column1, ct=column_type))

# B) Adding a new column with a default row value
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct} DEFAULT '{df}'"\
        .format(tn=table_name, cn=new_column2, ct=column_type, df=default_val))

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()

import filelock

def insertSomething(something):   
    lock = filelock.FileLock("my_lock_file")
    while True:
        try:
            with lock.acquire(timeout=1):
                print("starting",something)
                doInsert(something)
                break
        except filelock.Timeout:
            continue
    print("ending",something)


def doInsert(something):
    table_name = 'my_table_2'
    id_column = 'my_1st_column'
    column_name = 'my_2nd_column'
    # Connecting to the database file
    print(something)
    conn = sqlite3.connect("file:test2.db",uri=True)
    c = conn.cursor()

    # A) Inserts an ID with a specific value in a second column
    for i in range(100+something):
      try:
          c.execute("INSERT INTO {tn} ({idf}, {cn}) VALUES ({sm}, 'test')".\
              format(tn=table_name, idf=id_column, cn=column_name,sm=i))
      except sqlite3.IntegrityError:
          pass

    # with a specific value in a second column
    c.execute("INSERT OR IGNORE INTO {tn} ({idf}, {cn}) VALUES ({sm}, 'test')".\
            format(tn=table_name, idf=id_column, cn=column_name,sm=something))

    
    for i in range(100):        
      c.execute("UPDATE {tn} SET {cn}=('Hi World') WHERE {idf}=({sm})".\
            format(tn=table_name, cn=column_name, idf=id_column,sm=something))
    time.sleep(1)
    conn.commit()
    conn.close()

def readSomething():
    while True:
        try:
            data = readIt()
            break
        except sqlite3.OperationalError:
            time.sleep(0.01)
            print("locked, continuing")
            continue
    return data

def readIt():
    table_name = 'my_table_2'
    column_2 = 'my_2nd_column'
    conn = sqlite3.connect("file:test2.db?mode=ro",uri=True)
    c = conn.cursor()
    # 1) Contents of all columns for row that match a certain value in 1 column
    c.execute('SELECT * FROM {tn} WHERE {cn}="Hi World"'.
              format(tn=table_name, cn=column_2))
    all_rows = c.fetchall()
    c.close()
    conn.close()
    return all_rows
 
import threading

insertSomething(123)

thr = threading.Thread(target=insertSomething, args=(1234,), kwargs={})
thr2 = threading.Thread(target=insertSomething, args=(12345,), kwargs={})
thr3 = threading.Thread(target=insertSomething, args=(12,), kwargs={})
thr4 = threading.Thread(target=insertSomething, args=(500000,), kwargs={})
thr5 = threading.Thread(target=insertSomething, args=(65656,), kwargs={})
thr.start()
thr2.start()
thr3.start()
thr4.start()
thr5.start()
print("reading")
for i in range(10000):
  a = readSomething()
print("reading done")
print(a)
thr.join()
thr2.join()
thr3.join()
thr4.join()
thr5.join()