import aiohttp
import asyncio
import csv
import os

API_URL = "http://127.0.0.1:5050/EmployeeManagement/bulk-record/"
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(CURRENT_DIR, "employees.csv")

async def send_employee_record(session, record):
    async with session.post(API_URL, json=record) as response:
        print(await response.text()) 

async def main():
    records = []
    
    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row["salary"] = float(row["salary"])  
            row["date_of_joining"] = row["date_of_joining"].strip() 
            records.append(row)
    
    async with aiohttp.ClientSession() as session:
        tasks = [send_employee_record(session, record) for record in records]
        await asyncio.gather(*tasks) 
asyncio.run(main()) 
