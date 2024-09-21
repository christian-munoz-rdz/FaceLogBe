from typing import Any


class HandledException(Exception):
    def __init__(self, error: Exception, details: Any ) -> None:
        self.error = error
        self.details = details
        super().__init__(self.error)