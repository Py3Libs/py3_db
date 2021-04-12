from dataclasses import dataclass
import cx_Oracle
from abstracts.database import IDatabase


@dataclass
class OracleConfig:
    host:str=""
    port:int=5673
    dbname:str=""
    username:str=""
    password:str=""
    encode:str="utf-8"
    tns:str=""


class OracleDatabase(IDatabase):

    def __init__(self, conn_config=None):
        self.__conn_config = conn_config
        self.__conn = None
        self.__cursor = None

    def open_conn(self):
        try:
            oralce_tns = self.__conn_config.tns

            if not oralce_tns:
                oralce_tns = cx_Oracle.makedsn(
                    self.__conn_config.host,
                    self.__conn_config.port,
                    self.__conn_config.dbname
                )

            self.__conn = cx_Oracle.connect(
                self.__conn_config.username,
                self.__conn_config.password,
                oralce_tns,
                encoding = self.__conn_config.encoding
            )

        except Exception as e:
            raise e

    def close_conn(self):
        try:
            if self.is_opened():
                self.__conn.close()

        except Exception as e:
            raise e

    def is_opened(self) -> bool:
        try:
            if self.__conn:
                return self.__conn.ping() is None

            return True

        except cx_Oracle.InterfaceError:
            return False

        except Exception as e:
            raise e

    def __is_cursor_opened(self):
        try:
            if self.__cursor is not None:
                return True

            return False

        except Exception as e:
            return None

    def query(self, sql="", dict_format=True):
        try:
            self.open_conn()
            with self.__conn.cursor() as cur:
                result = cur.execute(sql)
                
                if dict_format:
                    result.rowfactory = lambda *args: dict(zip([d[0] for d in result.description], args))

                return result.fetchall()

        except Exception as e:
            raise e

        finally:
            self.close_conn()

    def execute(self, sql="", auto_commit=True):
        try:
            if auto_commit:
                self.open_conn()
                with self.__conn.cursor() as cur:
                    cur.execute(sql)
                    self.commit()

                self.close_conn()

            else:
                if not self.is_opened():
                    self.open_conn()

                if not self.__is_cursor_opended():
                    self.__cursor = self.__conn.cursor()

                self.__cursor.execute(sql)

        except Exception as e:
            self.rollback()
            raise e
    
    def execute_many(self, sql="", data=[], auto_commit=True):
        try:
            errors = None

            if auto_commit:
                self.open_conn()
                with self.__conn.cursor() as cur:
                    cur.executemany(sql, data, batcherrors=True, arraydmlrowcounts=True)
                    self.commit()
                    errors = cur.getbatcherrors()

                self.close_conn()

            else:
                if not self.is_opened():
                    self.open_conn()

                if not self.__is_cursor_opended():
                    self.__cursor = self.__conn.cursor()

                self.__cursor.executemany(sql, data, batcherrors=True, arraydmlrowcounts=True)
                errors = self.__cursor.getbatcherrors()

            # if errors:
            #     for error in errors:
            #         print("number of errors whick took place:", len(errors))
            #         print("Error", error.message.rstrip(), "at row offset", error.offset)

        except Exception as e:
            self.rollback()
            raise e

    def commit(self):
        try:
            if self.__conn and self.is_opened():
                self.__conn.commit()

            if self.__is_cursor_opened():
                self.__cursor.close()
                self.__cursor = None

        except Exception as e:
            raise e

    def rollback(self):
        try:
            if self.__conn and self.is_opened():
                self.__conn.rollback()

            if self.__is_cursor_opened():
                self.__cursor.close()
                self.__cursor = None

        except Exception as e:
            raise e


