from functools import wraps
import time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from .models import * 
from .serializers import *
from django.db import IntegrityError
from rest_framework.parsers import MultiPartParser

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

from datetime import datetime
from rest_framework.parsers import MultiPartParser
import csv
import io

class EmployeeAPI(APIView):
    parser_classes = [MultiPartParser]  

    def post(self, request):
        print("Request Data:", request.data)

        if 'file' not in request.FILES:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        uploaded_file = request.FILES['file']

        try:
            decoded_file = uploaded_file.read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(decoded_file))
            records = list(reader)

            employees_to_insert = []

            for record in records:
                try:
                    record["salary"] = float(record["salary"])  
                    record["date_of_joining"] = datetime.strptime(record["date_of_joining"].strip(), "%d-%m-%Y").strftime("%Y-%m-%d")
                    employees_to_insert.append(EmployeeRecord(**record))

                except ValueError as ve:
                    return Response({"error": f"Invalid date format for {record['date_of_joining']}. Use DD-MM-YYYY."},
                                    status=status.HTTP_400_BAD_REQUEST)

            if employees_to_insert:
                EmployeeRecord.objects.bulk_create(employees_to_insert, ignore_conflicts=True)
                return Response({"message": "File processed successfully (duplicates ignored)"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "No new records inserted (all were duplicates)"}, status=status.HTTP_200_OK)

        except IntegrityError as ie:
            return Response({"error": f"Database Integrity Error: {str(ie)}"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": f"Failed to process CSV: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

