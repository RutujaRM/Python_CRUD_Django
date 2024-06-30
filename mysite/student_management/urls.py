
from django.urls import path
from . import views

urlpatterns = [

   ## School API
      path("school_list",view=views.get_schools , name="school_list"),       #OK 
      path("school_id/<int:id>",view=views.get_school_id,name="school_id" ), #OK
      path("school_add", view=views.post_school,name="school_add" ),         #OK 
      path("school_update/<int:id>" , view=views.update_school_data , name="school_update"), #OK
      path("school_delete/<int:id>" ,view=views.delete_school , name="delete_school" ),      #OK

   ## Student API  
      path("student_list",view=views.get_student , name="student_list"),          #OK
      path("student_id/<int:id>",view=views.get_student_id,name="student_id" ),   #OK
      path("student_add", view=views.post_student,name="student_add" ),            #OK           
      path("student_update/<int:id>" , view=views.update_student_data , name="student_update"), #OK
      path("student_delete/<int:id>" ,view=views.delete_student , name="delete_student" ),    #OK


   ## Users API
      path("users_list",view=views.get_users , name="users_list"), 
      path("users_id/<int:id>",view=views.get_users_id , name="users_id"),   
      path("users_add" , view=views.post_user_role ,name="users_add") , 


   ## User With Role Admin School API
    path("admin_school_add" , view=views.admin_create_school , name="admin_school_add"),
    path("admin_school_update/<int:id>" , view=views.admin_update_school , name="admin_school_update"),
    path("admin_school_delete/<int:id>" , view=views.admin_delete_school , name="admin_school_delete"),


   ## User With Role Admin Student API

     path("admin_student_add" , view=views.admin_create_student , name="admin_school_add"),
    path("admin_student_update/<int:id>" , view=views.admin_update_student , name="admin_school_update"),
    path("admin_student_delete/<int:id>" , view=views.admin_delete_student , name="admin_school_delete"),


   path("students_by_school_id/<int:id>" , view=views.get_students_by_school_id , name="students_by_school_id")

        
        

 ]


