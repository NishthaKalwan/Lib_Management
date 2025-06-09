#view handles our request and various web pages
from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


from .models import Lib_Layout, createSubAdminForm, createUserForm, IssuedBook  # import book        **************************
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decorators import admin


class loginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)

def loginPage(request):
    form=loginForm(request.POST or None)
    if request.method=='POST':
       if form.is_valid():
           username=form.cleaned_data.get('username')
           password=form.cleaned_data.get('password')

           user = authenticate(request, username=username, password=password)
           if user is not None:
               login(request, user)
               return redirect('home')
    context={'form':form}
    return render(request, 'loginPage.html',context)

@admin(allowed_roles=['Admin'])
def SubAdminRegisterPage(request):
    if request.method=='POST':
        form = createSubAdminForm(request.POST) # throw that data into form     ****************************
        if form.is_valid():
            un=form.cleaned_data.get('username')
            messages.success(request,'Account Created for '+un)
            form.save()
            return redirect('login')
    else:
        form = createSubAdminForm()
    context={    'form':form    }
    return render(request,'SubAdminRegister.html',context)

def UserRegisterPage(request):
    if request.method=='POST':
        form=createUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form=createUserForm()
    context={'form':form}
    return render(request,'userRegister.html',context)

def logoutUser(request):
    logout(request)
    return  redirect('login')


# @admin(allowed_roles=['Admin'])
def userPage(request):
    content={}
    return render(request,'user.html',content)

@login_required(login_url='login')
# @admin(allowed_roles=['Admin'])
# @subadmin(allowed_roles=['Sub_admins'])

def home(request):
    # title = get_title()

    return render(request,'home.html' , {})

@login_required(login_url='login')
# @admin(allowed_roles=['Admin'])
def book_do(request):
    #book_title = get_object_or_404(Lib_Layout , Title=title)
    text={
     #   'book_title' : book_title,
        'txt' : 'add new book or check the books list'
    }
    return render(request,'do_book.html',text)

@login_required(login_url='login')
@admin(allowed_roles=['Admin'])
# @admin(allowed_roles=['Admin'])
def book_add(request):
    class Book_Form(forms.ModelForm):  # form create krega to take details from user and to display that form we have to render a html page
        class Meta:
            model = Lib_Layout
            fields = ['Title', 'Author', 'Publisher', 'Price', 'Issued']

    if request.method=='POST':                      #POST is to submit the data as request object determine if the form submission(post) or just showing the form(GET)
        Book =Book_Form(request.POST)               # object of Book_Form class
        if Book.is_valid():
            Book.save()
            return redirect('create') #to get a clear fields to enter new book
        else:
            print(Book.errors)
    else:
        Book=Book_Form(request.POST)

    context={                                           #context is used to render its data on the page
        "new_book": Book,                               #new_book and name both are variable storing the object Book and string respectively
        'name' : 'Nishtha',
    }
    return render(request, 'add_book.html',context)

@login_required(login_url='login')
# @admin(allowed_roles=['Admin'])
def book_update(request,title):         #request :An object that contains data sent by the user (like GET or POST), title:  A parameter passed in the URL. used to identify which book to update (eg update/Harry%20Potter)
    class UpdateForm(forms.ModelForm):
        class Meta:
            model = Lib_Layout          #telling  django that this model is connected to Lib_Layout
            fields = ['Title', 'Author', 'Publisher', 'Price', 'Issued']
    book = get_object_or_404(Lib_Layout, Title=title)               # This line tries to find a book where Title == title from the URL., title: This is the value from the URL.
    if request.method == 'POST':
        form = UpdateForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('create')  # or redirect to detail view
    else:
        form = UpdateForm(instance=book)
    return render(request, 'update_book.html', {'form': form})

@login_required(login_url='login')
@admin(allowed_roles=['Admin'])
# @admin(allowed_roles=['Admin'])
# @subadmin(allowed_roles=['Sub_admins'])

def book_delete(request,title):
        book = get_object_or_404(Lib_Layout,Title=title )
        book.delete()
        return redirect('books')  # change this to the name of your list page

@login_required(login_url='login')
# @admin(allowed_roles=['Admin'])
# @subadmin(allowed_roles=['Sub_admins'])
def search(request):
    book_title = None               #directly passing the variable from if statements to contxt is throwing error so we first made variables these three with initial values
    all_books = []
    show_books = False

    if request.method == 'POST':
        user_searched_book = request.POST.get('searched_book')
        book_title = Lib_Layout.objects.filter(Title = user_searched_book)
        if 'show_books' in request.POST:    # means whether the button is pressed
            show_books = True
            all_books = Lib_Layout.objects.all()

    context = {
        's_book' : book_title,
        'all_books' : all_books,
        'show_books' : show_books,
    }

    return render(request , 'search_book.html' , context)

@login_required(login_url='login')
# @admin(allowed_roles=['Admin'])

def detail_book(request , title):
    book = get_object_or_404(Lib_Layout , Title=title)
    context = {
        'book' : book
    }
    return render(request, 'details.html', context)

@login_required(login_url='login')
# @admin(allowed_roles=['Admin'])

def navbar(request):
    return render(request,'navbar.html',{})


# @user(allowed_roles=['Users'])
def book_contact(request):
    text={
        'txt' : 'Here are some contact details. feel free to contact when its super urgent.',
    }
    return render(request,'contact.html', text)




def view_issued_books(request):
    issued_books = IssuedBook.objects.filter(user=request.user)
    books_with_fine = []

    for book in issued_books:
        fine = book.calculate_fine()
        books_with_fine.append((book, fine))

    return render(request, 'issued_books.html', {'books_with_fine': books_with_fine})



















def practice(request):
    obj=Lib_Layout.objects.get(all)
    # context={
    #     'obj_title': obj.Title,
    #     'obj_issued': obj.Issued
    # }
    content={
        'object':obj
    }
    return render(request,'practice.html',content)

