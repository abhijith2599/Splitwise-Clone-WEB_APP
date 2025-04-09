from django.shortcuts import render,redirect 
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

from django.views.generic import View,CreateView,DeleteView,UpdateView,DetailView,ListView,UpdateView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password
# from django.contrib.auth.decorators import login_required      # we cant use here now , bcz it donot have a redirect in it. we can use it when we use react

from Splitz.models import *
from Splitz.forms import *

import random

# Create your views here. 
# webo ppeb wzqf modv
# rzp_test_2KDmLYLam63pfJ     razor pay key_id
# 54Z49MqvChA06KNsnkubIi2u    razor pay key_secret


                ###         DECORATORS          ###

def is_user(fn):         # this decorator is to check if the actions like update , delete is performed by the same user who created it

    def wrapper(request,**kwargs):

        data = Expense_model.objects.get(id = kwargs.get('pk'))

        if data.user_id == request.user:

            return fn(request,**kwargs)
        
        return redirect('login')
    
    return wrapper


def is_login(fn):                   # this is to check if the a user is login, before doing any actions

    def wrapper(request):

        if request.user.is_authenticated:

            return fn(request)
        
        return redirect('login')

    return wrapper



                    ###         MAIN PAGES          ###

class HomeView(View):

    def get(self,request):

        return render(request,'home.html')
    
    
@method_decorator(decorator=is_login,name='dispatch')
class UserpageView(View):

    def get(self,request):

        return render(request,'userpage.html')




                    ###         USER CREDENTIALS            ###

class LogOut_View(View):

    def get(self,request):

        logout(request)

        return redirect('login')


class UserRegistration_view(View):

    def get(self,request):

        form = UserRegister_form

        return render(request,'signup.html',{'form':form})
    
    def post(self,request):

        form = UserRegister_form(request.POST)

        if form.is_valid():

            User.objects.create_user(**form.cleaned_data)

            subject = 'Splitwise welcome mail'
            message = f"Hii {form.cleaned_data['username']} welcome to splitwise"
            from_email = 'abhijithdplr@gmail.com'
            recipient_list = [form.cleaned_data['email']]
            send_mail(subject,message,from_email,recipient_list,fail_silently=True)
            return redirect('home')
        
        return render(request,'signup.html',{'form':form})


class LogIn_view(View):

    def get(self,request):

        form = Login_form

        return render(request,'login.html',{'form':form})
    
    def post(self,request):

        form = Login_form(request.POST)

        if form.is_valid():

            u_name = form.cleaned_data['username']

            pass_id = form.cleaned_data['password']

            user_obj = authenticate(request,username=u_name,password=pass_id)

            if user_obj:

                login(request,user_obj)

                messages.success(request,'Logged in Succesfully')
                return render(request,'userpage.html')

        messages.warning(request,'Invalid Username or Password')
            
        return redirect('login')
    


                ###         FOR EXPENSE         ###

@method_decorator(decorator=is_login,name='dispatch')
class AddExpense_view(View):

    def get(self,request):

        form = Expense_form

        return render(request,"add_expense.html",{'form':form})
    
    def post(self,request):

        form = Expense_form(request.POST)

        if form.is_valid():

            amount = form.cleaned_data.get('amount')

            users = User.objects.exclude(id = request.user.id)
            
            split_amount = amount/(users.count()+1)
        
            expense = Expense_model.objects.create(**form.cleaned_data, user_id = request.user)

            for i in users:

                SplitModel.objects.create(user_id = i, expense_id = expense, split_amount = split_amount)

                balance,created = BalanceModel.objects.get_or_create(amount_payer = i, amount_receiver =request.user,defaults={'balance_amount':split_amount})

                if not created:

                    balance.balance_amount += split_amount

                    balance.save()

            return redirect('expense_list')

    # model = Expense_model

    # form_class = Expense_form

    # template_name = "add_expense.html"

    # success_url = reverse_lazy('signup')

    # def form_valid(self, form):

    #     form.instance.user_id = self.request.user
    #     return super().form_valid(form)
    
    # def form_invalid(self, form):           # this is o redirect to another webpage if the form is invalid
    #     return HttpResponseRedirect(reverse_lazy('signup'))


# @method_decorator(decorator=is_login,name='dispatch')
@method_decorator(decorator=is_user,name='dispatch')
class ExpenseUpdate_view(View):     # (UpdateView)

    # model = Expense_model

    # form_class = Expense_form

    # template_name = "expense_update.html"

    # success_url = reverse_lazy('expense_list')

    def get(self,request,**kwargs):           # we are updatting a  expense here , kwargs contain alreday created expense id , we are updatting it

        data = Expense_model.objects.get(id = kwargs.get('pk'))             # getting the data with that expanse_id

        form = Expense_form(instance=data)          ## showing that data in the form

        return render(request,'expense_update.html',{'form':form})
    
    def post(self,request,**kwargs):

        data = Expense_model.objects.get(id = kwargs.get('pk'))

        form = Expense_form(request.POST,instance=data)

        if form.is_valid():

            form.user_id = request.user     # updatting the expense ,adding the FK

            form.save()


            amount = form.cleaned_data.get('amount')    # getting the updatted amount
            
            data = SplitModel.objects.filter(expense_id = kwargs.get('pk'))     #  gettig the split datas with the expense id's matching

            # updating balance amount

            for i in data:    # for getting the slpit amount of the specific expense

                old_split_amount  = i.split_amount
                break

            existing_balance = BalanceModel.objects.filter(amount_receiver = request.user)   # removing the existing split of expense id

            for i in existing_balance:

                for j in data:

                    if i.amount_payer == j.user_id:
                        i.balance_amount -= old_split_amount
                        i.save()

            new_split_amount = amount/(data.count() + 1)

            for i in data:
            
                i.split_amount = new_split_amount
                i.save()

                for j in existing_balance:
                    if j.amount_payer == i.user_id:
                        j.balance_amount += i.split_amount
                        j.save()
                        break
                
            return redirect('expense_list')


