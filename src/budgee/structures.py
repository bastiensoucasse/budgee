"""Data structures module."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Person:
    """Person to manage."""

    name: str
    """Name of the person."""

    incomes: list[Income] = field(default_factory=list, init=False, repr=False)
    """Incomes associated to the person."""

    expenses: list[Expense] = field(default_factory=list, init=False, repr=False)
    """Expenses associated to the person."""

    def total_incomes(self) -> float:
        """Calculates the total incomes of the person.

        Returns:
            total_incomes: Sum of all income shares.
        """
        return sum(i.share() for i in self.incomes)

    def total_expenses(self) -> float:
        """Calculates the total expenses of the person.

        Returns:
            total_expenses: Sum of all expense shares.
        """
        return sum(e.share() for e in self.expenses)

    def profits(self) -> float:
        """Calculates the profits of the person.

        Returns:
            profits: Total incomes minus total expenses.
        """
        return self.total_incomes() - self.total_expenses()

    def total_shared_incomes(self) -> float:
        """Calculates the total share of the incomes shared with other persons.

        Returns:
            total_shared_incomes: Sum of shared income shares.
        """
        return sum(i.share() for i in self.incomes if len(i.persons) > 1)

    def total_shared_expenses(self) -> float:
        """Calculates the total share of the expenses shared with other persons.

        Returns:
            total_shared_expenses: Sum of shared expense shares.
        """
        return sum(e.share() for e in self.expenses if len(e.persons) > 1)


@dataclass
class _Transaction:
    name: str
    """Name of the transaction."""

    amount: float
    """Amount of the transaction."""

    persons: list[Person] = field(default_factory=list, init=False, repr=False)
    """Persons associated to the transaction."""

    def share(self) -> float:
        """Calculates the share of one person of the transaction.

        If only one person is associated to the transaction, the share is the total amount.
        If several persons are associated to the transaction, the share is the total amount
        divided by the number of person associated to the transaction.

        Returns:
            share: Share of one person of the transaction.

        Raises:
            ValueError: If the transaction is not allocated.
        """
        if len(self.persons) < 1:
            msg = f'{self.__class__.__name__} "{self}" unallocated.'
            raise ValueError(msg)
        return self.amount / len(self.persons)


@dataclass
class Income(_Transaction):
    """Income to manage."""


@dataclass
class Expense(_Transaction):
    """Expense to manage."""
