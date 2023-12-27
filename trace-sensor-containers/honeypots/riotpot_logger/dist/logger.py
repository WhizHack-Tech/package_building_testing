#!/usr/bin/python3

from sqlalchemy import create_engine
import pandas.io.sql as sqlio
import pandas as pd
import os, time, gc

def log_loop(connection_engine):
    table_name = "connections"
    print("[i] Connected with the database. Starting infinite lookup loop.")
    while True:
        data = sqlio.read_sql_query(f"SELECT * FROM {table_name};", connection_engine)
        if data.empty:
            del data
        else:
            data['timestamp'] = data['timestamp'].dt.strftime("%Y-%m-%d %H-%M-%S")
            log_file = open("/var/log/riotpot/logs.json","a")
            # If file doesnt exists then create one.
            if os.path.getsize("/var/log/riotpot/logs.json") == 0:
                i = 0
                for row in data.iterrows():
                    row[1].to_json(log_file)
                    if i != len(data) - 1:
                        log_file.write("\n")
                    else:
                        pass
                    i = i+1
            # If it does exist then ensure your add a newline before you start writing data.
            else:
                i = 0
                log_file.write("\n")
                for row in data.iterrows():
                    row[1].to_json(log_file)
                    if i != len(data) - 1:
                        log_file.write("\n")
                    else:
                        pass
                    i = i+1
            del data
            gc.collect()
        connection_engine.execute(f"TRUNCATE TABLE {table_name};")
        time.sleep(2)

def connect():
    try:
        connection_engine = create_engine("postgresql+psycopg2://user:password@postgres/db")
        log_loop(connection_engine)
    except Exception as error:
        print("[e] Failed in connecting with the database.")
        print(error)

if __name__ == "__main__":
    connect()