
from urllib import request
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import School, Students, Users
import json

# **************************************  School Model *************************************************

# 1) Get method To get school list

@csrf_exempt
@require_http_methods(["GET"])
def get_schools(request):
    schools = School.objects.all()  # retrieves all records from the School model School.objects.all() returns a QuerySet 
    data = []                       #List created To store the serialized school data
    for school in schools:
        data.append({                         # dictionaries are appended to the data list
                'School_ID': school.School_ID,
                'Name': school.Name,
                'Address': school.Address,
                'City': school.City,
                'Phone_No': school.Phone_No,
                'Postal_Code': school.Postal_Code,
                'Fax_No': school.Fax_No,
                'Email': school.Email, 
           
        })
    return JsonResponse(data, safe=False) # ensure data is correctly formatted and not introduce serialization errors or security risks.

# 2) To get particular id school

@csrf_exempt
@require_http_methods(["GET"])
def get_school_id(request, id):
    try:
        school = School.objects.get(School_ID=id)  # Retrieve school object by School_ID
        
        # Prepare data to be returned in JSON format
        data = {
            'School_ID': school.School_ID,
            'Name': school.Name,
            'Address': school.Address,
            'City': school.City,
            'Phone_No': school.Phone_No,
            'Postal_Code': school.Postal_Code,
            'Fax_No': school.Fax_No,
            'Email': school.Email,
        }
        
        return JsonResponse(data)
    
    except School.DoesNotExist:
        return HttpResponseNotFound(f'School with ID {id} not found')
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# 3) post method to post/insert/add data into list

@csrf_exempt   #(Cross-Site Request Forgery) CSRF protection is important for security,
@require_http_methods(["POST"])
def post_school(request):
    data = json.loads(request.body)

    required_fields = ['Name', 'Address', 'City', 'Phone_No', 'Postal_Code', 'Fax_No', 'Email']
    
    # Check all required fields
    for field in required_fields:
        if field not in data:
            return HttpResponseBadRequest(f'Missing required field: {field}')
    
    # Create new School object
    school = School.objects.create(  
        Name=data['Name'],               # which takes the relevant fields from the data dictionary.saves the new school record to the database 
        Address=data['Address'],
        City=data['City'],
        Phone_No=data['Phone_No'],
        Postal_Code=data['Postal_Code'],
        Fax_No=data['Fax_No'],
        Email=data['Email']
    )    

    # Insert new inserted data in the response data dictionary  hold the details of the newly created school.
    response_data = {
        'School_ID': school.School_ID,
        'Name': school.Name,
        'Address': school.Address,
        'City': school.City,
        'Phone_No': school.Phone_No,
        'Postal_Code': school.Postal_Code,
        'Fax_No': school.Fax_No,
        'Email': school.Email,
    }
    return JsonResponse(response_data, status=201)  #201 inser sucessfully


# 4) Put :- To Update particular fields

@csrf_exempt
@require_http_methods(["PUT"])
def update_school_data(request, id):
    try:
        school = School.objects.get(School_ID=id)
        data = json.loads(request.body) # reads the raw body of the request and parses it as JSON, storing the resulting dictionary in the data.
        
        if 'Name' in data:                  #checks if each field present in data dictonary 
            school.Name = data['Name']      #if present then update that attrivute with value present in data variable dictonary
        if 'Address' in data:
            school.Address = data['Address']
        if 'City' in data:
            school.City = data['City']
        if 'Phone_No' in data:
            school.Phone_No = data['Phone_No']
        if 'Postal_Code' in data:
            school.Postal_Code = data['Postal_Code']
        if 'Fax_No' in data:
            school.Fax_No = data['Fax_No']
        if 'Email' in data:
            school.Email = data['Email']

        school.save()
        
        return JsonResponse({'message': 'School updated successfully'}) #f no school with the specified ID 404 Not Found
    except School.DoesNotExist:
        return JsonResponse({'error': 'School not found'}, status=404)
    except Exception as e:                                 #catches any exceptions and e var holds that object instance 
        return JsonResponse({'error': str(e)}, status=400) #Then converts that exception/error msg into string


# 5) Delete :- To delete particular school
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_school(request, id):
    try:
        school = School.objects.get(School_ID=id)
        school.delete()
        return JsonResponse({'message': 'School deleted successfully'})
    except School.DoesNotExist:
        return JsonResponse({'error': 'School not found'}, status=404)







# **************************************  Student Model *************************************************


#1) Get Method

