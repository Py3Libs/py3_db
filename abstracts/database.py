import abc
import cx_Oracle


class IDatabase(abc.ABC):

    @abc.abstractmethod
    def open_conn(self):
        raise NotImplementedError

    @abc.abstractmethod
    def close_conn(self):
        raise NotImplementedError

    @abc.abstractmethod
    def is_opened(self) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def query(self, sql:str, dict_format:bool):
        raise NotImplementedError

    @abc.abstractmethod
    def execute(self, sql:str, auto_commit:bool):
        raise NotImplementedError
    
    @abc.abstractmethod
    def execute_many(self, sql:str, data:list, auto_commit:bool):
        raise NotImplementedError

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError