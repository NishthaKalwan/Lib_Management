"""
URL configuration for Books project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# from book.models import loginUser
from book.views import home, book_add, book_contact, book_do, book_delete, book_update, search, navbar, practice, \
    detail_book, SubAdminRegisterPage, loginPage, logoutUser, UserRegisterPage, view_issued_books

urlpatterns = [
    path('admin/', admin.site.urls),
# ('any name for url' ,function name in view.py , for direction {%url..%})

    path('',loginPage,name='login'),
    path('home/',home,name='home'), #/login/create

    path('books/',book_do, name='books'),     # which-> CRUD

    path('create/',book_add , name='create'),                   # C
    path('search/',search,name='search'),                       # R
    path('update/<str:title>',book_update,name='update'),       # U
    path('delete/<str:title>',book_delete, name='delete'),  # D
    path('details/<str:title>' , detail_book , name='d_book'),
    path('navbar/',navbar,name='navbar'),
    path('home/contact/',book_contact, name='contact') ,
    path('logout/',logoutUser,name='logout'),
    path('SubAdminRegistration/',SubAdminRegisterPage,name='SubAdminregister'),
    path('UserRegistration/',UserRegisterPage,name='UserRegister'),
    path('practice/',practice,name='practice'),
    path('IssueDetails',view_issued_books,name='view_issued_books')
]
