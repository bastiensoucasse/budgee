"""Base models."""

from enum import StrEnum

from pydantic import Field
from pydantic.dataclasses import dataclass

from budgee.utils import slugify


@dataclass
class Person:
    """Person to manage."""

    name: str
    """Name of the person."""

    transactions: list[str] = Field(default_factory=list, kw_only=True)
    """List of the transaction IDs related to the person."""

    def id(self) -> str:
        """Gets the person identifier by slugifying its name.

        Returns:
            id: Person ID (slugified name).
        """
        return slugify(self.name)


@dataclass
class Transaction:
    """Transaction to manage."""

    class Category(StrEnum):
        """Transaction category."""

        HOUSING = "Housing"
        UTILITY = "Utility"
        ENTERTAINMENT = "Entertainment"
        DEVELOPMENT = "Development"
        MUSIC_PRODUCTION = "Music Production"
        HEALTH_FITNESS = "Health & Fitness"

    name: str
    """Name of the transaction."""

    value: float
    """Value of the transaction."""

    category: Category | None = None
    """Category of the transaction."""

    persons: list[str] = Field(default_factory=list, kw_only=True)
    """List of the person IDs related to the transaction."""

    def id(self) -> str:
        """Gets the transaction identifier by slugifying its name.

        Returns:
            id: Transaction ID (slugified name).
        """
        return slugify(self.name)

    def compute(self) -> float:
        """Computes the value of the transaction for one person.

        If only one person is related to the transaction, the return value will be the same as the total value.
        If several persons are related, the return value will be the total value
        divided by the number of person sharing the transaction.

        Returns:
            value: Value of the transaction for a single person.

        Raises:
            ValueError: If the transaction is not related to any person.
        """
        if len(self.persons) < 1:
            msg = f'{self.__class__.__name__} "{self}" unallocated.'
            raise ValueError(msg)
        return self.value / len(self.persons)


@dataclass
class Income(Transaction):
    """Income to manage."""

    def __post_init__(self) -> None:
        """Sets the value to positive (income) by multiplying it by -1 if negative."""
        if self.value < 0:
            self.value *= -1


@dataclass
class Expense(Transaction):
    """Expense to manage."""

    def __post_init__(self) -> None:
        """Sets the value to negative (expense) by multiplying it by -1 if positive."""
        if self.value > 0:
            self.value *= -1
