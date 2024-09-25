"""Budget manager module."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from rilog import logger

from budgee.models import ExpenseModel, IncomeModel, ManagerModel, PersonModel
from budgee.structures import Expense, Income, Person


@dataclass
class Manager:
    """Budget manager."""

    persons: dict[str, Person] = field(default_factory=dict, kw_only=True)
    """Persons to manage."""

    incomes: dict[str, Income] = field(default_factory=dict, kw_only=True)
    """Incomes to manage."""

    expenses: dict[str, Expense] = field(default_factory=dict, kw_only=True)
    """Expenses to manage."""

    def create_person(self, name: str) -> None:
        """Creates a new person to manage.

        Args:
            name: Name of the person.
        """
        self.persons[name] = Person(name)

    def create_income(self, name: str, amount: float) -> None:
        """Creates a new income to manage.

        Args:
            name: Name of the income.
            amount: Amount of the income.
        """
        self.incomes[name] = Income(name, amount)

    def create_expense(self, name: str, amount: float) -> None:
        """Creates a new expense to manage.

        Args:
            name: Name of the expense.
            amount: Amount of the expense.
        """
        self.expenses[name] = Expense(name, amount)

    def delete_person(self, name: str) -> None:
        """Deletes a person from the manager.

        Args:
            name: Name of the person to delete.
        """
        person = self.persons[name]
        for transaction in person.incomes + person.expenses:
            transaction.persons.remove(person)
        del self.persons[name]

    def delete_income(self, name: str) -> None:
        """Deletes an income from the manager.

        Args:
            name: Name of the income to delete.
        """
        income = self.incomes[name]
        for person in income.persons:
            person.incomes.remove(income)
        del self.incomes[name]

    def delete_expense(self, name: str) -> None:
        """Deletes an expense from the manager.

        Args:
            name: Name of the expense to delete.
        """
        expense = self.expenses[name]
        for person in expense.persons:
            person.expenses.remove(expense)
        del self.expenses[name]

    def _summarize_persons(self) -> None:
        if not self.persons:
            return

        logger.log("Persons:")
        logger.set_prefix("    • ")
        for person in self.persons.values():
            logger.log(person.name)
        logger.remove_prefix()

    def _summarize_incomes(self) -> None:
        if not self.incomes:
            return

        logger.log("Incomes:")
        logger.set_prefix("    + ")
        for income in self.incomes.values():
            logger.log(f"{income.name}: {income.amount}")
        logger.remove_prefix()

    def _summarize_expenses(self) -> None:
        if not self.expenses:
            return

        logger.log("Expenses:")
        logger.set_prefix("    - ")
        for expense in self.expenses.values():
            logger.log(f"{expense.name}: {expense.amount}")
        logger.remove_prefix()

    def summarize(self) -> None:
        """Summarizes the manager by displaying all managed persons, incomes, and expenses."""
        logger.log("[b blue]------- Summary -------")
        self._summarize_persons()
        self._summarize_incomes()
        self._summarize_expenses()

    def display_person(self, name: str) -> None:
        """Displays the transactions of a person.

        Args:
            name: Name of the person to summarize.
        """
        person = self.persons[name]
        logger.log(f"[b blue]------- {person.name} -------")
        logger.log("Incomes:")
        logger.set_prefix("    + ")
        for income in person.incomes:
            logger.log(f"{income.name}: {income.share()}")
        logger.remove_prefix()
        logger.log("Expenses:")
        logger.set_prefix("    - ")
        for expense in person.expenses:
            logger.log(f"{expense.name}: {expense.share()}")
        logger.remove_prefix()
        logger.log(f"Profits: {person.profits()}")
        logger.log(f"Total Incomes: {person.total_incomes()}")
        logger.log(f"Total Expenses: {person.total_expenses()}")
        logger.log(f"Total Shared Incomes: {person.total_shared_incomes()}")
        logger.log(f"Total Shared Expenses: {person.total_shared_expenses()}")

    def _to_model(self) -> ManagerModel:
        person_models = [
            PersonModel(
                name=person.name,
                incomes=[income.name for income in person.incomes],
                expenses=[expense.name for expense in person.expenses],
            )
            for person in self.persons.values()
        ]
        income_models = [
            IncomeModel(
                name=income.name,
                amount=income.amount,
                persons=[person.name for person in income.persons],
            )
            for income in self.incomes.values()
        ]
        expense_models = [
            ExpenseModel(
                name=expense.name,
                amount=expense.amount,
                persons=[person.name for person in expense.persons],
            )
            for expense in self.expenses.values()
        ]
        return ManagerModel(
            persons=person_models,
            incomes=income_models,
            expenses=expense_models,
        )

    def save(self, file_path: Path | str) -> None:
        """Exports the manager to a JSON file.

        Args:
            file_path: Path to the JSON file.
        """
        model = self._to_model()
        if not isinstance(file_path, Path):
            file_path = Path(file_path)
        with file_path.open(mode="w", encoding="utf-8") as file:
            json.dump(model.model_dump(), file, indent=4)

    @classmethod
    def _from_model(cls, model: ManagerModel) -> Manager:
        manager = cls()

        for person_data in model.persons:
            person = Person(person_data.name)
            manager.persons[person.name] = person

        for income_data in model.incomes:
            income = Income(income_data.name, income_data.amount)
            manager.incomes[income.name] = income

        for expense_data in model.expenses:
            expense = Expense(expense_data.name, expense_data.amount)
            manager.expenses[expense.name] = expense

        for person_data in model.persons:
            person = manager.persons[person_data.name]
            person.incomes = [manager.incomes[income_name] for income_name in person_data.incomes]
            person.expenses = [manager.expenses[expense_name] for expense_name in person_data.expenses]

        for income_data in model.incomes:
            income = manager.incomes[income_data.name]
            income.persons = [manager.persons[person_name] for person_name in income_data.persons]

        for expense_data in model.expenses:
            expense = manager.expenses[expense_data.name]
            expense.persons = [manager.persons[person_name] for person_name in expense_data.persons]

        return manager

    @classmethod
    def load(cls, file_path: Path | str) -> Manager:
        """Imports a manager from a JSON file.

        Args:
            file_path: Path to the JSON file.

        Returns:
            manager: Imported manager.
        """
        if not isinstance(file_path, Path):
            file_path = Path(file_path)
        with file_path.open(encoding="utf-8") as file:
            model = ManagerModel(**json.load(file))
        return cls._from_model(model)
