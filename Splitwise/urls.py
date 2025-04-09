"""
URL configuration for Splitwise project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from Splitz.views import *

def redirect_to_home(request):
    return redirect('home')


urlpatterns = [
    
    path('admin/', admin.site.urls),

    path("",redirect_to_home),
    path('Splitwise',HomeView.as_view(),name='home'),
    path('Splitz/userpage/',UserpageView.as_view(),name='userpage'),

    path('Splitz/signup/',UserRegistration_view.as_view(),name='signup'),
    path('Splitz/login/',LogIn_view.as_view(),name='login'),
    path('Splitz/logout/',LogOut_View.as_view(),name='logout'),

    path('Splitz/add_expense/',AddExpense_view.as_view(),name='add_expense'),
    path('Splitz/expense_list/',ExpenseList_view.as_view(),name='expense_list'),
    path('Splitz/expense_detail/<int:pk>',ExpenseDetail_view.as_view(),name='expense_detail'),
    path('Splitz/expense_delete/<int:pk>',ExpenseDelete_view.as_view(),name='expense_delete'),
    path('Splitz/expense_update/<int:pk>',ExpenseUpdate_view.as_view(),name='expense_update'),

    path('Splitz/expense_settle/',Settlement_view.as_view(),name='settle'),
    path('Splitz/settles_read/',SettlementRead_view.as_view(),name='settle_read'),
    path('Splitz/settle_update/<int:pk>',Settlement_update_view.as_view(),name='settle_update'),
    path('Splitz/settle_delete/<int:pk>',Settle_delete_view.as_view(),name='settle_delete'),
    path('Splitz/forgot/',Forgotpasswordview.as_view(),name='forgot'),
    path('Splitz/otp_verification/',OTPverificationview.as_view(),name='otp'),
    path('Splitz/password_change/',PasswordChangeview.as_view(),name='pass_change'),

    path('Splitz/premium/',PremiumView.as_view(),name='premium')

]
