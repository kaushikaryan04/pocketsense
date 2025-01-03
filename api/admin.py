from django.contrib import admin
from .models import Expense , ExpenseGroup , ExpenseSplit , Settlement

admin.site.register(Expense)
admin.site.register(ExpenseGroup)
admin.site.register(ExpenseSplit)
admin.site.register(Settlement)