@csrf_exempt
def get_student(request):
    if request.method == 'GET':
        students = Students.objects.all().values(  #retrieves all records from the / values() is a method that returns a QuerySet

             #When we want particular fields then only mention that fields only here /  allows selecting specific fields from the model
        )  
        return JsonResponse(list(students), safe=False)


#2) Get Particular Student data
@csrf_exempt
@require_http_methods(["GET"])
def get_student_id(request, id):
    try:
        student = Students.objects.get(Student_Id=id)  # Retrieve student object by Student_Id
        
        data = {
            'Student_Id': student.Student_Id,
            'First_Name': student.First_Name,
            'Last_Name': student.Last_Name,
            'Gender': student.Gender,
            'Email': student.Email,
            'Standard': student.Standard,
            'DOB': student.DOB,
            'Address': student.Address,
            'City': student.City,
            'Phone_No': student.Phone_No,
            'Parents_Phone_No': student.Parents_Phone_No,
            'school_id': student.school.pk,
        }
        
        return JsonResponse(data)
    
    except Students.DoesNotExist:
        return HttpResponseNotFound(f'Student with ID {id} not found')
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# 3) Post student data
@csrf_exempt
def post_student(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            required_fields = ['First_Name', 'Last_Name', 'Gender', 'Email', 'Standard', 'DOB', 'Address', 'City', 'Phone_No', 'Parents_Phone_No', 'School_ID']
            
            # Check all required fields
            for field in required_fields:
                if field not in data:
                    return HttpResponseBadRequest(f'Missing required field: {field}')
            
            # Check if the school exists
            try:
                school = School.objects.get(School_ID=data['School_ID'])
            except School.DoesNotExist:
                return HttpResponseBadRequest("School not found.")
            
            # Create a new Students object
            student = Students(
                First_Name=data['First_Name'],
                Last_Name=data['Last_Name'],
                Gender=data['Gender'],
                Email=data['Email'],
                Standard=data['Standard'],
                DOB=data['DOB'],
                Address=data['Address'],
                City=data['City'],
                Phone_No=data['Phone_No'],
                Parents_Phone_No=data['Parents_Phone_No'],
                school=school
            )
            
            # Save the student object to the database
            student.save()

            # Prepare response data
            response_data = {
                'Student_Id': student.Student_Id,        # Student_Id is already an integer
                'First_Name': student.First_Name,
                'Last_Name': student.Last_Name,
                'Gender': student.Gender,
                'Email': student.Email,
                'Standard': student.Standard,
                'DOB': student.DOB,
                'Address': student.Address,
                'City': student.City,
                'Phone_No': student.Phone_No,
                'Parents_Phone_No': student.Parents_Phone_No,
                'School_ID': student.school.pk,
            }

            return JsonResponse(response_data, status=201)  # Return JSON response with status 201
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON format.")
    else:
        return HttpResponseBadRequest("Only POST method is allowed.")



# 4) Put :- To Update particular fields

@csrf_exempt
@require_http_methods(["PUT"])
def update_student_data(request, id):
    try:
        student = Students.objects.get(Student_Id=id)
        data = json.loads(request.body)
        
        if 'First_Name' in data:
            student.First_Name = data['First_Name']
        if 'Last_Name' in data:
            student.Last_Name = data['Last_Name']
        if 'Gender' in data:
            student.Gender = data['Gender']
        if 'Email' in data:
            student.Email = data['Email']
        if 'Standard' in data:
            student.Standard = data['Standard']
        if 'DOB' in data:
            student.DOB = data['DOB']
        if 'Address' in data:
            student.Address = data['Address']
        if 'City' in data:
            student.City = data['City']
        if 'Phone_No' in data:
            student.Phone_No = data['Phone_No']
        if 'Parents_Phone_No' in data:
            student.Parents_Phone_No = data['Parents_Phone_No']
        
        # Update school if provided
        if 'School_Details' in data:
            try:
                school = School.objects.get(School_ID=data['School_Details'])
                student.school = school
            except School.DoesNotExist:
                return JsonResponse({'error': 'School not found'}, status=404)

        student.save()
        
        return JsonResponse({'message': 'Student updated successfully'})
    except Students.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# 5) Delete :- To delete particular school
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_student(request, id):
    try:
        student = Students.objects.get(Student_Id=id)
        student.delete()
        return JsonResponse({'message': 'Student deleted successfully'})
    except Students.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)



# **************************************************** Users Role Model *************************************************

