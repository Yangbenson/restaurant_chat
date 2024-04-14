import pymysql
import datetime

class DatabaseManager:
    def __init__(self, host, port, user, password, db, charset):
        self.db_settings = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "db": db,
            "charset": charset
        }
        self.connection = None

    def connect(self):
        self.connection = pymysql.connect(**self.db_settings)

    def close(self):
        if self.connection:
            self.connection.close()

    def create_table(self, table):
        try:
            self.connect()
            now = datetime.datetime.now()
            date_time_str = now.strftime("%Y-%m-%d")
            table_name = f"`{date_time_str}_{table}`"

            with self.connection.cursor() as cursor:
                cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

                create_statement = (
                    f'CREATE TABLE {table_name}('
                    '`id` INT NOT NULL AUTO_INCREMENT,'
                    '`acousticness` FLOAT NOT NULL,'
                    '`danceability` FLOAT NOT NULL,'
                    '`energy` FLOAT NOT NULL,'
                    '`instrumentalness` FLOAT NOT NULL,'
                    '`loudness` FLOAT NOT NULL,'
                    '`speechiness` FLOAT NOT NULL,'
                    '`tempo` INT NOT NULL,'
                    '`valence` FLOAT NOT NULL,'
                    '`key` FLOAT NOT NULL,'
                    '`duration_ms` FLOAT NOT NULL,'
                    '`Classification` VARCHAR(128),'
                    '`song_name` VARCHAR(512),'
                    'PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;'
                )
                cursor.execute(create_statement)
                self.connection.commit()

        except Exception as e:
            print(f"Error creating table: {e}")
        finally:
            self.close()

    def insert_data(self, table, df_insert):
        try:
            self.connect()
            now = datetime.datetime.now()
            date_time_str = now.strftime("%Y-%m-%d")
            table_name = f"`{date_time_str}_{table}`"

            values = [tuple(row) for row in df_insert.values]

            insert_statement = (
                f'INSERT INTO {self.db_settings["db"]}.{table_name} '
                '(acousticness, danceability, energy, instrumentalness, loudness, speechiness, tempo, valence, `key`, duration_ms, Classification, song_name) '
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            )

            with self.connection.cursor() as cursor:
                cursor.executemany(insert_statement, values)
                self.connection.commit()

        except Exception as e:
            print(f"Error inserting data: {e}")
        finally:
            self.close()

# 使用方法
db_manager = DatabaseManager(host="52.14.71.236", port=3306, user="benson", password="", db="portfolio", charset="utf8")

# 創建表
db_manager.create_table("your_table_name")

# 插入數據
# 假定 df 是一個 Pandas DataFrame，包含你要插入的數據
db_manager.insert_data("your_table_name", df)

#
# def SQL(table, db, kind, df_insert=""):
#     now = datetime.datetime.now()
#     date_time_str = now.strftime("%Y-%m-%d")
#
#     try:
#         db_settings = {
#             "host": "52.14.71.236",
#             "port": 3306,
#             "user": "benson",
#             "password": "",
#             "db": "portfolio",
#             "charset": "utf8"
#         }
#         conn = pymysql.connect(**db_settings)
#
#         if kind == "create":
#             with conn.cursor() as cursor:
#                 cursor.execute("DROP TABLE IF EXISTS "'`' + str(date_time_str) + '_' + table + '`')
#
#                 cursor.execute(
#                     'CREATE TABLE ' + '`' + str(date_time_str) + '_' + table + '`(' +
#                     '`id` INT NOT NULL AUTO_INCREMENT,' +
#                     '`acousticness` FlOAT NOT NULL,' +
#                     '`danceability` FlOAT NOT NULL,' +
#                     '`energy` FlOAT NOT NULL,' +
#                     '`instrumentalness` FlOAT NOT NULL,' +
#                     '`loudness` FlOAT NOT NULL,' +
#                     '`speechiness` FlOAT NOT NULL,' +
#                     '`tempo` INT NOT NULL,' +
#                     '`valence` FlOAT NOT NULL,' +
#                     '`key` FlOAT NOT NULL,' +
#                     '`duration_ms` FlOAT NOT NULL,' +
#                     '`Classification` VARCHAR(128),' +
#                     '`song_name` VARCHAR(512),' +
#                     'PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;'
#                 )
#
#         if kind == "insert":
#
#             df = df_insert
#
#             values = []
#
#             for i in range(len(df)):
#                 values.append(tuple(df.iloc[i, :]))
#
#             head = 'INSERT INTO ' + db + ".`" + str(
#                 date_time_str) + "_" + table + """` (acousticness,danceability,energy,instrumentalness,loudness,speechiness,tempo,valence,`key`,duration_ms,Classification,song_name) """ \
#                    + """VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
#
#             print('-------------print query--------------')
#             # print(head)
#             print(values)
#             with conn.cursor() as cursor:
#                 cursor.executemany(str(head), (values))
#                 insert = cursor.fetchall()
#                 conn.commit()
#                 conn.close()
#
#             print(insert)
#
#     except Exception as err:
#         print(err)
#
#         conn.close()
#         raise (err)
