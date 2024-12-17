from django.http import HttpResponse
from .models import Admin,UserPatient,UserDoctor,Department,Order,PatientFamily
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max
import json
def Alllogin(request):
    return render(request, 'HIS/alllogin.html')
@csrf_exempt
def Doctor_loginfirst(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')  # 使用身份证号作为密码

        try:
            # 查询医生信息
            doctor = UserDoctor.objects.get(name=username, id_card=password, status=1)

            # 创建或获取用户对象
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password(password)  # 将身份证号作为密码
                user.save()

            # 使用 Django 的 login 函数保存会话
            login(request, user)

            return JsonResponse({
                'success': True,
                'message': '登录成功',
                'doctor': {
                    'id': doctor.id,
                    'name': doctor.name,
                    'department': doctor.department.name,
                }
            })
        except UserDoctor.DoesNotExist:
            return JsonResponse({'success': False, 'message': '账号或密码错误'}, status=400)

    return JsonResponse({'message': '仅支持 POST 请求'}, status=405)
def index(request):
    return render(request, 'HIS/index.html')
def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success', 'message': '登录成功'})
        else:
            return JsonResponse({'status': 'error', 'message': '用户名或密码错误'})
    return render(request, 'HIS/login.html')
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserDoctor, Order

@csrf_exempt
def Doctor_page(request):
    if request.method == 'POST':
        # 修改医生信息
        try:
            data = json.loads(request.body)

            # 如果请求是删除预约
            if data.get('action') == 'delete_appointment':
                appointment_id = data.get('appointment_id')
                if appointment_id:
                    try:
                        Order.objects.get(id=appointment_id).delete()
                        return JsonResponse({'success': True, 'message': '预约已删除'})
                    except Order.DoesNotExist:
                        return JsonResponse({'success': False, 'message': '预约不存在'}, status=404)
                else:
                    return JsonResponse({'success': False, 'message': '未提供预约 ID'}, status=400)

            # 处理修改医生信息的逻辑
            username = request.user.username
            doctor = UserDoctor.objects.get(name=username)

            doctor.id_card = data.get('id_card', doctor.id_card)
            doctor.department.name = data.get('department', doctor.department.name)
            doctor.status = 1 if data.get('status', '在职') == '在职' else 0
            doctor.save()

            return JsonResponse({'success': True, 'message': '个人信息已更新'})
        except UserDoctor.DoesNotExist:
            return JsonResponse({'success': False, 'message': '医生信息不存在'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'发生错误: {str(e)}'}, status=500)

    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # AJAX 请求，返回医生和预约信息
        try:
            username = request.user.username
            doctor = UserDoctor.objects.get(name=username)

            doctor_data = {
                'id': doctor.id,
                'name': doctor.name,
                'id_card': doctor.id_card,
                'department': doctor.department.name if doctor.department else '未分配',
                'status': '在职' if doctor.status == 1 else '离职',
            }

            appointments = Order.objects.filter(doctor=doctor)
            appointments_data = [
                {
                    'id': order.id,
                    'name': order.name,
                    'gender': '男' if order.gender == 'M' else '女',
                    'age': order.age,
                    'phone_number': order.phone_number,
                    'id_card': order.id_card,
                    'department': order.department.name if order.department else '未分配',
                }
                for order in appointments
            ]

            return JsonResponse({'doctor': doctor_data, 'appointments': appointments_data})
        except UserDoctor.DoesNotExist:
            return JsonResponse({'error': '医生信息不存在'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'发生错误: {str(e)}'}, status=500)

    return render(request, 'HIS/doctor-page.html')

def Register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # 验证两次密码是否一致
        if password != confirm_password:
            return render(request, 'HIS/register.html', {'error': '两次密码输入不一致！'})

        # 检查用户名是否已存在
        if User.objects.filter(username=username).exists():
            return render(request, 'HIS/register.html', {'error': '用户名已存在！'})

        # 创建新用户
        User.objects.create_user(username=username, password=password)
        return redirect('login')  # 注册成功后跳转到登录页面

        # 如果是 GET 请求，返回注册页面
    return render(request, 'HIS/register.html')
def Main_page(request):
    return render(request, 'HIS/main-page.html')
def Account(request):
    return render(request, 'HIS/account.html')
@csrf_exempt
def Build_personalfile(request):
    if request.method == 'GET':
        # 返回填写健康档案的页面
        return render(request, 'HIS/build-personalfile.html')

    elif request.method == 'POST':
        try:
            # 解析前端发送的数据
            data = json.loads(request.body)

            # 遍历数据并存储到数据库
            for record in data:
                UserPatient.objects.update_or_create(
                    name=record['name'],
                    defaults={
                        'gender': 'M' if record['gender'] == '男' else 'F',
                        'age': int(record['age']),
                        'height': float(record['height']),
                        'weight': float(record['weight']),
                        'phone_number': record['phone'],
                    }
                )

            return JsonResponse({'status': 'success', 'message': '档案已成功保存！'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    else:
        # 返回错误提示
        return JsonResponse({'status': 'error', 'message': '无效的请求方法'})
@csrf_exempt
def Personalfile(request):
    if request.method == 'GET':
        # 从数据库获取所有档案数据
        records = UserPatient.objects.all()
        data = [
            {
                'name': record.name,
                'gender': '男' if record.gender == 'M' else '女',
                'age': record.age,
                'height': record.height,
                'weight': record.weight,
                'phone': record.phone_number,
            }
            for record in records
        ]
        # 将数据传递给模板
        return render(request, 'HIS/personalfile.html', {'records': data})

@csrf_exempt
def Familyfile(request):
    if request.method == 'GET':
        # 查询所有记录
        records = PatientFamily.objects.all()
        data = [
            {
                'number': record.number,
                'name': record.name,
                'relation': dict(PatientFamily.RELATION_CHOICES).get(record.relation, '未知'),
                'gender': record.gender,
                'age': record.age,
                'height': record.height,
                'weight': record.weight,
            }
            for record in records
        ]
        if request.headers.get('Accept') == 'application/json':
            return JsonResponse(data, safe=False)
        return render(request, 'HIS/familyfile.html', {'records': data})

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)

            # 查询当前最大编号
            max_number = PatientFamily.objects.aggregate(Max('number'))['number__max']
            # 如果没有记录，设置新编号为 1；否则，将当前最大编号加 1
            new_number = str(int(max_number) + 1) if max_number else "1"

            # 添加记录
            PatientFamily.objects.create(
                number=new_number,
                name=data['name'],
                relation=data['relation'],
                gender=data['gender'],
                age=data['age'],
                height=data['height'],
                weight=data['weight'],
            )
            return JsonResponse({'status': 'success', 'message': '记录已成功添加', 'new_number': new_number})
        except KeyError as e:
            return JsonResponse({'status': 'error', 'message': f"缺少必要字段: {str(e)}"}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            record = get_object_or_404(PatientFamily, number=data['number'])
            record.name = data.get('name', record.name)
            record.relation = data.get('relation', record.relation)
            record.gender = data.get('gender', record.gender)
            record.age = data.get('age', record.age)
            record.height = data.get('height', record.height)
            record.weight = data.get('weight', record.weight)
            record.save()
            return JsonResponse({'status': 'success', 'message': '记录已成功更新'})
        except KeyError as e:
            return JsonResponse({'status': 'error', 'message': f"缺少必要字段: {str(e)}"}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    elif request.method == 'DELETE':
        try:
            # 打印接收到的请求体
            print("Raw request body:", request.body)

            # 尝试解析 JSON 数据
            data = json.loads(request.body)
            print("Parsed data:", data)

            # 获取编号
            record_number = data.get('number')
            print("Record number to delete:", record_number)

            if not record_number:
                return JsonResponse({'status': 'error', 'message': '编号不能为空'}, status=400)

            # 查询记录
            record = get_object_or_404(PatientFamily, number=record_number)
            print(f"Deleting record: {record}")
            record.delete()
            return JsonResponse({'status': 'success', 'message': '记录已成功删除'})
        except json.JSONDecodeError as e:
            print("JSON Decode Error:", str(e))
            return JsonResponse({'status': 'error', 'message': '请求体不是有效的 JSON'}, status=400)
        except PatientFamily.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '记录不存在'}, status=404)
        except Exception as e:
            print("Unexpected error during delete:", str(e))
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': '请求方法不支持'}, status=405)
@csrf_exempt
def Inquire(request):
    if request.method == 'GET':
        # 获取身份证号
        user_id_card = request.GET.get('id_card')

        if user_id_card:
            try:
                # 查询预约信息
                order = Order.objects.get(id_card=user_id_card)
                data = {
                    'name': order.name,
                    'gender': '男' if order.gender == 'M' else '女',
                    'age': order.age,
                    'phone': order.phone_number,
                    'id_card': order.id_card,
                    'department': order.department.name if order.department else '未选择',
                    'doctor': order.doctor.name if order.doctor else '未选择',
                }
                return render(request, 'HIS/inquire.html', {'order': data})
            except Order.DoesNotExist:
                # 返回未找到预约的错误信息
                return render(request, 'HIS/inquire.html', {'error_message': '未找到预约信息，请重新输入身份证号。'})

        # 如果未提供身份证号，返回默认查询页面
        return render(request, 'HIS/inquire.html')

    elif request.method == 'POST':
        # 取消预约功能
        user_id_card = request.POST.get('id_card')

        if not user_id_card:
            return JsonResponse({'status': 'error', 'message': '未提供身份证号'}, status=400)

        try:
            # 查找预约信息
            order = Order.objects.get(id_card=user_id_card)
            order.delete()
            return JsonResponse({'status': 'success', 'message': '预约已成功取消'})
        except Order.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '未找到预约信息，无法取消'}, status=404)
        except Exception as e:
            # 返回异常信息
            return JsonResponse({'status': 'error', 'message': f'操作失败：{str(e)}'}, status=500)

    # 其他方法不支持
    return JsonResponse({'status': 'error', 'message': '请求方法不支持'}, status=405)