# 1) Get Users List 
@csrf_exempt
@require_http_methods(["GET"])
def get_users(request):
    users = Users.objects.all()
    data = []
    for user in users:
        data.append({
                'User_Id': user.User_Id,
                'Name': user.Name,
                'Phone_No': user.Phone_No,
                'Email': user.Email, 
                'password': user.password,
                'Role':user.Role
        })
    return JsonResponse(data, safe=False) #safe=False indicates that the object being serialized is not necessarily JSON-serializable by default


#2) Get Particular Users data

@csrf_exempt
@require_http_methods(["GET"])
def get_users_id(request, id):
    try:
        user = Users.objects.get(User_Id=id)  # Retrieve user object by User_Id
        
        # Prepare data to be returned in JSON format
        data = {
            'User_Id': user.User_Id,
            'Name': user.Name,
            'Phone_No': user.Phone_No,
            'Email': user.Email,
            'password': user.password,
            'Role': user.Role,
        }
        
        return JsonResponse(data)
    
    except Users.DoesNotExist:
        return HttpResponseNotFound(f'User with ID {id} not found')
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# 3) Post Users Data with there roles

@csrf_exempt 
@require_http_methods(["POST"])
def post_user_role(request):
    data = json.loads(request.body)

    required_fields = ['Name', 'Phone_No', 'Email', 'password', 'Role']
    
    # Check all required fields
    for field in required_fields:
        if field not in data:
            return HttpResponseBadRequest(f'Missing required field: {field}')
    
    # Create new School object
    users = Users.objects.create(
        Name=data['Name'],
        Phone_No=data['Phone_No'],
        Email=data['Email'],
        password=data['password'],
        Role=data['Role'],
    )    

    # Insert new inserted data in the response data dictionary
    response_data = {
        'User_Id': users.User_Id,
        'Name': users.Name,
        'Phone_No': users.Phone_No,
        'Email': users.Email,
        'password': users.password,
        'Role': users.Role,
    }
    return JsonResponse(response_data, status=201)  #201 inser sucessfully



# ***************************************************** Admin Role For School CRUD  *****************************************************

# Check if the user is an admin which value we get from Frontend
# def is_admin(user):          
#     return user.Role == 'admin'   

# if request.user.Role != 'admin':
#         return HttpResponseForbidden()


# 1) Post insert school data by admin

@csrf_exempt
@require_http_methods(["POST"])
def admin_create_school(request, user_id):
    try:
        # Retrieve user based on user_id
        user_temp = Users.objects.get(user_id=user_id)
        if request.method == 'POST':
        # Check if the user has the role of "Admin"
          if user_temp.user_role == "Admin":
            data = json.loads(request.body)

            required_fields = ['Name', 'Address', 'City', 'Phone_No', 'Postal_Code', 'Fax_No', 'Email']
            for field in required_fields:
                if field not in data:
                    return HttpResponseBadRequest(f'Missing required field: {field}')
            
            school = School.objects.create(
                Name=data['Name'],
                Address=data['Address'],
                City=data['City'],
                Phone_No=data['Phone_No'],
                Postal_Code=data['Postal_Code'],
                Fax_No=data['Fax_No'],
                Email=data['Email']
            )

            response_data = {
                'School_ID': school.School_ID,
                'Name': school.Name,
                'Address': school.Address,
                'City': school.City,
                'Phone_No': school.Phone_No,
                'Postal_Code': school.Postal_Code,
                'Fax_No': school.Fax_No,
                'Email': school.Email,
            }
            return JsonResponse(response_data, status=201)
    except Users.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)



# 2) Put To update school data by Admin

@csrf_exempt
@require_http_methods(["PUT"])
def admin_update_school(request, user_id, school_id):
    # Retrieve user based on user_id
    user_temp = Users.objects.get(user_id=user_id)
    
    if request.method == 'PUT':
    # Check if the user has the role of "Admin"
     if user_temp.user_role == "Admin":
       
            data = json.loads(request.body)
            try:
                school = School.objects.get(School_ID=school_id)
                if 'Name' in data:
                    school.Name = data['Name']
                if 'Address' in data:
                    school.Address = data['Address']
                if 'City' in data:
                    school.City = data['City']
                if 'Phone_No' in data:
                    school.Phone_No = data['Phone_No']
                if 'Postal_Code' in data:
                    school.Postal_Code = data['Postal_Code']
                if 'Fax_No' in data:
                    school.Fax_No = data['Fax_No']
                if 'Email' in data:
                    school.Email = data['Email']

                school.save()
                
                response_data = {
                    'School_ID': school.School_ID,
                    'Name': school.Name,
                    'Address': school.Address,
                    'City': school.City,
                    'Phone_No': school.Phone_No,
                    'Postal_Code': school.Postal_Code,
                    'Fax_No': school.Fax_No,
                    'Email': school.Email,
                }
                return JsonResponse(response_data, status=200)
            except School.DoesNotExist:
                return JsonResponse({'error': 'School not found'}, status=404)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse("You are not allowed to access", status=400, safe=False)


