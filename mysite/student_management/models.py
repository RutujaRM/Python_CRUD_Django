from django.db import models

# Create your models here.

# School table Schema
class School(models.Model):
    School_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Address = models.TextField(max_length=100)
    City =models.CharField(max_length=20)
    Phone_No=models.CharField(max_length=10)
    Postal_Code =models.CharField(max_length=6)
    Fax_No = models.CharField(max_length=10)
    Email=models.EmailField(unique=True)
   # School_Type = models.CharField(max_length=20)    #public private

    def __str__(self):    #Constructor
        return self.School_ID
    

# Student Table Schema  
class Students(models.Model):
    Student_Id=models.AutoField(primary_key=True)
    First_Name=models.CharField(max_length=20)
    Last_Name=models.CharField(max_length=20)
    Gender=models.CharField(max_length=10)
    Email=models.EmailField(unique=True)
    Standard=models.CharField(max_length=5)
    DOB=models.DateField()  
    Address=models.TextField(max_length=200)
    City=models.CharField(max_length=100)
    Phone_No=models.CharField(max_length=10)
    Parents_Phone_No=models.CharField(max_length=10)
    school=models.ForeignKey(School, on_delete=models.CASCADE)  ## Foreign Key to link student to particular school 

    def __str__(self):    #Constructor
        return str(self.Student_Id)   
    

# Users Role Table Schema

class Users(models.Model):
    User_Roles=(
        ('admin','Admin'),
        ('user','User'),
    )
    User_Id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50)
    Phone_No = models.IntegerField(max_length=10)
    Email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    Role = models.CharField(max_length=5 , choices=User_Roles , default='user')

    def __str__(self):
        return str(self.User_Id)



    
    



  