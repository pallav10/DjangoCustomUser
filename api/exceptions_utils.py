
class ValidationException(Exception):
    def __init__(self, errors, status):
        # Call the base class constructor with the parameters it needs
        super(ValidationException, self).__init__(status)

        # Now for your custom code...
        self.errors = errors
        self.status = status


