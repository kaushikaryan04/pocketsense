from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ExpenseGroup(models.Model) :
    group_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    members  = models.ManyToManyField(User , related_name = 'expense_groups')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return f'{self.group_name}'



class Expense(models.Model):
    SPLIT_TYPE = (
        ('EQUAL' ,'EQUAL'),
        ('EXACT' , 'EXACT'),
    )
    expense_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10 , decimal_places=2)
    shared_equally = models.BooleanField(default=True)
    paid_by = models.ForeignKey(User , on_delete=models.CASCADE , related_name='expenses_paid')
    created_at = models.DateTimeField(auto_now_add=True)
    split_type = models.CharField(max_length = 20 , choices = SPLIT_TYPE , default = 'EQUAL')
    group = models.ForeignKey(ExpenseGroup , on_delete=models.CASCADE , related_name='expenses')

    def __str__(self) :
        return f'{self.expense_name}'

class ExpenseSplit(models.Model) :
    expense = models.ForeignKey(Expense , on_delete=models.CASCADE , related_name='splits')
    is_paid = models.BooleanField(default = False)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    share_amount = models.DecimalField(max_digits=10 , decimal_places=2)
    owed_to = models.ForeignKey(User , on_delete=models.CASCADE , related_name='owed_to' , null=False , blank=False)

    class Meta :
        unique_together = ('expense' , 'user')

    def __str__(self ) :
        return f'{self.expense} - {self.user}'

class Settlement(models.Model) :
    from_user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='settlements_paid')
    to_user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='settlements_received')
    amount = models.DecimalField(max_digits=10 , decimal_places=2)
    split = models.ForeignKey(ExpenseSplit , on_delete=models.CASCADE , related_name='settlements',null = False , blank = False)
    date = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=100 , blank=True)

    def __str__(self) :
        return f'{self.from_user.username} - {self.to_user.username} - {self.amount}'
