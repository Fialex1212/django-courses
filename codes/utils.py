import random, string
from codes.models import ActivationCode


def generate_activation_code(length=12):
    chars = string.ascii_uppercase + string.digits
    code = "".join(random.choices(chars, k=length))
    while ActivationCode.objects.filter(code=code).exists():
        code = "".join(random.choices(chars, k=length))
    return code
