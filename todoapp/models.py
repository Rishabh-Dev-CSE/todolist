from django.db import models
from django.contrib.auth.models import AbstractUser
from . manager import *

#_______________User Model_________________________

class CustomUser(AbstractUser):
    username =None
    phone_number = models.CharField(max_length=255,unique=True, default="")
    email = models.EmailField(unique=True ,null=True,blank=True)
    user_id = models.CharField(unique=True, null=True, blank=True,max_length=255,default='')
    boss_id = models.CharField(unique=True,null=True, blank=True,max_length=255)
    password = models.CharField(max_length=255)
    manager_code = models.CharField(max_length=255, null=True, blank=True , default='')

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()

    def __str__(self):
        return str(self.user_id)

    #-----------------------Boss Model-----------------------

class BossCustomUser(CustomUser):

    objects = BossUserManager()
    def __str__(self):
        return str(self.boss_id)

class EmployeeModel(models.Model):
    emp_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employee', null=True, blank=True ,default="")
    manager_id = models.ForeignKey(BossCustomUser, on_delete=models.CASCADE,default='', related_name='manegr_employee')
    employee_id = models.CharField(max_length=255, unique=True)
    employee_name = models.CharField(max_length=255)
    employee_email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True ,default='Not Found')
    employee_DOB = models.DateField()
    employee_joining_date =models.DateField(auto_now_add=True)
    employee_id_card_choice = (
        ('Pancard','Pancard'),
        ('Aadharcard', 'Aadharcard'),
        ('Pending','Pending'),
    )
    employee_id_card = models.CharField(max_length=255, choices=employee_id_card_choice, default="Pending")
    card = models.CharField(max_length=255,default="Add", blank=True)

    def __str__(self):
        return self.employee_id

class ManagerToUserTask(models.Model):
    manager_id = models.ForeignKey(BossCustomUser, on_delete=models.CASCADE,default='')
    employee_user_id = models.ForeignKey(EmployeeModel, on_delete=models.CASCADE,default='')
    task_duration = models.DateField()
    send_date = models.DateTimeField(auto_now_add=True)
    task_title = models.CharField(max_length=255, default="",blank=True)
    task_discreption = models.TextField(null=True, default='')
    status_choice = (
        ('pending','pending'),
        ('completed', 'completed')
    )
    task_status = models.CharField(max_length=100, choices=status_choice,blank=True, default='pending')
  
    def __str__(self):
        return str(self.employee_user_id)

class UserTask(models.Model):
    user_id =  models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title_choice = (('Home Work','Home Work'),
                    ('Office Work','Office Work'),
                    ('Other','Other'))
    task_title = models.CharField(max_length=255, choices=title_choice)
    task_description = models.CharField(max_length=255)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user_id

class ManagerTask(models.Model):
    user_id = models.ForeignKey(UserTask, on_delete=models.CASCADE)
    manager_id = models.CharField(max_length=255)
    give_task = models.CharField(max_length=255)
    suggetion_description = models.TextField(null=True, default='', blank=True)
    d_date = models.DateField()
    a_date = models.DateField(auto_now_add=True)
    a_time = models.TimeField(auto_now_add=True)

    def __srt__(self):
        return self.manager_id


