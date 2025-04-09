from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Expense_model(models.Model):

    amount = models.DecimalField(max_digits=10,decimal_places=2)

    created_date = models.DateTimeField(auto_now_add=True)

    user_id = models.ForeignKey(User,on_delete=models.CASCADE)

    description = models.TextField()

    bill_image = models.ImageField(upload_to="Bill_Images",null=True,blank=True)


class SplitModel(models.Model):

    user_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name='split_users')

    expense_id = models.ForeignKey(Expense_model,on_delete=models.CASCADE,related_name='split_expense')

    split_amount = models.DecimalField(max_digits=10,decimal_places=2)

    status = models.BooleanField(default=False)


class SettlementModel(models.Model):

    payer = models.ForeignKey(User,on_delete=models.CASCADE,related_name='payer')

    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='receiver')

    settled_amount = models.DecimalField(max_digits=10,decimal_places=2)

    payed_on = models.DateField(auto_now_add=True)


class BalanceModel(models.Model):

    amount_payer = models.ForeignKey(User,on_delete=models.CASCADE,related_name="am_payer")

    amount_receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name="am_receiver")

    balance_amount = models.DecimalField(max_digits=10,decimal_places=2)