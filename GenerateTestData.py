from faker import Faker
import pandas as pd 
import numpy as np
import re
import random 
from datetime import datetime, date, timedelta 
from unidecode import unidecode
import holidays

"""
Program      : GenerateTestData.py
Description  : Synthetic HR test data generator
Author       : Ben Goh
Version      : 1.0.0
Date         : 9 November 2026

Purpose:
    Generate synthetic employee, attendance,
    expense and leave data for software testing.
"""


def employee_data(n=50):
# Generate a DataFrame with n rows of employee data, including realistic Australian addresses and postcodes.    

    fake = Faker(["en_AU", "vi_VN", "it_IT", "en_IN", "el_GR"])
    # postcode lookup table for Australian states and territories
    POSTCODE_RANGES = {
        "NSW": [(2000, 2599), (2619, 2899), (2921, 2999)],
        "ACT": [(2600, 2618), (2900, 2920)],
        "VIC": [(3000, 3999)],
        "QLD": [(4000, 4999)],
        "SA":  [(5000, 5799)],
        "WA":  [(6000, 6797)],
        "TAS": [(7000, 7799)],
        "NT":  [(800, 899)],
    }

    
    def au_postcode(state):
        # randomly select a postcode range for the given state and generate a postcode within that range
        lo, hi = random.choice(POSTCODE_RANGES[state])
        return f"{random.randint(lo, hi):04d}"
    
    # Employment types with weights for random selection
    ET = ["FT", "PT", "CS"]

    # Departments and roles for random selection
    structure = {
            "IT": ["Team Lead", "Analyst", "Developer"],
            "HR": ["Manager", "Administrator", "Coordinator"], 
            "Finance": ["Manager", "Administrtor", "Analyst"], 
            "Marketing": ["Team Lead", "Consultant", "Designer"],
            "Customer Service": ["Manager", "Consultant", "Coordinator"] 
        }
    departments = list(structure.keys())

    rows = [] 

    for _ in range(n): 

        employee_id = fake.unique.random_int(min=10000, max=90000)
        first = unidecode(fake.first_name())
        last = unidecode(fake.last_name())

        # tidying up the address to extract suburb, state, and postcode
        addr = fake["en_AU"].address()
        line1, last = addr.split("\n")[0], addr.split("\n")[-1]
        m = re.match(r"^(?P<suburb>.+?),\s+(?P<state>[A-Z]{2,3},)\s+(?P<postcode>\d{4})$", last)
        suburb, state, postcode = m["suburb"], m["state"], m["postcode"]
        state = state.split(',')[0]  # Remove the trailing comma from the state
        postcode = au_postcode(state)  # Generate a postcode based on the state

        email = f"{first}.{last}@example.com".lower().replace(" ", "")
        employment_type = random.choices(ET, weights=[75, 30, 5])[0]
        department = random.choices(departments, weights=[50, 20, 20, 5, 5])[0]
        role = random.choices(structure[department], weights=[10, 30, 60])[0]

        # building the employee record and appending it to the rows list
        rows.append({ 
            "EmployeeID" : employee_id, 
            "FirstName" : first, 
            "LastName" : last, 
            "Address": line1, 
            "Suburb": suburb, 
            "State": state, 
            "PostCode": postcode, 
            "Email": email,
            "EmploymentType" : employment_type,
            "Department" : department,
            "Role" : role
        }) 
    
    employee = pd.DataFrame(rows)
    employee.to_csv("employee_test_data.csv", index=False)
    return employee

