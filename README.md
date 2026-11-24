# TestDataGenerator

A Python-based synthetic test data generator designed to support functional testing, application data imports and test automation.

The project generates realistic, related employee and HR transaction data in CSV format. It is intended to help software testers, business analysts and test automation engineers create sample datasets without relying on genuine employee information.

## Features

The generator currently supports four types of test data:

1. Employee master data
2. Time and attendance records
3. Employee expense claims
4. Employee leave records

### 1. Employee Data

Generates synthetic employee profiles with a default of 50 employees.

Features include:

- Fictional employee names drawn from different cultural and national backgrounds, reflecting Australia's multicultural workforce.
- Synthetically generated Australian residential addresses.
- Australian states, territories, suburbs and postcodes.
- Employment types: Full-time (FT), Part-time (PT) and Casual (CS).
- Department and role assignments, with roles associated with their respective departments.
- Unique employee identifiers.
- Synthetic email addresses.

All employee names and residential addresses are fictional. No genuine employee personal information is used.

**Method:**

```python
employee_data(n=50)
```

Generates a standalone employee CSV file.

### 2. Time and Attendance Data

Generates time and attendance records covering from randomly two weeks to up to 30 business days.

Features include:

- Randomly generated clock-in and clock-out times.
- Attendance records associated with employee IDs.
- Different attendance patterns based on employment type.
- Random attendance selection, allowing casual employees to have days without attendance records.

The number of attendance records varies depending on the random selection of employees and their employment types.

Two related CSV files are generated:

| CSV file | Description |
|---|---|
| Employees | Employee master data |
| Time and Attendance | Employee attendance records |

**Method:**

```python
timeandattendance()
```

### 3. Employee Expense Claims

Generates synthetic employee expense claim records.

Features include:

- Multiple expense categories, such as travel, meals, parking, office supplies, training and mileage.
- Randomly generated claim amounts and descriptions.
- GST calculations where applicable.
- Claim statuses, including Approved, Pending and Rejected.
- Expense records associated with employee IDs.
- Different claim probabilities based on employment type.

Expense claims are primarily generated for full-time and part-time employees. Casual employees have a much lower chance of submitting claims, approximately 10%.

Two related CSV files are generated:

| CSV file | Description |
|---|---|
| Employees | Employee master data |
| Expenses | Employee expense claim records |

**Method:**

```python
employee_expense_data(n=200)
```

The default parameter generates up to 200 expense claim attempts. The actual number of records may be lower because of the random selection rules.

### 4. Employee Leave Records

Generates synthetic employee leave records using randomly selected leave categories, including:

- Annual leave
- Sick leave
- Carer's leave

Features include:

- Leave records associated with employee IDs.
- Randomly generated leave periods.
- Working-day calculations that exclude weekends.
- Australian state and territory public holidays.

Public holiday information is obtained through the Python `holidays` package, allowing the generator to take the relevant state or territory holiday calendar into consideration.

Two related CSV files are generated:

| CSV file | Description |
|---|---|
| Employees | Employee master data |
| Leave  | Employee leave records |


**Method:**

```python
employee_leave_data(n=50)
```

## Related CSV Data Generation

An important feature of this project is the generation of related datasets rather than isolated random records.

For time and attendance, expense claims, and leaves the generator produces separate employee and transaction CSV files. Employee IDs provide the link between the master employee records and their associated transactions.

This helps maintain data relationships and provides a consistent reference when importing the data into an application.

## Using the Generated Data

The generated CSV files can be used in two main ways.

### Application Data Import

Business analysts and software testers can use the generated CSV files to populate an HR application or other business system.

The user is responsible for mapping the CSV column names to the corresponding fields in the target application before importing the data.

### Data-Driven Test Automation

The CSV files can also be used as external test data for automated testing.

For example, an automation framework can read employee, attendance, expense or leave records from CSV files and use the values as inputs when executing test scenarios.

This separates test data from automation scripts and supports repeatable, data-driven testing.

## Installation

### Prerequisites

- Python 3
- pip (Python package installer)

Clone or download this repository:

```bash
git clone https://github.com/bgoh29/TestDataGenerator.git
```

Navigate to the project directory:

```bash
cd TestDataGenerator
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Dependencies

The project uses the following third-party Python packages:

- Faker – synthetic data generation.
- Pandas – data manipulation and CSV file generation.
- Unidecode – normalisation of generated names.
- Holidays – Australian public holiday information.

Python standard library modules such as `random`, `re` and `datetime` do not require separate installation.

## Running the Generator

The generation methods can be called from the command line without writing a separate Python program.

Run the commands from the project directory.

**Generate employee data:**

```bash
python -c "from GenerateTestData import employee_data; employee_data()"
```

**Generate time and attendance data:**

```bash
python -c "from GenerateTestData import timeandattendance; timeandattendance_data()"
```

**Generate expense claim data:**

```bash
python -c "from GenerateTestData import employee_expense_data; employee_expense_data()"
```

**Generate employee leave data:**

```bash
python -c "from GenerateTestData import employee_leave_data; employee_leave_data()"
```

To use a different number of records where supported, pass the desired value to the relevant method.

For example:

```bash
python -c "from GenerateTestData import employee_data; employee_data(100)"
```

The generated CSV files are saved in the program's working directory.

## Running Automated Tests

The project includes automated tests using Pytest.

Install Pytest if it is not already installed:

```bash
pip install pytest
```

Run the test suite from the project root:

```bash
python -m pytest -v
```

## Project Purpose

TestDataGenerator was developed as a practical tool to support software testing activities.

By providing synthetic employee and HR transaction data, it helps testers and analysts:

- Prepare realistic test datasets.
- Validate data import and field mapping.
- Test relationships between employee and transaction records.
- Create reusable data-driven automation inputs.
- Exercise different employment types and HR business scenarios.
- Avoid using genuine employee personal information in test environments.

The project is intended for testing and demonstration purposes. Generated data is synthetic and should not be treated as genuine employee information or an authoritative representation of Australian employment entitlements.
