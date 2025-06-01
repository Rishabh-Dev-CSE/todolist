from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.contrib.auth.decorators import login_required
import random as rm
from django.contrib import messages
import datetime as dt
from django.http import JsonResponse
from django.core.files.base import ContentFile
import base64
import json
import os
# Home view function, renders the home page........
def home(request):
    return render(request, 'index.html')

#Create User Task.........
@login_required
@csrf_exempt
def createUserTask(request):
    if request.user.boss_id:
        return render(request, 'createemployee.html')

    return render(request, 'managerlogin.html')

# Function to create a new user...........
@csrf_exempt
def createUser(request):
    if request.POST:
        phone_number = request.POST.get('phone_number')  # Get phone number from request
        email = request.POST.get('email')  # Get email from request
        uid = request.POST.get('user_id')  # Get user ID
        password = request.POST.get('password1')  # Get first password field
        confirm = request.POST.get('password2')  # Get second password field

        # Check if phone number already exists
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            return render(request, 'createuser.html', {'msg': 'Phone already exists!'})

        # Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'createuser.html', {'msg': 'Email already exists!'})

        # Check if user ID already exists
        if CustomUser.objects.filter(user_id=uid).exists():
            return render(request, 'createuser.html', {'msg': 'User already exists! (Choose another name)'})

        # Check if passwords match
        if password == confirm:
            user = CustomUser.objects.create_user(phone_number=phone_number, email=email, password=password, user_id=uid)
            if user is not None:
                user.save()
                return render(request, 'loginuser.html', {'msg': 'User created successfully'})

    return render(request, 'createuser.html')

# Function to create a manager........
@csrf_exempt
def createManager(request):
    if request.POST:
        phone_number = request.POST.get('phone_number')  # Get phone number
        email = request.POST.get('email')  # Get email
        manager_id = request.POST.get('manager_id')  # Get manager ID
        password = request.POST.get('password1')  # Get password
        confirm = request.POST.get('password2')  # Confirm password
        # Check if phone number already exists
        if BossCustomUser.objects.filter(phone_number=phone_number).exists():
            return render(request, 'createmanager.html', {'error': 'Phone already exists!'})

        # Check if email already exists
        if BossCustomUser.objects.filter(email=email).exists():
            return render(request, 'createmanager.html', {'error': 'Email already exists!'})

        # Check if user ID already exists
        if BossCustomUser.objects.filter(boss_id=manager_id).exists():
            return render(request, 'createmanager.html', {'error': 'Manager already exists! try another'})

        # Check if passwords match
        if password == confirm:
            user = BossCustomUser.objects.create_user(phone_number=phone_number, email=email, password=password, boss_id=manager_id, user_id=None)
            if user is not None:
                user.save()
                return render(request, 'createmanager.html', {'success': 'Manager created successfully'})
            else:
                return render(request, 'createmanager.html', {'error': 'Something went wrong'})
    return render(request, 'createmanager.html')

# Function to create an employee and his user Account........
@csrf_exempt
def createEmployee(request):
    r_code  = rm.randint(1000,9999)# this line of code create random mamaner code.......

    if not request.user.is_authenticated:
        return redirect('loginmanager')
    else:
        all_emp = BossCustomUser.objects.get(boss_id=request.user.boss_id)  # Get all employees under manager
        all_data = EmployeeModel.objects.filter(manager_id=all_emp)
        employee_data = all_data
        id_card_choices = EmployeeModel.employee_id_card_choice

    # now create Employee and his user Account .........
    if request.POST:
        if request.user.boss_id:
            manager = request.POST.get('manager_id')  # Get manager ID
            manager = BossCustomUser.objects.get(boss_id=manager)  # Get manager instance
           #check manager is not exists.....
            if manager is None:
                return render(request, 'managerlogin.html', {'msg': 'Invalid manager ID'})
        #................
            employee_id = request.POST.get('emp_id')  # Get employee ID
            employee_name = request.POST.get('emp_name')  #Get employee name
            email = request.POST.get('email')# Get employee email
            employee_DOB = request.POST.get('DOB')  # Get employee DOB
            phone_number = request.POST.get('phone_number')# get employee phone number
            id_card = request.POST.get('employee_id_card')#get employee card name
            card_number = request.POST.get('card_number')#get employee card details
            manager_code  = request.POST.get('manager_code')# get manager code
            #create password for employee.........
            password =(employee_DOB[0:4] + phone_number[-4:])
            # checking number and email
            if EmployeeModel.objects.filter(employee_email = email).exists()  or EmployeeModel.objects.filter(phone_number = phone_number).exists():
                return render(request, 'createemployee.html', {'error':'Employee phone number and email already exist !','emp_data': employee_data})
            #checking employee id .......
            if EmployeeModel.objects.filter(employee_id = employee_id).exists():
                    return render(request, 'createemployee.html', {'error':'Employee phone number and email already exist !','emp_data': employee_data})

            # Create new employee entry.......
            emp_data = EmployeeModel.objects.create(manager_id=manager, employee_id=employee_id, employee_name=employee_name, employee_email=email, employee_DOB=employee_DOB,employee_id_card=id_card,card=card_number,phone_number=phone_number)

            #Create Employee as user......
            emp_user = CustomUser.objects.create_user(password=password, manager_code=r_code, phone_number=phone_number,user_id = employee_id,email=email)

            # save all data ......
            if emp_data is not None:
                emp_data.save()
                emp_user.save()
                return render(request, 'createemployee.html', {'success': 'Employee created successfully', 'emp_data': employee_data,'id_card_choices': id_card_choices,'manager_code':r_code})
        else:
            return render (request, 'managerlogin.html',{'error':'(sorry to create !)Login a manager than create employee'})

    return render(request, 'createemployee.html', {'emp_data': employee_data,'id_card_choices': id_card_choices,'manager_code':r_code})

