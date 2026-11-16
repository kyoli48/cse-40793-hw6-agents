from domain.pricing import calculateTotal


def show_price(price, quantity):
    """Display a total; price is in dollars and the displayed total is in dollars."""
    print(calculateTotal(price, quantity))
