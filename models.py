from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import get_user_model
from datetime import date

class Lib_Layout(models.Model):
    Title = models.TextField()          # blank and null are the attributes of the TextField blank refers to how the field is rendered and null has to deal with the database
    Author = models.TextField()
    Publisher = models.TextField()
    Price = models.IntegerField()
    Issued = models.CharField(max_length=5, choices=[('yes', 'Yes'), ('no', 'No')], default='no')
    issue_date = models.DateField(auto_now_add=True)
    # Issued = models.BooleanField(default=False)
    # Issued = models.CharField(max_length=3, default='no')

class createSubAdminForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']

        def save(self, commit=True):
            user = super().save(commit=False)
            user.user_type = 'subadmin'
            if commit:
                user.save()
            return user

class loginUser(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password']

class createUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']


Ibook = get_user_model()

class IssuedBook(models.Model):
    user = models.ForeignKey(Ibook, on_delete=models.CASCADE)
    book_title = models.CharField(max_length=100)
    issue_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    def calculate_fine(self):
        allowed_days = 7  # Free borrowing period
        fine_per_day = 10  # ₹10 per day

        today = date.today()
        return_date = self.return_date or today

        total_days = (return_date - self.issue_date).days
        overdue_days = max(0, total_days - allowed_days)
        return overdue_days * fine_per_day
