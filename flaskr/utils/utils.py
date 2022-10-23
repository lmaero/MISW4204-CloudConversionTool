ALLOWED_EXTENSIONS = {'mp3', 'ogg', 'flac', 'aiff', 'wav', 'opus'}


def password_check(passwd):
    special_sym = ['$', '@', '#', '%']
    is_valid_password = True
    message = ""

    if len(passwd) < 6:
        message = 'Password length should be at least 6'
        is_valid_password = False

    if len(passwd) > 20:
        message = 'Length should be not be greater than 8'
        is_valid_password = False

    if not any(char.isdigit() for char in passwd):
        message = 'Password should have at least one numeral'
        is_valid_password = False

    if not any(char.isupper() for char in passwd):
        message = 'Password should have at least one uppercase letter'
        is_valid_password = False

    if not any(char.islower() for char in passwd):
        message = 'Password should have at least one lowercase letter'
        is_valid_password = False

    if not any(char in special_sym for char in passwd):
        message = 'Password should have at least one of the symbols $@#'
        is_valid_password = False

    return is_valid_password, message