def timeandattendance_data():
#  Generate time and attendance data for n employees, for 2 weeks, with realistic clock-in and clock-out times, 
#  and a chance of missing records based on employment type.   

    fake = Faker()
    staff = employee_data()
    # Chance (%) that an attendance record is created, per employment type
    attend_pct = {"FT": 90, "PT": 70, "CS": 30}

    def should_record(emp_type):
        return random.randint(1, 100) <= attend_pct[emp_type]

    def random_time_near(base_dt, window_minutes=5):
        return base_dt + timedelta(seconds=random.randint(0, window_minutes * 60))


    period = random.randint(14,60) #a random range of days to generate attendance data
    td = date.today() - timedelta(days = period)
    startdate = td - timedelta(days=td.weekday())  # Start from the most recent Monday
    enddate = startdate + timedelta(days = 11)
    workdays = pd.date_range(start=startdate, end=enddate, freq='B')  # Business days only
    
    rows = []

    for day in  workdays: 

        for emp in staff.itertuples():
            if not should_record(emp.EmploymentType): 
                continue
            employeeId = emp.EmployeeID        
            starttime = random_time_near(day.to_pydatetime().replace(hour=8, minute=45)) 
            endtime = starttime + timedelta(hours=7, minutes= 47, seconds=random.randint(0, 600))
            
            rows.append({
                "EmployeeID" : employeeId,
                "Date" : day,
                "ClockIn": starttime.time(), 
                "ClockOut": endtime.time() 
            })
    
    timeandattendance = pd.DataFrame(rows)
    timeandattendance.to_csv("timeandattendance_test_data.csv", index=False)
    return timeandattendance

def employee_expense_data(n=200):
    # Generate expense data for employees, with realistic expense categories 
    # and amounts, and a chance of missing records based on employment type.   

    
    fake = Faker(["en_AU", "vi_VN", "it_IT", "en_IN", "el_GR"])
    staff = employee_data()
    numberofclaims = n

    # Chance (%) that an expense record is created, per employment type
    expense_pct = {"FT": 80, "PT": 60, "CS": 10}

    def should_record(emp_type):
        return random.randint(1, 100) <= expense_pct[emp_type]

    categories = {
    # category: (min $, max $, GST applies?, description templates)
    "Travel":        (50, 1500, True,  ["Flight to {city}", "Taxi to {city} client site", "Hotel stay in {city}"]),
    "Meals":         (15, 150,  True,  ["Lunch with client", "Team dinner", "Working lunch in {city}"]),
    "Parking":       (5,  60,   True,  ["Parking at {city} office", "Airport parking"]),
    "Office Supplies": (10, 300, True, ["Printer paper and toner", "Stationery order", "Desk accessories"]),
    "Training":      (100, 2500, True, ["Online course fee", "Conference registration", "Workshop in {city}"]),
    "Mileage":       (20, 400,  False, ["Mileage claim: {city} client visit", "Mileage: site inspection"]),
    }

# Weight so everyday categories appear more often
    cat_names = list(categories)
    cat_weights = [15, 35, 20, 15, 5, 10]

    status_options = ["Approved", "Pending", "Rejected"]
    status_weights = [70, 20, 10]

   # set a random range of days to generate expense data, starting from the most recent Monday
    period = random.randint(15,31) #a random range of days to generate expense  data
    td = date.today() - timedelta(days = period)
    startdate = td - timedelta(days=td.weekday())  # Start from the most recent Monday
    enddate = startdate + timedelta(days = 11)
    claimdates = pd.date_range(start=startdate, end=enddate, freq='B')  # Business days only
    GST_RATE = 0.10
     
    rows = []
    for  _   in range(numberofclaims):
        
        emp = staff.sample(1).iloc[0]
        if not should_record(emp.EmploymentType):
            continue
        category = random.choices(cat_names, weights=cat_weights)[0]
        min_amt, max_amt, gst_applies, templates = categories[category]

        # Generate a unique ClaimID using the first three letters of the category and a random number
        claimid = f"{category[0:3].upper()}{fake.unique.random_int(min=10000, max=90000)}"

        # Generate a random amount within the specified range, calculate GST and net amount
        amount = round(random.uniform(min_amt, max_amt), 2) 
        gst = round(amount * GST_RATE, 2) if gst_applies else 0.0
        net = round(amount - gst, 2)
        description_template = random.choice(templates)
        description = description_template.format(city=fake['en_AU'].city())
        claim_date = random.choice(claimdates)
        status = random.choices(status_options, weights=status_weights)[0]

        rows.append({
            "ClaimID": claimid,
            "EmployeeID": emp.EmployeeID,
            "Claim Date": claim_date,
            "Claim Category": category,
            "Description": description,
            "Amount": amount,
            "GST": gst,
            "Net Amount": net,
            "Status": status
        })
        
    expenses = pd.DataFrame(rows)
    expenses.to_csv("expenses_test_data.csv", index=False)
    return expenses



