# ICS499 Assignment 2

SQL data anonymization program for ICS 499.

The program reads a MySQL `.sql` export and creates a new `.sql` file with personal information replaced with fake data.

It anonymizes:

* names
* addresses
* emails
* phone numbers

## Tech

* Python 3
* Faker

Faker is the only dependency.

## Install

```bash
pip install Faker
```

or

```bash
pip install -r requirements.txt
```

## Run

```bash
python anonymize.py original.sql -o anonymized.sql
```

This reads `original.sql` and creates `anonymized.sql`.

## Files

`original.sql`

Sample SQL file used for testing.

`anonymize.py`

Main program that reads and anonymizes the SQL file.

`anonymized.sql`

Generated output from the program.

`verify.py`

Runs tests against the original and anonymized files.

`requirements.txt`

Python dependency list.

## How it works

The program first reads the CREATE TABLE statements so it knows the column names and their order.

This is also used for INSERT statements that do not include a column list.

The program looks at the column name first to decide if something might be PII.

Examples are columns ending in `name` or containing `email`, `phone`, or `address`.

It also checks the actual value before changing it so normal text does not get anonymized by accident.

For example, `venues.name` is skipped because the values are facility names and not people.

## Consistency

The same original value always gets the same replacement during the run.

Each value is normalized and stored in a dictionary after it is replaced.

A hash is also created using:

```text
salt + category + original value
```

The hash is used as the seed for Faker.

This makes the fake data consistent across different tables.

For example, if the same person appears in `players` and `away_trips`, they get the same fake name.

The salt is randomly created each time the program runs and is not saved.

Because of this, a new run can create different fake data and there is no saved reverse mapping.

## Format preservation

The program tries to preserve the format of the original data.

Examples:

* phone punctuation stays the same
* uppercase emails stay uppercase
* email plus tags are kept
* name suffixes like `Jr.` are kept
* NULL stays NULL
* IDs, dates, numbers, and SQL structure are not changed

The program also handles addresses stored in different ways.

For example:

```text
9142 Courtly Road
Woodbury
MN
55125
```

and

```text
9142 Courtly Road, Woodbury, MN 55125
```

use the same generated address pieces.

## Testing

The sample SQL file includes several test cases.

These include:

* repeated names across tables
* repeated emails and phone numbers
* different phone formats
* uppercase emails
* email plus tags
* name suffixes
* SQL apostrophe escaping
* NULL values
* INSERT statements without column lists
* facility names that should not be anonymized
* split and full address formats

Testing can be run with:

```bash
python verify.py
```

The verification script checks that:

* PII was changed
* repeated values stay consistent
* values stay in the correct columns
* non-PII text stays unchanged
* SQL structure stays unchanged
* IDs, numbers, dates, and NULL values stay unchanged
* split and full addresses map consistently

A successful run ends with:

```text
ALL TESTS PASSED
```

## Research

Data masking means hiding or replacing sensitive data so the real value is not exposed.

Anonymization means changing data so it can no longer reasonably be connected back to the original person.

Pseudonymization replaces identifying data with other values, but the data may still be linked back if a mapping or key exists.

Synthetic data is fake data created to look similar to real data without using the original values.

Hashing converts data into a fixed value using a one-way function. Hashes are useful for consistency but usually do not look realistic enough to directly replace names, emails, or addresses.

Tokenization replaces sensitive values with tokens and normally uses a separate mapping system to connect the token back to the original value.

This project uses a mix of hashing and synthetic data generation. The hash is used to consistently seed Faker, while Faker creates realistic replacement values.

## Design decisions

The project was intentionally kept small and only focuses on the four required PII categories.

The program edits string values inside INSERT statements instead of rewriting the entire SQL file.

Anything that is not replaced is copied directly from the original file.

`venues.name` is specifically skipped because those values are facility names and not people.

No mapping file is created.

## Known limitations

This is not a full SQL parser.

It is designed around normal MySQL dump style CREATE TABLE and INSERT statements.

The column detection rules are also based on common names such as `email`, `phone`, `address`, and columns ending in `name`.

Unusual schemas may need additional rules.

The program also only handles the four PII categories required for this assignment.
