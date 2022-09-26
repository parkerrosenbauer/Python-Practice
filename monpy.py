import re

MONEY_CONVERSION = {
    "hundred-dollars": 10000,
    "fifty-dollars": 5000,
    "twenty-dollars": 2000,
    "ten-dollars": 1000,
    "five-dollars": 500,
    "two-dollars": 200,
    "dollars": 100,
    "half-dollars": 50,
    "quarters": 25,
    "dimes": 10,
    "nickels": 5,
    "pennies": 1
}


class Money:
    def __init__(self, dollars, cents):
        self.total_cents = dollars * 100 + cents

    def __repr__(self):
        """Render money object nicely on prompt."""
        return f"Money({self.dollars}.{self.cents})"

    @classmethod
    def from_string(cls, amount):
        match = re.search(r'^\$(?P<dollars>\d+)\.(?P<cents>\d\d)$', amount)
        if match is None:
            raise ValueError(f"Invalid amount: {repr(amount)}")
        dollars = int(match.group('dollars'))
        cents = int(match.group('cents'))
        return cls(dollars, cents)

    @classmethod
    def just_pennies(cls, amount):
        dollars = amount // 100
        cents = amount % 100
        return cls(dollars, cents)

    @classmethod
    def mixed_money(cls, **kwargs):
        total_cents = 0
        for money, amount in kwargs.items():
            if money not in MONEY_CONVERSION.keys():
                raise KeyError(f"{money} isn't a real unit of US currency.")
            total_cents += MONEY_CONVERSION[money] * amount
        dollars = total_cents // 100
        cents = total_cents % 100
        return cls(dollars, cents)

    @property
    def dollars(self):
        return self.total_cents // 100

    @dollars.setter
    def dollars(self, new_dollars):
        self.total_cents = 100 * new_dollars + self.total_cents

    @property
    def cents(self):
        return self.total_cents % 100

    @cents.setter
    def cents(self, new_cents):
        self.total_cents = 100 * self.dollars + new_cents

    def make_change(self) -> dict:
        cents_left = self.total_cents
        change = {}
        for currency_unit, value in MONEY_CONVERSION.items():
            num_currency_unit = cents_left // value
            if num_currency_unit > 0 and (currency_unit != "two-dollars" and currency_unit != "half-dollars"):
                change[currency_unit] = num_currency_unit
                cents_left -= num_currency_unit * value
        return change
