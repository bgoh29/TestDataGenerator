from faker import Faker
import pandas as pd 
import re
import random 
from datetime import datetime, date, timedelta 
from unidecode import unidecode


def employee_data(n=50):
#   Generate a DataFrame with n rows of employee data, including realistic Australian addresses and postcodes.    
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
        addr = fake["en_AU"].address()
        line1, last = addr.split("\n")[0], addr.split("\n")[-1]
        m = re.match(r"^(?P<suburb>.+?),\s+(?P<state>[A-Z]{2,3},)\s+(?P<postcode>\d{4})$", last)
        suburb, state, postcode = m["suburb"], m["state"], m["postcode"]
        state = state.split(',')
        first = unidecode(fake.first_name())
        last = unidecode(fake.last_name())
        email = f"{first}.{last}@example.com".lower().replace(" ", "")
        employment_type = random.choices(ET, weights=[75, 30, 5])[0]
        department = random.choices(departments, weights=[50, 20, 20, 5, 5])[0]
        role = random.choices(structure[department], weights=[10, 30, 60])[0]

        rows.append({ 
            "EmployeeID" :fake.unique.random_int(min=10000, max=90000), 
            "FirstName" : first, 
            "LastName" : last, 
            "Address": line1, 
            "Suburb": suburb, 
            "State": state[0], 
            "PostCode": au_postcode(state[0]), 
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


    period = random.randint(14,30) #a random range of days to generate attendance data
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
    # Generate expense data for n employees, with realistic expense categories 
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
    period = random.randint(15,30) #a random range of days to generate expense  data
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