# Function to get all employees under a manager........
@login_required
@csrf_exempt
def allEmp(request):
    all_emp = BossCustomUser.objects.get(boss_id=request.user.boss_id)
    emp_data = EmployeeModel.objects.filter(manager_id=all_emp)
    emp_count = EmployeeModel.objects.filter(manager_id=all_emp).count()

    return render(request, 'allemp.html', {'allemp': emp_data, 'empcount':emp_count})

# Function to handle manager login.......
@csrf_exempt
def loginManager(request):
    if request.method == "POST":
        if request.POST.get('boss_id'):
            manager_id = request.POST.get('boss_id')  # Get boss ID
            password = request.POST.get('password')  # Get password

            try:
                user_fetch = BossCustomUser.objects.get(boss_id=manager_id)  # Fetch manager instance
            except BossCustomUser.DoesNotExist:
                return render(request, 'loginuser.html', {'msg': 'Manager ID not found'})

            user = authenticate(username=user_fetch.phone_number, password=password)  # Authenticate manager

            if user is not None:
                login(request, user)
                all_emp = BossCustomUser.objects.get(boss_id=request.user.boss_id)
                emp_data = EmployeeModel.objects.filter(manager_id=all_emp)
                id_card_choices = EmployeeModel.employee_id_card_choice
                return render(request, 'createemployee.html', {'msg': 'Manager Successfully Login', 'allemp': emp_data,'id_card_choices': id_card_choices})
            else:
                return render(request, 'loginuser.html', {'msg': 'Invalid credentials'})

    return render(request, 'loginuser.html')

@login_required
@csrf_exempt
def managerToUserTask(request, employee_id=None):
    all_emp = BossCustomUser.objects.get(boss_id=request.user.boss_id)
    emp_data = EmployeeModel.objects.filter(manager_id=all_emp)

    if employee_id:
        data_of_employee = EmployeeModel.objects.get(employee_id = employee_id)
        if data_of_employee is not None:
                return render(request, 'managertousertask.html', {'emp_fill':data_of_employee,'allemp': emp_data})
        else:
            pass

    if request.method == "POST":
        manager_id = BossCustomUser.objects.get(boss_id=request.user.boss_id)
        employee_id = request.POST.get('emp_id')
        employee = EmployeeModel.objects.get(employee_id =employee_id)
        d_date = request.POST.get('d-date')
        t_task = request.POST.get('task-title')
        des_task = request.POST.get('task-des')

        find_emp = EmployeeModel.objects.filter(employee_id=employee).first()

        if find_emp:
            ManagerToUserTask.objects.create(
                manager_id=manager_id,
                employee_user_id=employee,
                task_duration=d_date,
                task_title=t_task,
                task_discreption=des_task
            )
            return render(request, 'managertousertask.html', {'allemp': emp_data, 'msg': 'Task Referred'})

        else:
            return render(request, 'managertousertask.html', {'allemp': emp_data, 'msg': 'Employee Id is not found for this!'})

    return render(request, 'managertousertask.html', {'allemp': emp_data,})

