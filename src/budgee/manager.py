"""Person/transaction management."""

from json import dump, load
from pathlib import Path

from pydantic import BaseModel, Field

from budgee.logger import logger
from budgee.models import Expense, Income, Person, Transaction
from budgee.utils import slugify


class Manager(BaseModel):
    """Person/transaction manager."""

    people: dict[str, Person] = Field(default_factory=dict)
    """People to manage."""

    transactions: dict[str, Transaction] = Field(default_factory=dict)
    """Transactions to manage."""

    def _get_person(self, name: str) -> Person | None:
        return self.people.get(slugify(name))

    def _get_transaction(self, name: str) -> Transaction | None:
        return self.transactions.get(slugify(name))

    def _find_person(self, name: str) -> Person:
        person = self._get_person(name)
        if not person:
            msg = f'Person "{name}" does not exist.'
            raise ValueError(msg)
        return person

    def _find_transaction(self, name: str) -> Transaction:
        transaction = self._get_transaction(name)
        if not transaction:
            msg = f'Transaction "{name}" does not exist.'
            raise ValueError(msg)
        return transaction

    def _check_person_doesnt_exist(self, name: str) -> None:
        if person := self._get_person(name):
            msg = f'Person "{person.name}" already exists.'
            raise ValueError(msg)

    def _check_transaction_doesnt_exist(self, name: str) -> None:
        if transaction := self._get_transaction(name):
            msg = f'Transaction "{transaction.name}" already exists.'
            raise ValueError(msg)

    def create_person(self, name: str) -> None:
        """Creates a new person to manage.

        Args:
            name: Name of the person.
        """
        self._check_person_doesnt_exist(name)
        person = Person(name)
        self.people[person.id()] = person

    def _create_transaction(
        self,
        name: str,
        value: float,
        transaction_type: type[Transaction],
        *,
        category: str | None = None,
    ) -> None:
        self._check_transaction_doesnt_exist(name)
        transaction = transaction_type(name, value, Transaction.Category(category) if category else None)
        self.transactions[transaction.id()] = transaction

    def create_income(self, name: str, value: float, *, category: str | None = None) -> None:
        """Creates a new income to manage.

        Args:
            name: Name of the income.
            value: Value of the income.
            category: Category of the income.
        """
        self._create_transaction(name, value, Income, category=category)

    def create_expense(self, name: str, value: float, *, category: str | None = None) -> None:
        """Creates a new expense to manage.

        Args:
            name: Name of the expense.
            value: Value of the expense.
            category: Category of the expense.
        """
        self._create_transaction(name, value, Expense, category=category)

    def delete_person(self, name: str) -> None:
        """Deletes a person from the manager.

        Args:
            name: Name of the person to delete.
        """
        person = self._find_person(name)
        person_id = person.id()
        for transaction_id in person.transactions:
            self.transactions[transaction_id].persons.remove(person_id)
        del self.people[person_id]

    def delete_transaction(self, name: str) -> None:
        """Deletes a transaction from the manager.

        Args:
            name: Name of the transaction to delete.
        """
        transaction = self._find_transaction(name)
        transaction_id = transaction.id()
        for person_id in transaction.persons:
            self.people[person_id].transactions.remove(transaction_id)
        del self.transactions[transaction_id]

    def _update_person_name(self, person: Person, new_name: str) -> None:
        self._check_person_doesnt_exist(new_name)
        person_id = person.id()
        person.name = new_name
        new_person_id = person.id()
        for transaction_id in person.transactions:
            transaction = self.transactions[transaction_id]
            transaction.persons.remove(person_id)
            transaction.persons.append(new_person_id)
        del self.people[person_id]
        self.people[new_person_id] = person

    def _update_transaction_name(self, transaction: Transaction, new_name: str) -> None:
        self._check_transaction_doesnt_exist(new_name)
        transaction_id = transaction.id()
        transaction.name = new_name
        new_transaction_id = transaction.id()
        for person_id in transaction.persons:
            person = self.people[person_id]
            person.transactions.remove(transaction_id)
            person.transactions.append(new_transaction_id)
        del self.transactions[transaction_id]
        self.transactions[new_transaction_id] = transaction

    def update_person(self, name: str, *, new_name: str | None = None) -> None:
        """Updates a person with new properties.

        Args:
            name: Current name of the person to update.
            new_name: New name of the person.
        """
        person = self._find_person(name)
        if new_name:
            self._update_person_name(person, new_name)

    def update_transaction(
        self,
        name: str,
        *,
        new_name: str | None = None,
        new_value: float | None = None,
        new_category: str | None = None,
    ) -> None:
        """Updates a transaction with new properties.

        Args:
            name: Current name of the transaction to update.
            new_name: New name of the transaction.
            new_value: New value of the transaction.
            new_category: New category of the transaction.
        """
        transaction = self._find_transaction(name)
        if new_name:
            self._update_transaction_name(transaction, new_name)
        if new_value:
            transaction.value = new_value
        if new_category:
            transaction.category = Transaction.Category(new_category)

    def save(self, context_file_path: Path | str) -> None:
        """Saves the current manager context to a JSON file.

        Args:
            context_file_path: Path to the context file to create.
        """
        if not isinstance(context_file_path, Path):
            context_file_path = Path(context_file_path)
        with context_file_path.open(mode="w", encoding="utf-8") as context_file:
            dump(self.model_dump(), context_file, indent=4)
        logger.log(f'Manager context saved successfully to "{context_file_path}".')

    @staticmethod
    def load(context_file_path: Path | str) -> "Manager":
        """Loads a manager context from a JSON file.

        Args:
            context_file_path: Path to the context file to load.

        Returns:
            manager: Manager loaded from the context file.
        """
        if not isinstance(context_file_path, Path):
            context_file_path = Path(context_file_path)
        with context_file_path.open(encoding="utf8") as context_file:
            context = load(context_file)
        manager = Manager(**context)
        logger.log(f'Manager context loaded successfully from "{context_file_path}".')
        return manager