def employee_leave_data(n=50):
    # Generate leave data for employees, with realistic leave types and durations, and a chance of missing records based on employment type.   
    today = date.today()
    STATES = ["NSW", "VIC", "QLD", "SA", "WA", "TAS", "ACT", "NT"]

    # dict of {date: holiday name} per state, covering this year and next
    ph = {s: holidays.Australia(subdiv=s, years=[today.year, today.year + 1]) for s in STATES}

    # NumPy needs the dates as a datetime64 array
    ph_np = {s: np.array(sorted(ph[s]), dtype="datetime64[D]") for s in STATES}

    # leave types with offsets, durations, weights, and status probabilities
    leave_types = {
    #  type       (start offset in days from today, working days requested, type weight)
    "Annual":  {"offset": (7, 120),    "days": (1, 15), "weight": 50,
                "status": (["Approved", "Pending", "Rejected", "Cancelled"], [50, 40, 5, 5])},
    "Sick":    {"offset": (-120, -5),  "days": (1, 3),  "weight": 35,
                "status": (["Approved", "Pending", "Rejected", "Cancelled"], [85, 5, 5, 5])},
    "Carer's": {"offset": (7, 90),     "days": (1, 3),  "weight": 15,
                "status": (["Approved", "Pending", "Rejected", "Cancelled"], [50, 40, 5, 5])},
                }


    def build_leave(emp_id, state):
        # Randomly select a leave type, generate a start and end date, calculate the number of leave days deducted, and determine the status and lodged date.
        cfg_name = random.choices(list(leave_types),
                              weights=[c["weight"] for c in leave_types.values()])[0]
        cfg = leave_types[cfg_name]
        hol = ph_np[state]

        # Generate a unique leave ID using the first three letters of the leave type
        # and a random number
        leaveid = f"{cfg_name[0:3].upper()}{random.randint(10000, 99999)}"  # Unique leave ID
     
        # Start: random date, rolled forward to a working day (not a weekend or holiday)
        raw_start = today + timedelta(days=random.randint(*cfg["offset"]))
        start = np.busday_offset(np.datetime64(raw_start), 0, roll="forward", holidays=hol)

        # End: N weekdays later, then rolled back if it lands on a public holiday
        n = random.randint(*cfg["days"])
        end = np.busday_offset(start, n - 1, roll="forward")             # ignores holidays
        end = np.busday_offset(end, 0, roll="backward", holidays=hol)    # never ends on a holiday

        leave_days = int(np.busday_count(start, end + 1, holidays=hol))  # excludes weekends and holidays

        start_d, end_d = pd.Timestamp(start).date(), pd.Timestamp(end).date()

        status = random.choices(*cfg["status"])[0]

        # Future leave is lodged before it starts, past sick leave is lodged on or after the first day
        if start_d > today:
            lodged = today - timedelta(days=random.randint(0, 30))
        else:
            lodged = start_d + timedelta(days=random.randint(0, 3))

        return {
            "LeaveID": leaveid,
            "EmployeeID": emp_id,
            "State": state,
            "LeaveType": cfg_name,
            "StartDate": start_d,
            "EndDate": end_d,
            "LeaveDaysDeducted": leave_days,
            "Status": status,
            "LodgedDate": lodged
            }
    
    # generating employee leave data for n requests
    n_requests = n
    staff = employee_data()

    # building leave data for employee, 
    # randomly selecting an employee and their state, 
    # and generating leave data using the build_leave function
    rows = []
    for _ in range(n_requests):
        emp = staff.sample(1).iloc[0]
        rows.append(build_leave(emp["EmployeeID"], emp["State"]))

    leave_data = pd.DataFrame(rows)
    leave_data.to_csv("leave_test_data.csv", index=False)
    return leave_data
    