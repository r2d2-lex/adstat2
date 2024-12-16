def safe_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0


def make_errors_result(errors) -> str:
    errors_str = ''
    for field in errors:
        try:
            errors_str = errors_str + f'{field} {errors[field][0]}\n'
        except (IndexError, KeyError):
            pass
    errors_str = errors_str.rstrip('\n')
    return errors_str
