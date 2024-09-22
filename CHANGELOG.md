# Changelog

## Unreleased

**Added**

- Introduced a command-line interface (CLI) defined as default entry point
  with version display and context loading options.
- Introduced a manager for people and transactions
  with methods for creating, updating, and deleting people and transactions,
  summarizing the current context (people and transactions),
  and saving/loading the manager from/to a context JSON file.
- Introduced base models for persons, transactions, incomes, and expenses,
  with transaction categories and a transaction value computing method.
- Introduced an enhanced logger with progress tracking with methods for logging messages and warnings,
  setting/removing log prefixes, and tracking progress of data iteration with a progress bar.
- Implemented a slugify utility to generate identifiers.
