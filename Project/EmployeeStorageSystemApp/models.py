from django.db import models

# Create your models here.

class EmployeeRecord(models.Model):
    id = models.AutoField(primary_key=True) 
    employee_id = models.CharField(max_length=20, unique=True) 
    name = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=100)
    department = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_joining = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def save(self, *args, **kwargs):
    #     if not self.employee_id:  # Generate only if empty
    #         last_record = EmployeeRecord.objects.order_by('-employee_id').first()
    #         if last_record and last_record.employee_id.startswith('EMPID'):
    #             last_number = int(last_record.employee_id[5:])  # Extract numeric part
    #             new_number = last_number + 1
    #         else:
    #             new_number = 1
    #         self.employee_id = f'EMPID{new_number:03d}'  # Format as EMPID001, EMPID002, etc.

    #     super().save(*args, **kwargs)  # Save the object

