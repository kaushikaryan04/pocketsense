from django.urls import path
from .views import RegisterUserView , create_group, ExpenseView, settle_expense

urlpatterns = [
    path('api/register' ,RegisterUserView.as_view(), name = 'register-user' ),
    path('api/create-group' , create_group , name = 'create-group'),
    path('api/expense' , ExpenseView.as_view() , name = 'expense'),
    path('api/settle' , settle_expense , name = 'settle-expense')

]
