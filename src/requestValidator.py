import re
def isValid(required, json):
    for field in required:
        if field not in json:
            return False
    return True

def isValidName(name):
    valid = re.match(r'^[\w-]+$', name) is not None
    return valid

def isValidNumber(id):
    return isinstance(id, int)

def isValidEmail(email):
    valid = re.match(r'[^@]+@[^@]+\.[^@]+', email) is not None
    return valid
