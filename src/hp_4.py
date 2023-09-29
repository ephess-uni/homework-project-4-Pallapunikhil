# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict



def reformat_dates(old_dates):
    dates = []
    for date_str in old_dates:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        formatted_date = date_obj.strftime('%d %b %Y')
        dates.append(formatted_date)
    return dates


def date_range(start, n):
    if not isinstance(start, str):
        raise TypeError("start should be a string")
    if not isinstance(n, int):
        raise TypeError("n should be an integer")
    date = datetime.strptime(start, '%Y-%m-%d')
    date_list = [date + timedelta(days=i) for i in range(n)]
    return date_list


def add_date_range(values, start_date):
    obj = date_range(start_date, len(values))
    result = [(date, value) for date, value in zip(obj, values)]
    return result


def fees_report(infile, outfile):
    late_fees = defaultdict(float)
    all_patrons = set() 
    
    with open(infile, 'r') as file:
        reader = DictReader(file)
        for row in reader:
            checkout_date = datetime.strptime(row['date_checkout'], '%m/%d/%Y')
            due_date = datetime.strptime(row['date_due'], '%m/%d/%Y')
            returned_date = datetime.strptime(row['date_returned'], '%m/%d/%Y')  # Adjust date format
            
            if returned_date > due_date:
                days_late = (returned_date - due_date).days
                late_fees[row['patron_id']] += days_late * 0.25
            
            all_patrons.add(row['patron_id'])  
    
    for patron_id in all_patrons:
        if patron_id not in late_fees:
            late_fees[patron_id] = 0.0
    
    with open(outfile, 'w', newline='') as file:
        writer = DictWriter(file, fieldnames=['patron_id', 'late_fees'])
        writer.writeheader()
        for patron_id, fee in late_fees.items():
            writer.writerow({'patron_id': patron_id, 'late_fees': f'{fee:.2f}'})


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
