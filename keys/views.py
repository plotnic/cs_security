from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from keys.models import Key
import keygen
import os
from PIL import Image

appname = 'one-time passcode'
index_page = loader.get_template('keys/index.html')
main_page =  loader.get_template('keys/index_logged.html')
get_page = loader.get_template('keys/get.html')
register_new_page = loader.get_template('keys/register_form.html')
qr_page = loader.get_template('keys/qr_page.html')
code_page = loader.get_template('keys/get_new_code.html')
forbidden_page = loader.get_template('keys/forbidden.html')
wrong_page = loader.get_template('keys/wrong_pw.html')

# Create your views here.
def details(request):
	return HttpResponse("Hello world")

def index_old(request):
#	appname = 'KEYS'
	context = RequestContext(request, {
						'appname':appname,
					}
	)
	return HttpResponse(index_page.render(context))

def exit(request):
	logout(request)
	return redirect('/keys/')
	

@login_required
def main(request):
	user_name = request.user.username
	if request.method == "POST":
		user_name = request.POST['name']
		password = request.POST['pwd']
	context = RequestContext(request, {
						'appname':appname,
						'user_name':user_name,
					}
	)
	return HttpResponse(main_page.render(context))

@login_required
def get_codes(request):
	user_name = request.user.username
	if request.method == "GET":
		rows = Key.objects.filter(user=user_name)
		context = RequestContext(request, {'user_name': user_name,
			'rows': rows})
		return HttpResponse(get_page.render(context))
	if request.method == "POST":
		app = request.POST['app']
		return generate_new_code(request, app)

@login_required
def register_new(request):
	user_name = request.user.username
	if request.method == "GET":
		context = RequestContext(request, {'user_name': user_name})
		return HttpResponse(register_new_page.render(context))
	if request.method == "POST":
		passcode = request.POST["pass"]
		if request.user.check_password(passcode):
			key = keygen.generate_key()
			if request.POST['app']:
				app = request.POST['app']
			new = Key.objects.create(user=user_name, key=keygen.encrypt_code(passcode,key), app=app)
			url = keygen.make_qr(key)
			context = RequestContext(request, {'user_name': user_name,
				'url': url, 'app': app})
			return HttpResponse(qr_page.render(context))
		else:
			context = RequestContext(request, {'user_name': user_name,
				'link': 'register'})
			return HttpResponse(wrong_page.render(context))

@login_required
def get_img(request, imgurl):
	response = HttpResponse(content_type="image/png")
	fn = "img/" + imgurl
	img = Image.open(fn)
	img.save(response, 'png')
	os.remove(fn)
	return response

@login_required
def generate_new_code(request, ids):
	user_name = request.user.username
	passcode = request.POST["pass"]
	auth = request.user.check_password(passcode)
	try:
		row = Key.objects.get(id=ids)
	except:
		context = RequestContext(request, {'user_name': user_name})
		return HttpResponse(forbidden_page.render(context))
	if row.user == user_name and auth:
		code = keygen.generate_code(passcode, row.key)
		context = RequestContext(request, {'user_name': user_name,
			'app': row.app, 'code': code})
		return HttpResponse(code_page.render(context))
	elif not auth:
		context = RequestContext(request, {'user_name': user_name, 
			'link': 'new'})
		return HttpResponse(wrong_page.render(context))
	else:
		context = RequestContext(request, {'user_name': user_name})
		return HttpResponse(forbidden_page.render(context))

def index(request):

	if request.method == "GET":
		if not request.user.is_authenticated() or not request.user.is_active or request.user is None:
			context = RequestContext(request, {
							'appname':appname,
							}
			)
			return HttpResponse(index_page.render(context))
		else:
			return redirect('/keys/main')
			
        if request.method == "POST":
		action = request.POST['action']
		
		# TO DO use switch here
		if action == "login":
			return user_login(request)
		else:
		        return user_register(request)
	

def user_login(request):
        user_name = request.POST['name']
        password = request.POST['pwd']
	user = authenticate(username=user_name, password=password)
              
        print('user: %s pass: %s') % (user_name, password)
        
	if user is not None:
        	if user.is_active:
                	login(request, user)
                        return redirect('/keys/main')
		else:
                        # return disabled account
                        error = "Account diabled"
                        context = RequestContext(request, {
                                                            'appname':appname,
                                                            'user_name':user_name,
                                                            'error':error,
                                                           }
			)

	else:
        	error = "Wrong username or password"
                context = RequestContext(request, {
                                                        'appname':appname,
                                                        'user_name':user_name,
                                                        'error':error,
                	                          }
                )
	return HttpResponse(index_page.render(context))

def user_register(request):
        user_name = request.POST['name']
        password = request.POST['pwd']
	try:
		u = User.objects.create_user(user_name, 'test@mit.edu', password)
		u.save()
		user = authenticate(username=user_name, password=password)
		login(request, user)
	except:
		error = 'Can\'t register a new user' 
		context = RequestContext(request, {
							'appname':appname,
							'error':error,
						  }
                        )
		return HttpResponse(index_page.render(context))
	
	return redirect('/keys/main')


