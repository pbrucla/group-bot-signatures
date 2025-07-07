class SignatureError(Exception):
    # for all signature library errors
    pass

class CanonicalizationError(SignatureError):
    # building the signature base fails
    pass

class ParameterError(SignatureError):
    #parsing or building signature params fails
    pass

class VerificationError(SignatureError):
    #signature does not verify
    pass