@method_decorator(decorator=is_login,name='dispatch')
class ExpenseList_view(ListView):    # to list out all the expenses created by the users in auth_user

    model = Expense_model

    template_name = "expense_list.html"

    context_object_name = "data"

    # def get_queryset(self):                           # to display only the list of expensees added by the logged user, we can create another
    #                                             # view to show this, 
    #     return Expense_model.objects.filter(user_id = self.request.user)
    

@method_decorator(decorator=is_login,name='dispatch')
@method_decorator(decorator=is_user,name='dispatch')
class ExpenseDetail_view(DetailView):      # to get the details of a specific expense that is created by the logged in user

    model = Expense_model

    template_name = "expense_detail.html"

    context_object_name = "data"



@method_decorator(decorator=is_login,name='dispatch')
@method_decorator(decorator=is_user,name='dispatch')
class ExpenseDelete_view(View):

    def get(self,request,**kwargs):

        Expense_model.objects.get(id = kwargs.get('pk'),user_id = request.user).delete()   # if the object doesn't  exist it will raise an error,
                                # to avoid use get_object_404
        
        return redirect('expense_list')
    

    

                            ###             FOR SETTLEMENT                  ###

class Settlement_view(View):      # to settle the amount 

    def get(self,request,**kwargs):

        form = Settle_form

        return render(request,'settlement.html',{'form':form})
    
    def post(self,request,**kwargs):

        form = Settle_form(request.POST)

        if form.is_valid():

            SettlementModel.objects.create(**form.cleaned_data,payer=request.user)
            amount = form.cleaned_data.get('settled_amount')
            amt_receiver = form.cleaned_data.get('receiver')
            u_name = User.objects.get(username = amt_receiver)

            data = BalanceModel.objects.get(amount_payer=request.user,amount_receiver=u_name)

            if data:

                if data.balance_amount >= amount:

                    data.balance_amount -= amount
                    data.save()
                    if data.balance_amount == 0:
                        data.delete()

        return redirect('settle_read')


class SettlementRead_view(View):    # to see all the settlements done by the logged in user

    def get(self,request):

        data = SettlementModel.objects.filter(payer = request.user)

        return render(request,'settle_view.html',{'data':data})
    

class SettlementUnique_view(View):    # when the settlements are listed and clicking on one specific shows more data about it { not necessary }

    def get(self,request,**kwargs):

        data = SettlementModel.objects.get(id = kwargs.get('pk'))

        return render(request,'settle_unique.html',{'data':data})


class Settlement_update_view(View):

    def get(self,request,**kwargs):

        data = SettlementModel.objects.get(id = kwargs.get('pk'))

        form = Settle_form(instance=data)  

        return render(request,'settle_update.html',{'form':form})  

    def post(self,request,**kwargs):

        data = SettlementModel.objects.get(id = kwargs.get('pk'))

        form = Settle_form(request.POST,instance=data)   

        if form.is_valid():

            form.save()

        return redirect('settle_read') 


class  Settle_delete_view(View):

    def get(self,request,**kwargs):

        SettlementModel.objects.get(id = kwargs.get('pk')).delete()

        return redirect('settle_read')


                    ###         OTP             ###

class Forgotpasswordview(View):

    def get(self,request):

        form = ForgotForm

        return render(request,'forgot.html',{'form':form})
    
    def post(self,request):

        form = ForgotForm(request.POST)

        user = User.objects.get(username = request.POST.get('username'))

        otp = random.randint(1000,9999)

        request.session['otp'] = otp

        request.session['username'] = user.username

        send_mail(subject='password change',message=str(otp),from_email="abhijithdplr@gmail.com",recipient_list=[user.email])

        return redirect('otp')
    

class OTPverificationview(View):

    def get(self,request):

        form = OTPform

        return render(request,'otp.html',{'form':form})
    
    def post(self,request):

        # form = OTPform(request.POST)

        entered_otp = request.POST.get('otp')

        if int(entered_otp) == request.session.get('otp'):

            return redirect('pass_change')
        
        else:

            return redirect('forgot')
        

class PasswordChangeview(View):

    def get(self,request):

        form = PasswordChangeform

        return render(request,'new_pass.html',{'form':form})
    
    def post(self,request):

        form = PasswordChangeform(request.POST)

        if form.is_valid():

            new = form.cleaned_data.get('new_password')

            confirm  = form.cleaned_data.get('confirm_password')

            if new == confirm:

                user = User.objects.get(username = request.session.get('username'))
                user.password = make_password(new)                         #  we can use user.set_password('new'), we don't need to import it
                user.save()
                return redirect('login')
            
            return redirect('pass_change')


            ###         PREMIUM         ###
# rzp_test_2KDmLYLam63pfJ     razor pay key_id
# 54Z49MqvChA06KNsnkubIi2u    razor pay key_secret

RZP_KEY_ID = "rzp_test_2KDmLYLam63pfJ"
RZP_KEY_SECRET = "54Z49MqvChA06KNsnkubIi2u"

import razorpay
class PremiumView(View):

    def get(self,request):

        client = razorpay.Client(auth=(RZP_KEY_ID, RZP_KEY_SECRET))
        user = request.user
        # data = { "amount": 500, "currency": "INR", "receipt": "order_rcptid_11" }

        payment = client.order.create(data = {'amount':100,
                                            'currency':'INR'})
        print(payment)
        return redirect('signup')