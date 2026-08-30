class AppError(Exception):
    message: str = "Application error occurred."

    def __init__(self, message: str | None = None):
        super().__init__(message or self.message)


class ImageAlreadyExistsError(AppError):
    message: str = "Image already exists."


class UnsupportedImageExtension(AppError):
    message: str = "Unsupported image extension."