# 3) Delete school by admin

@csrf_exempt
@require_http_methods(["DELETE"])
def admin_delete_school(request, user_id, school_id):
    try:
        # Retrieve user based on user_id
        user_temp = Users.objects.get(user_id=user_id)
        
        # Check if the user has the role of "Admin"
        if user_temp.user_role != "Admin":
            return JsonResponse({'error': 'Only Admins can delete schools'}, status=401)

        if request.method == 'DELETE':
            try:
                school = School.objects.get(School_ID=school_id)
                school.delete()
                return JsonResponse({'message': 'School deleted successfully'}, status=204)
            except School.DoesNotExist:
                return JsonResponse({'error': 'School not found'}, status=404)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
    except Users.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse
  
# ***************************************************** Admin Role For Student CRUD  *****************************************************

# 1) Post Method For Student add by Admin

@csrf_exempt
@require_http_methods(["POST"])
def admin_create_student(request, user_id):
    try:
        # Retrieve user based on user_id
        user_temp = Users.objects.get(user_id=user_id)
        
        # Check if the user has the role of "Admin"
        if user_temp.user_role != "Admin":
            return JsonResponse({'error': 'Only Admins can create students'}, status=401)

        if request.method == 'POST':
            data = json.loads(request.body)
            
            required_fields = ['Name', 'Roll_No', 'Class', 'Address', 'Phone_No', 'Email']
            for field in required_fields:
                if field not in data:
                    return HttpResponseBadRequest(f'Missing required field: {field}')
            
            student = Students.objects.create(
                Name=data['Name'],
                Roll_No=data['Roll_No'],
                Class=data['Class'],
                Address=data['Address'],
                Phone_No=data['Phone_No'],
                Email=data['Email']
            )

            response_data = {
            'Student_Id': student.Student_Id,
            'First_Name': student.First_Name,
            'Last_Name': student.Last_Name,
            'Gender': student.Gender,
            'Email': student.Email,
            'Standard': student.Standard,
            'DOB': student.DOB,
            'Address': student.Address,
            'City': student.City,
            'Phone_No': student.Phone_No,
            'Parents_Phone_No': student.Parents_Phone_No,
            'School_ID': student.school.pk,
        }
            return JsonResponse(response_data, status=201)
    except Users.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    



# 2) Put updata student data by Admin

@csrf_exempt
@require_http_methods(["PUT"])
def admin_update_student(request, user_id, student_id):
    try:
        # Retrieve user based on user_id
        user_temp = Users.objects.get(user_id=user_id)
        
        # Check if the user has the role of "Admin"
        if user_temp.user_role != "Admin":
            return JsonResponse({'error': 'Only Admins can update students'}, status=401)

        if request.method == 'PUT':
            data = json.loads(request.body)
            try:
                student = Students.objects.get(Student_ID=student_id)
                if 'Name' in data:
                    student.Name = data['Name']
                if 'Roll_No' in data:
                    student.Roll_No = data['Roll_No']
                if 'Class' in data:
                    student.Class = data['Class']
                if 'Address' in data:
                    student.Address = data['Address']
                if 'Phone_No' in data:
                    student.Phone_No = data['Phone_No']
                if 'Email' in data:
                    student.Email = data['Email']

                student.save()
                
                response_data = {
            'Student_Id': student.Student_Id,
            'First_Name': student.First_Name,
            'Last_Name': student.Last_Name,
            'Gender': student.Gender,
            'Email': student.Email,
            'Standard': student.Standard,
            'DOB': student.DOB,
            'Address': student.Address,
            'City': student.City,
            'Phone_No': student.Phone_No,
            'Parents_Phone_No': student.Parents_Phone_No,
            'School_ID': student.school.pk,
        }
                return JsonResponse(response_data, status=200)
            except Students.DoesNotExist:
                return JsonResponse({'error': 'Student not found'}, status=404)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
    except Users.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# 3) Delete student by Admin

