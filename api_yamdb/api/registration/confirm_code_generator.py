import random
import string

CODE_SIZE = 6


def generator(
    size=CODE_SIZE,
    chars=string.ascii_uppercase + string.digits
):
    return ''.join(random.choice(chars) for _ in range(size))
