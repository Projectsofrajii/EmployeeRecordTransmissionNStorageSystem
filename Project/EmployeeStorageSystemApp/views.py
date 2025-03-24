from functools import wraps
import time
from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework import status  # type: ignore
from .models import * 
from .serializers import *
from django.db import IntegrityError
from rest_framework.parsers import MultiPartParser  # type: ignore
import pandas  # type: ignore
import threading

# Create your views here.

# Decorator for logging execution time
def log_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        response = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution Time: {end_time - start_time:.4f} seconds")
        return response
    return wrapper

class EmployeeAPI(APIView):
    parser_classes = [MultiPartParser]  

    def post(self, request):

        if 'file' not in request.FILES:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        uploaded_file = request.FILES['file']

        try:
            filedata = pandas.read_csv(uploaded_file, dtype=str)  
            if filedata.empty:
                return Response({"message": "Uploaded CSV is empty."}, status=status.HTTP_400_BAD_REQUEST)
            
            filedata["salary"] = filedata["salary"].astype(float)            
            filedata["date_of_joining"] = pandas.to_datetime(filedata["date_of_joining"], format="%d-%m-%Y").dt.strftime("%Y-%m-%d")            
            filedata["id"] = filedata["id"].astype(int)

            odd_records = filedata[filedata["id"] % 2 != 0]
            even_records = filedata[filedata["id"] % 2 == 0]
        
            employees_odd = [EmployeeRecord(**row) for _, row in odd_records.iterrows()]
            employees_even = [EmployeeRecord(**row) for _, row in even_records.iterrows()]
            
            def insert_records(records):
                if records:
                    EmployeeRecord.objects.bulk_create(records, ignore_conflicts=True)
            
            thread1 = threading.Thread(target=insert_records, args=(employees_odd,))
            thread2 = threading.Thread(target=insert_records, args=(employees_even,))
            
            thread1.start()
            print('Thread1 started..')
            thread2.start()
            print('Thread2 started..')

            thread1.join()
            thread2.join()
            
            return Response({"message": "File processed successfully with multi-threading (duplicates ignored)"}, status=status.HTTP_201_CREATED)

        except ValueError as ve:
            return Response({"error": f"Invalid data format: {str(ve)}"}, status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError as ie:
            return Response({"error": f"Database Integrity Error: {str(ie)}"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": f"Failed to process CSV: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