@csrf_exempt
@require_http_methods(["DELETE"])
def admin_delete_student(request, user_id, student_id):
    try:
        # Retrieve user based on user_id
        user_temp = Users.objects.get(user_id=user_id)
        
        # Check if the user has the role of "Admin"
        if user_temp.user_role != "Admin":
            return JsonResponse({'error': 'Only Admins can delete students'}, status=401)

        if request.method == 'DELETE':
            try:
                student = Students.objects.get(Student_ID=student_id)
                student.delete()
                return JsonResponse({'message': 'Student deleted successfully'}, status=204)
            except Students.DoesNotExist:
                return JsonResponse({'error': 'Student not found'}, status=404)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
    except Users.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)




# ************************************* Students list by school id **********************************

@csrf_exempt
@require_http_methods(["GET"])
def get_students_by_school_id(request, id):
    try:
        school = School.objects.get(School_ID=id)  # Retrieve the school object by its primary key
        students = Students.objects.filter(school=school)  # Filter students by the retrieved school object

       # JSON format
        data = []
        for student in students:
            data.append({
                'Student_Id': student.Student_Id,
                'First_Name': student.First_Name,
                'Last_Name': student.Last_Name,
                'Gender': student.Gender,
                'Email': student.Email,
                'Standard': student.Standard,
                'DOB': student.DOB,
                'Address': student.Address,
                'City': student.City,
                'Phone_No': student.Phone_No,
                'Parents_Phone_No': student.Parents_Phone_No,
                'School_ID': student.school.pk,
            })

        return JsonResponse(data, safe=False)
    
    except School.DoesNotExist:
        return HttpResponseNotFound(f'School with ID {id} does not exist')

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


















































# ##########################################  School Model #################################################

# ## 1) Get Method :- To fetch data from database

# class SchoolList(View):
#     @csrf_exempt
#     def post(request,args):
#         schools = School.objects.all()  #Fetch school data fields from School Model into this schools variable
#         schools_list = []               #Creates School list 

#         for school in schools:          #Loop on that schools data and append/add data into school list into dictonary
#             schools_list.append(
#                 {                       # Create dictonary key:value pairs
#                 'S_ID': school.S_ID,
#                 'Name': school.Name,
#                 'Address': school.Address,
#                 'City': school.City,
#                 'Phone_No': school.Phone_No,
#                 'Postal_Code': school.Postal_Code,
#                 'Fax_No': school.Fax_No,
#                 'Email': school.Email, 
#                 }
#             )
#         return JsonResponse(schools_list , safe=False)  
    
# ## 1) Post Method :- To insert data School into database
#     @csrf_exempt
    # def post(request):
    #     data = json.loads(request.body)

    #     required_fields=['Name','Address','City','Phone_No','Postal_Code','Fax_No','Email']
        
    #     #Check all required fields are present or not
    #     for field in required_fields:
    #         if field not in data:
    #             return HttpResponseBadRequest(f'Missing required field: {field}')
          
    #     #Create new School Object when new school data is enter
    #     school = School.objects.create(
    #         Name=data['Name'],
    #         Address=data['Address'],
    #         City=data['City'],
    #         Phone_No=data['Phone_No'],
    #         Postal_Code=data['Postal_Code'],
    #         Fax_No=data['Fax_No'],
    #         Email=data['Email']
    #     )    

    #     #Assign new generated data in this response data dictonary
    #     response_data = {
    #         'S_ID': school.S_ID,
    #         'Name': school.Name,
    #         'Address': school.Address,
    #         'City': school.City,
    #         'Phone_No': school.Phone_No,
    #         'Postal_Code': school.Postal_Code,
    #         'Fax_No': school.Fax_No,
    #         'Email': school.Email,
    #     }

    #  # Return the response data with a 201 status code
    #     return JsonResponse(response_data, status=201)

# def student_create():
#     if request.method in ['POST', 'PUT']:
#         schools = School.objects.all()  
#         schools_list = []         

#         for school in schools:         
#             schools_list.append(
#                 {                 
#                 'S_ID': school.S_ID,
#                 'Name': school.Name,
#                 'Address': school.Address,
#                 'City': school.City,
#                 'Phone_No': school.Phone_No,
#                 'Postal_Code': school.Postal_Code,
#                 'Fax_No': school.Fax_No,
#                 'Email': school.Email, 
#                 }
#             )
#         return JsonResponse(schools_list , safe=False) 
    
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator


# @method_decorator(csrf_exempt, name='post')
# class UserView(View):

#    # Check csrf here  
#    def get(self, request):
#        pass
#       #code here

#    # exempt csrf will affect only post method
#    def post(self, request):
#        pass
#        #code here





# from django.views import View
# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt


# class MyView(View):
#     def get(*args, **kwargs):
#         print("RUTUJA")
#         return HttpResponse('This is a POST response')




