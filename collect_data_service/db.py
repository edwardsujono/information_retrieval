import MySQLdb
import configparser
import json

def connect_db(config_file):
    config = configparser.ConfigParser()
    config.readfp(open(config_file))

    db_name = config.get('client', 'database')
    user = config.get('client', 'user')
    password = config.get('client', 'password')
    host = config.get('client', 'host')
    port = int(config.get('client', 'port'))

    db_conn = MySQLdb.connect(host=host, user=user, passwd=password, db=db_name, port=port)
    return db_conn

def insert_one(config_file, table, payload):
    db_conn = connect_db(config_file)
    db_conn.set_character_set('utf8mb4')
    cursor = db_conn.cursor()

    cursor.execute('SET NAMES utf8mb4;')
    cursor.execute('SET CHARACTER SET utf8mb4;')
    cursor.execute('SET character_set_connection=utf8mb4;')

    columns = ', '.join(payload.keys())
    tmp = payload
    for item in tmp:
        tmp[item] = '"{}"'.format(tmp[item])
    values = ', '.join(tmp.values())

    query = """INSERT INTO {} ({}) VALUES ({});""".format(table, columns, values)

    cursor.execute(query)
    cursor.close()
    db_conn.commit()

def insert_many(config_file, table, payload):
    db_conn = connect_db(config_file)
    db_conn.set_character_set('utf8mb4')
    cursor = db_conn.cursor()

    cursor.execute('SET NAMES utf8mb4;')
    cursor.execute('SET CHARACTER SET utf8mb4;')
    cursor.execute('SET character_set_connection=utf8mb4;')

    columns = ', '.join(payload['columns'])
    values = ', '.join(['%s' for i in range(len(payload['columns']))])
    query = """INSERT INTO {} ({}) VALUES ({});""".format(table, columns, values)

    cursor.executemany(query, payload['values'])
    cursor.close()
    db_conn.commit()

def insert_to_db(table_name):
    payload = {
            "columns": [],
            "values": []
    }
    LIMIT = 100

    try: 
        with open('data/{}.json'.format(table_name)) as f:
            data = json.load(f)
            payload["columns"] = list(data[0].keys())
            counter = 0

            for item in data:
                if counter >= LIMIT:
                    insert_many('my_sql.cnf', table_name, payload)
                    payload["values"] = []
                    counter = 0
                else:
                    payload["values"].append(tuple(item.values()))
                    counter += 1
            insert_many('my_sql.cnf', table_name, payload)
    except FileNotFoundError:
        return

insert_to_db('shopee_products')
# insert_to_db('lazada_products')
# insert_to_db('amazon_products')
