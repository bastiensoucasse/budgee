"""Data models module."""

from pydantic import BaseModel


class PersonModel(BaseModel):
    """Model representing a person."""

    name: str
    incomes: list[str]
    expenses: list[str]


class _TransactionModel(BaseModel):
    name: str
    amount: float
    persons: list[str]


class IncomeModel(_TransactionModel):
    """Model representing an income."""


class ExpenseModel(_TransactionModel):
    """Model representing an expense."""


class ManagerModel(BaseModel):
    """Model representing a manager."""

    persons: list[PersonModel]
    incomes: list[IncomeModel]
    expenses: list[ExpenseModel]
