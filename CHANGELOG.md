# Changelog

## Unreleased

**Added**

- Introduced a manager for people and transactions
  with methods for creating, updating, and deleting people and transactions,
  along with saving/loading the manager from/to a context JSON file.
- Introduced base models for persons, transactions, incomes, and expenses,
  with transaction categories and a transaction value computing method.
- Introduced an enhanced logger with progress tracking with methods for logging messages and warnings,
  setting/removing log prefixes, and tracking progress of data iteration with a progress bar.
- Implemented a slugify utility to generate identifiers.
