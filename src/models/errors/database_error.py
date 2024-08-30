class DatabaseException(Exception):

    def __init__(self, http_status_code: int, error_message: str) -> None:
        self.http_status_code = http_status_code
        self.error_message = error_message
        super().__init__(self.error_message)
