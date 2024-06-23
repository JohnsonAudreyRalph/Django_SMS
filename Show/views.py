from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import User_manager
from django.contrib import messages
from django.views import View
import random

# Create your views here.
class Login(View):
    def get(self, request):
        return render(request, 'Login.html')
    def post(self, request):
        if request.method == "POST":
            username = request.POST.get('UserName')
            Password = request.POST.get('Password')
            print(username, Password)
            user = authenticate(username=username, password=Password)
            if user is not None:
                login(request, user)
                messages_ = username
                return redirect('index/', {'messages':username})
            else:
                try:
                    # Kiểm tra điều kiện tên người dùng nhập vào có tồn tại hay không
                    User.objects.get(username=username)
                    # Nếu người dùng có tồn tại, nhưng mật khẩu sai ==> Reload lại trang web để người dùng đăng nhập lại
                    messages.error(request, "Sai thông tin đăng nhập!!!!")
                    return redirect('/')
                except User.DoesNotExist:
                    messages.error(request, "Không tồn tại tài khoản này")
                    return redirect('/')

class Register(View):
    def get(self, request):
        return render(request, 'Register.html')
    def post(self, request):
        if request.method == "POST":
            Username = request.POST.get('Username')
            phone = request.POST.get('Phone_Number')
            Password = request.POST.get('Password')
            Conf_Password = request.POST.get('Conf_Password')
            if User.objects.filter(username=Username):
                messages.error(request, "Tài khoản đã tồn tại! Hãy đăng ký tài khoản khác")
                return render(request, 'Register.html')
            if Password!=Conf_Password:
                messages.error(request, "Mật khẩu không khớp!")
                return render(request, 'Register.html')
            MyUser = User.objects.create_user(Username, password=Password)
            MyUser.save()
            save_info = User_manager(user=Username, password=Password, phone_number=phone)
            save_info.save()
            return redirect('/')
        return render(request, 'Register.html')

def index(request):
	if request.method == 'POST':
		oop_code = request.POST.get('oop_code')
		if oop_code:
			user = request.user
			print(user)
			# Kiểm tra xem mã OOP có đúng hay không
			try:
				oop_obj = User_manager.objects.get(user=user)
				if oop_code == oop_obj.code:
					# Thực hiện đổi mật khẩu
					new_password = request.POST.get('new_password')
					user.set_password(new_password)
					user.save()
					# Xóa mã OOP đã sử dụng
					oop_obj.delete()
					print('Mật khẩu mới: {}'.format(new_password))
					messages.success(request, 'Mật khẩu đã được thay đổi thành công!')
					return redirect('/')
				else:
					messages.error(request, 'Mã OOP không chính xác. Vui lòng thử lại.')
					print('Mã OOP không chính xác. Vui lòng thử lại')
			except User_manager.DoesNotExist:
				print('Mã OOP không tồn tại. Vui lòng yêu cầu mã OOP mới')
				messages.error(request, 'Mã OOP không tồn tại. Vui lòng yêu cầu mã OOP mới.')
		else:
			messages.error(request, 'Vui lòng nhập mã OOP.')
	else:
		# Sinh mã OOP ngẫu nhiên khi người dùng yêu cầu thay đổi mật khẩu
		oop_code = ''.join(random.choices('0123456789', k=8))
		print('====>', oop_code)
		User_manager.objects.update_or_create(user=request.user, defaults={'code': oop_code})
	return render(request, 'index.html')
