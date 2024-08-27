def mask_number(number):
    masked_number = '*' * (len(number) - 4) + number[-4:]
    return masked_number