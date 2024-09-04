from decimal import Decimal

def format_number(num: float) -> Decimal:
    """
    Format a float for fixed-length output, while retaining number type.
    """

    return Decimal(num).quantize((Decimal('.0001')))