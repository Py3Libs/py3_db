import abc
from abstracts.database import IDatabase


class IDatabaseFactory(abc.ABC):

    @abc.abstractmethod
    def get_database(self, db_type:str, db_name:str) -> IDatabase:
        """
        Args:
            db_type (str): [database type like 'oracle', 'postgres']
            db_name (str): [pre-define database name in config.json ]
            schema (str): [only for postgres]
        """
        raise NotImplementedError