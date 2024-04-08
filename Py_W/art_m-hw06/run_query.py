import sqlite3


def execute_sql(db_path, sql_file):
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        with open(sql_file, 'r',  encoding="utf8") as file:
            sql_ = file.read()
        cur.execute(sql_)
        rows = cur.fetchall()

        for row in rows:
            print(row)

    except sqlite3.Error as e:
        print(f"Error executing SQL script: {e}")
    finally:
        if conn:
            conn.close()


db_path = 'hw6_database.db'
query = [f'sql/queries/query_{i}.sql' for i in range(1, 11)]

for i, sql_file in enumerate(query, start=1):
    print(f"Executing query number: {i}")
    execute_sql(db_path, sql_file)
    print("\n")
