from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework.decorators import api_view , permission_classes
from api.models import Expense , ExpenseGroup , Settlement , ExpenseSplit
from .serializers import RegisterUserSerializer ,ExpenseSerializer
from rest_framework.response import Response
from rest_framework import views
from rest_framework import status
from django.contrib.auth.models import User
from django.db import transaction


class RegisterUserView(generics.CreateAPIView) :
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = RegisterUserSerializer

    def post(self ,request) :
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_group(request) :
    if request.method == 'POST' :
        group_name = request.data.get('group_name')
        description = request.data.get('description')
        members = request.data.get('members') # list of user ids
        if members is None or len(members) == 0 :
            print(request.data)
            print(request.POST)
            return Response({'message' : 'Members cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)
        members = User.objects.filter(id__in=members)
        group = ExpenseGroup.objects.create(group_name = group_name , description = description)
        for member in members :
            group.members.add(member)
        group.save()
        return Response({'message' : 'Group created successfully'}, status=status.HTTP_201_CREATED)


class ExpenseView(views.APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ExpenseSerializer

    def get_queryset(self, request ):
        return Expense.objects.filter(group__members=request.user)

    def get(self , request ) :
        expenses = self.get_queryset(request)
        data = self.serializer_class(expenses , many = True)
        return Response(data.data , status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self , request) :
        data = request.data
        # expense_group = ExpenseGroup.objects.get(id = data.get('group_id'))
        expense_group = get_object_or_404(ExpenseGroup , id = data.get('group_id'))

        if request.user not in expense_group.members.all() :
            return Response({'message' : 'You are not a member of this group'}, status=status.HTTP_400_BAD_REQUEST)

        if bool(data.get('shared_equally')) == False and 'exact_amount' not in data :
            return Response({'message' : 'Exact amount is required if not shared Equally'}, status=status.HTTP_400_BAD_REQUEST)

        expense = Expense.objects.create(
            expense_name = data.get('expense_name'),
            amount = float(data.get('amount')),
            shared_equally = bool(data.get('shared_equally')),
            paid_by = request.user,
            split_type = data.get('split_type'),
            group = expense_group
        )

        equal_share_amount = float(data.get('amount')) / expense_group.members.count()


        for member in expense_group.members.all() :

            if member == request.user :
                continue

            if expense.shared_equally == True :
                ExpenseSplit.objects.create(
                    expense = expense,
                    user = member,
                    share_amount = equal_share_amount,
                    is_paid = False,
                    owed_to=request.user
                )
            else :
                if member.id not in data.get('exact_amount') :
                    return Response({'message' : 'Exact amount for all members is required'}, status=status.HTTP_400_BAD_REQUEST)

                ExpenseSplit.object.create(
                    expense = expense,
                    user = member,
                    share_amount = data.get('exact_amount')[member.id],
                    is_paid = False,
                    owed_to= request.user
                )


        return Response({'message' : 'Expense added successfully'}, status=status.HTTP_201_CREATED)


@api_view(['post'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def settle_expense(request) :
    split = get_object_or_404(ExpenseSplit , id = request.data.get('split_id'))

    if split.user != request.user :
        return Response({'message' : 'You are not authorized to settle this expense'}, status=status.HTTP_400_BAD_REQUEST)
    if split.is_paid == True :
        return Response({'message' : 'This expense has already been settled'}, status=status.HTTP_400_BAD_REQUEST)

    amount = float(request.data.get('amount'))

    amount_left = float(split.share_amount) - amount
    if amount_left <= 0 :
        split.is_paid = True
        split.save()
        Settlement.objects.create(
            from_user = request.user,
            to_user = split.owed_to,
            amount = amount,
            split = split
        )
        return Response({'message' : 'Expense settled successfully'}, status=status.HTTP_200_OK)

    split.share_amount = amount_left
    split.save()
    return Response({'message' : f'Partial payment successfully amount left to pay {amount_left}'}, status=status.HTTP_200_OK)
