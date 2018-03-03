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
    query = """INSERT IGNORE INTO {} ({}) VALUES ({});""".format(table, columns, values)

    cursor.executemany(query, payload['values'])
    cursor.close()
    db_conn.commit()

def insert_to_db(site_name):
    sites = ["amazon", "shopee", "lazada"]

    if not(site_name in sites):
        print("Invalid site")
        return

    product_table_name = site_name + "_products"
    comments_table_name = site_name + "_comments"

    product_columns = ["product_name", "original_price", "current_price", "product_description", "product_link", "rating", "image_link"]
    comment_columns = ["product_id", "comment"]

    product_payload = {
            "columns": product_columns,
            "values": []
    }

    comments_payload = {
            "columns": comment_columns,
            "values": []
    }

    LIMIT = 100

    try: 
        with open('data/{}.json'.format(product_table_name)) as f:
            data = json.load(f)
            counter = 0

            for item in data:
                if counter >= LIMIT or data.index(item) == len(data)-1:
                    insert_many('my_sql.cnf', product_table_name, product_payload)
                    insert_many('my_sql.cnf', comments_table_name, comments_payload)
                    product_payload["values"] = []
                    comments_payload["values"] = []
                    counter = 0
                else:
                    if (table_name == 'amazon_products'):
                        item["product_description"] = "\n".join(item["product_description"])
                        for key in item:
                            if item[key] is None:
                                item[key] = "-1"

                    pid = item["product_link"]
                    comments = "\n".join(item.pop("comments"))

                    comments_payload["values"].append(tuple([pid, comments]))
                    product_payload["values"].append(tuple(item.values()))
                    counter += 1
    except FileNotFoundError:
        return

# insert_to_db('shopee')
# insert_to_db('lazada')
# insert_to_db('amazon')
