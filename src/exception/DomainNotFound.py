class DomainNotFound(Exception):
    def __init__(self, message="Không tìm thấy domain"):
        super().__init__(message)