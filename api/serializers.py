from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Expense



class RegisterUserSerializer(serializers.ModelSerializer) :
    email  = serializers.EmailField(
        required = True ,
        validators = [UniqueValidator(queryset = User.objects.all())]
    )
    password = serializers.CharField(
        required = True,
        write_only = True,
        validators = [validate_password]
    )
    password2 = serializers.CharField(write_only = True , required = True)


    def validate(self,attrs):
        if attrs['password'] != attrs['password2'] :
            raise serializers.ValidationError({'password' : 'Password fields did not match'})
        return attrs

    def create(self,validated_data) :
       user = User.objects.create(
           username = validated_data['username'],
           email = validated_data['email'],
           first_name = validated_data['first_name'],
           last_name = validated_data['last_name']
       )
       user.set_password(validated_data['password'])
       user.save()
       return user

    class Meta :
        model = User
        fields = ('email' , 'password' , 'password2' , 'username' , 'first_name' , 'last_name')

class ExpenseSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Expense
        fields = '__all__'
