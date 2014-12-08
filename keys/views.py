from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

appname = '<no name app>'
index_page = loader.get_template('keys/index.html')
main_page =  loader.get_template('keys/index_logged.html')

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

