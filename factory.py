import os
import json
from exception import NameNotFoundError
from abstracts.factory import IDatabaseFactory
from database import ConnectConfig, OracleDatabase, PostgresDatabase


class DatabaseFactory(IDatabaseFactory):

    def __init__(self, config_filename=""):
        self.__config_filename = config_filename
        self.__config = None
        self.__init_config()

    def __init__config(self):
        with open(self.__config_filename, "r", encoding="utf-8") as f:
            self.__config = json.load(f)

    def get_database(self, db_type="ORACLE", db_name="") -> IDatabase:
        try:
            if not self.__config:
                return None

            conn_config = ConnectConfig(**self.__config[db_type][db_name])
            db = OracleDatabase(conn_config) if db_type == "ORACLE" else PostgresDatabase(conn_config)

            return db

        except KeyError as e:
            raise NameNotFoundError(e)

        except Exception as e:
            raise e