def Online_register(request):
    if request.method == 'GET':
        # 检查是否有科室ID，用于返回医生数据
        department_id = request.GET.get('department_id')
        if department_id:
            # 返回对应科室的医生信息
            doctors = UserDoctor.objects.filter(department_id=department_id).values('id', 'name')
            return JsonResponse({'doctors': list(doctors)})

        # 如果没有 department_id，则渲染页面
        departments = Department.objects.all()
        return render(request, 'HIS/online-register.html', {
            'departments': departments,
        })

    elif request.method == 'POST':
        try:
            # 获取表单数据
            name = request.POST.get('name')
            gender = request.POST.get('gender')
            age = int(request.POST.get('age', 0))
            phone_number = request.POST.get('phone_number')
            id_card = request.POST.get('id_card')
            department_id = request.POST.get('department')
            doctor_id = request.POST.get('doctor')

            # 获取科室和医生对象
            department = Department.objects.get(id=department_id) if department_id else None
            doctor = UserDoctor.objects.get(id=doctor_id) if doctor_id else None

            # 保存数据到数据库
            Order.objects.create(
                name=name,
                gender=gender,
                age=age,
                phone_number=phone_number,
                id_card=id_card,
                department=department,
                doctor=doctor,
            )

            # 返回成功页面或重定向
            return render(request, 'HIS/inquire.html')

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    else:
        return JsonResponse({'status': 'error', 'message': '请求方法不支持'}, status=405)