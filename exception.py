class NameNotFoundError(Exception):
    def __init__(self, error_msg=""):
        self.message = f"{str(error_msg)} database type or name not existed."
        super().__init__(self.message)