#function to show all manager task.......

@login_required
@csrf_exempt
def allManagerTask(request):
    employee_side_task=''
    mg_task = ''
    if request.user.boss_id:
        mg_task = ManagerToUserTask.objects.filter(manager_id=request.user.id)
        print(mg_task)
    else:
        find_emp = EmployeeModel.objects.get(employee_id = request.user)
        employee_side_task = ManagerToUserTask.objects.filter(employee_user_id = find_emp)
    return render(request, 'alltask.html',{'mg_task':mg_task, 'emp_task':employee_side_task})

@csrf_exempt
@login_required
def taskUpdate(request):
    completed = request.GET.get('completed')
    task_id = request.GET.get('task_id')
    find_task = ManagerToUserTask.objects.get(id =task_id)
    find_task.task_status = completed
    find_task.save()

    return HttpResponse('done')
# Function to handle user login......

@csrf_exempt
def loginUser(request):
    if request.method == "POST":
        phone_number = request.POST.get('phone_number')  # Get phone number
        password = request.POST.get('password')  # Get password

        user = authenticate(username=phone_number, password=password)  # Authenticate user
        if user is not None:
            login(request, user)
            return render(request, 'index.html', {'msg': 'User logged in successfully', 'user_id': user.id})
        else:
            return render(request, 'loginuser.html', {'msg': 'Something went wrong'})

    return render(request, 'loginuser.html')

# fuction to loguot user.......
def logoutUser(request):
    logout(request)
    return render(request, 'loginuser.html', {'logout': 'Logout successfully'})

#function to delete Employee........
def deleteEemployee(request,id):

        if EmployeeModel.objects.filter(id=id).exists():
            find_emp = EmployeeModel.objects.get(id=id)

            if CustomUser.objects.filter(user_id = find_emp).exists():
                find_user_emp=CustomUser.objects.get(user_id = find_emp)
                find_user_emp.delete()# this line blow the code delete employee user Account
                find_emp.delete() # this line of code deleted employee's
                return HttpResponse("<script> alert('Employee and  his user Account deleted successfully'), window.location.href = '../all-emp'</script>")
        else:
             return HttpResponse("<script> alert('Wrong somthing can not be find employee Account details (faild opt) '), window.location.href = '../all-emp' </script>")



        all_emp = BossCustomUser.objects.get(boss_id=request.user.boss_id)
        emp_data = EmployeeModel.objects.filter(manager_id=all_emp)
        return render(request, 'allemp.html', {'msg':'Emplyee deleted successfully','allemp': emp_data})



@login_required
def filterUserTask(request):
        manager_id = request.GET.get('manager_id')
        print(manager_id)
        if BossCustomUser.objects.filter(boss_id = manager_id).exists():
            pass
        else:
            return HttpResponse('Manager Not Found ! Re-try')

        find_user_task = ManagerToUserTask.objects.filter(manager_id=manager_id, employee_user_id = request.user)


        return render(request, 'alltask.html', {'user_task':find_user_task})

@csrf_exempt
def capture_image(request):
    num = rm.randint(10000,99999)
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            video_data = data.get("video", "")

            if not video_data:
                print("❌ No video data received!")
                return JsonResponse({"error": "No video data received"}, status=400)

            # Extract Base64 data
            format, video_str = video_data.split(";base64,")
            ext = format.split("/")[-1]

            # File Path
            file_name = f"{request.user}{num}.{ext}"
            folder_name = f"media/{request.user}"
            os.makedirs(folder_name, exist_ok=True)
            file_path = os.path.join(f"{folder_name}", file_name)

            # Debug: Print file path
            print(f"✅ Saving video at: {file_path}")

            # Save Video
            with open(file_path, "wb") as f:
                f.write(base64.b64decode(video_str))

            print("✅ Video saved successfully!")

            return JsonResponse({"message": "Video saved successfully!", "file_path": file_path})

        except Exception as e:
            print(f"❌ Error: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
def upload_video(request):
    if request.method == "POST" and request.FILES.get("video"):
        video = request.FILES["video"]
        save_path = os.path.join("media", video.name)

        with open(save_path, "wb+") as destination:
            for chunk in video.chunks():
                destination.write(chunk)

        return JsonResponse({"message": "Upload successful", "video_url": f"/media/{video.name}"})

    return JsonResponse({"error": "Invalid request"}, status=400)
