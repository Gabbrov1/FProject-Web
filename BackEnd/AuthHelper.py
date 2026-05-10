import bcrypt




def hash_password(password: str) -> str:
    """_summary_

    Args:
        password (_type_): Password to be encrypted and salted

    Returns:
        _type_: _description_
    """
    
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


def check_password(password: str, hashed: str) -> bool:
    """_summary_

    Args:
        password (String): unencrypted password to be checked
        hashed (String): encrypted password to be compared against

    Returns:
        bool: _description_
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

