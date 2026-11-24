from pathlib import Path
from GenerateTestData import employee_data, employee_leave_data, timeandattendance_data, employee_expense_data
import pandas as pd
import os

# test 1
def test_csv_output_filename():
    # Action
    employee_data()

    expected_file = Path("employee_test_data.csv")
    
    assert expected_file.exists()
    os.remove(expected_file)  # Clean up after test

# test 2
def test_employee_data_records_count():
   
    # Action
    df = employee_data(n=20)
    output_file = Path("employee_test_data.csv")
    file_df = pd.read_csv(output_file)

    # Assert
    assert len(df) == 20
    assert len(file_df) == 20
    os.remove("employee_test_data.csv")  # Clean up after test  

# test 3
def test_employee_data_columns():
    # Action
    df = employee_data(n=10)
    output_file = Path("employee_test_data.csv")
    file_df = pd.read_csv(output_file)

    # Assert
    expected_columns = ["EmployeeID", "FirstName", "LastName", "Address", "Suburb", "State", "PostCode", "Email", "EmploymentType", "Department", "Role"]
    assert list(df.columns) == expected_columns
    assert list(file_df.columns) == expected_columns
    os.remove("employee_test_data.csv")  # Clean up after test   

#test 4
def test_timeandattendance_file_exists():
    # Action
    timeandattendance_data()

    expected_file = Path("timeandattendance_test_data.csv")
    # Assert
    assert expected_file.exists()
    os.remove(expected_file)  # Clean up after test

# test 5
def test_timeandattendance_data_columns():
    # Action
    df = timeandattendance_data()
    output_file = Path("timeandattendance_test_data.csv")
    file_df = pd.read_csv(output_file)

    # Assert
    expected_columns = ["EmployeeID", "Date", "ClockIn", "ClockOut"]
    assert list(df.columns) == expected_columns
    assert list(file_df.columns) == expected_columns
    os.remove("timeandattendance_test_data.csv")  # Clean up after test
    os.remove("employee_test_data.csv")

# test 6
def test_expense_data_file_exists():
    # Action
    employee_expense_data(n=10)

    expected_file = Path("expenses_test_data.csv")
    # Assert
    assert expected_file.exists()
    os.remove(expected_file)  # Clean up after test
    os.remove("employee_test_data.csv")

 #test 7
 # test_expense_data_columns
def test_expense_data_columns():
    # Action
    df = employee_expense_data(n=10)
    output_file = Path("expenses_test_data.csv")
    file_df = pd.read_csv(output_file)

    # Assert
    expected_columns = [ "ClaimID", "EmployeeID", "Claim Date", "Claim Category", "Description", "Amount", "GST", "Net Amount",  "Status"]
    assert list(df.columns) == expected_columns
    assert list(file_df.columns) == expected_columns
    os.remove("expenses_test_data.csv")  # Clean up after test
    os.remove("employee_test_data.csv")  

# test 8
def test_leave_data_file_exists():
    # Action
    employee_leave_data(n=10)

    expected_file = Path("leave_test_data.csv")
    # Assert
    assert expected_file.exists()
    os.remove(expected_file)  # Clean up after test
    os.remove("employee_test_data.csv")
    