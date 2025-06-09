
from django.http import HttpResponse
from django.shortcuts import redirect

def admin(allowed_roles=[]):
    # if allowed_roles is None:
      #  allowed_roles = []
    def decorator(view_func):
        def wrapper_func(request, *args,**kwargs):
            group=None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request,*args,**kwargs)
            else:
                return HttpResponse('you are not authorised for this functionality')
        return wrapper_func
    return decorator

#
# def user(allowed_roles=[]):
#
#     def decorator(view_func):
#         def wrapper_func(request, *args,**kwargs):
#             group=None
#             if request.user.groups.exists():
#                 group=request.user.groups.all()[0].name
#             if group in allowed_roles:
#                 return view_func(request,*args,**kwargs)
#             else:
#                 return HttpResponse('you r not authorised for this functionality')
#         return wrapper_func
#     return decorator

# unauthenticated user(i.e. sub admins)-> can do search only
#authenticated users (i.e. admins)->can do all the operations
   # if request.user.is_authenticated:
        #     return  redirect('home')