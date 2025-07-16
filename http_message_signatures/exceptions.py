
class SignatureError(Exception):
    # for all signature library errors'
    def __init__(self, message = None):
        super().__init__(message)
        self.message = message
    
    def __str__(self):
        errorType = self.__class__.__name__
        return f"{errorType} : {self.message}"
    

class CanonicalizationError(SignatureError):
    # building the signature base fails
    pass

class ParameterError(SignatureError):
    #parsing or building signature params fails
    pass

class VerificationError(SignatureError):
    #signature does not verify
    pass
