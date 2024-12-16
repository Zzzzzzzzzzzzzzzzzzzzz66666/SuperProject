from django.db import models
# 管理员类
from django.db import models

class Admin(models.Model):
    ROLE_CHOICES = (
        ('doctor', '医生'),
        ('patient', '病人'),
    )

    id = models.AutoField(primary_key=True)  # 自动生成主键
    name = models.CharField(max_length=45)  # 用户名
    password = models.CharField(max_length=128)  # 加密存储密码
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')  # 角色，默认为病人

    class Meta:
        db_table = 'Admin'


class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # 默认值为0
    doctor_room = models.PositiveIntegerField(default=0)  # 默认值为0

    class Meta:
        db_table = 'Department'

    def __str__(self):
        return self.name


class UserDoctor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    id_card = models.CharField(max_length=18, default='000000000000000000')  # 默认身份证号
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    status = models.SmallIntegerField(default=1)  # 默认值为1，表示医生在职

    class Meta:
        db_table = 'UserDoctor'

    def __str__(self):
        return self.name


class UserPatient(models.Model):
    GENDER_CHOICES = (
        ('M', '男'),
        ('F', '女'),
    )

    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    age = models.IntegerField(default=0)
    height = models.FloatField(default=0.0)  # 身高默认值为0.0
    weight = models.FloatField(default=0.0)  # 体重默认值为0.0
    phone_number = models.CharField(max_length=15)

    class Meta:
        db_table = 'UserPatient'


class Order(models.Model):
    GENDER_CHOICES = (
        ('M', '男'),
        ('F', '女'),
    )

    name = models.CharField(max_length=100)  # 姓名
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')  # 性别
    age = models.IntegerField(default=0)  # 年龄
    phone_number = models.CharField(max_length=15)  # 电话号码
    id_card = models.CharField(max_length=18, default='000000000000000000')  # 默认身份证号
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)  # 科室
    doctor = models.ForeignKey(UserDoctor, on_delete=models.SET_NULL, null=True)  # 医生

    class Meta:
        db_table = 'Order'


class PatientFamily(models.Model):
    GENDER_CHOICES = (
        ('M', '男'),
        ('F', '女'),
    )
    RELATION_CHOICES = (
        ('Father', '父亲'),
        ('Mother', '母亲'),
        ('Son', '儿子'),
        ('Daughter', '女儿'),
        ('Other', '其他'),
    )

    number = models.CharField(max_length=20, unique=True)  # 编号
    name = models.CharField(max_length=100)  # 姓名
    relation = models.CharField(max_length=10, choices=RELATION_CHOICES, default='Father')  # 默认关系为父亲
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')  # 默认性别为男
    age = models.IntegerField(default=0)  # 默认年龄为0
    height = models.FloatField(default=0.0)  # 默认身高为0.0
    weight = models.FloatField(default=0.0)  # 默认体重为0.0

    class Meta:
        db_table = 'PatientFamily'
