from rest_framework import serializers
from .models import Employee, Dispatches


class Employeeserializer(serializers.ModelSerializer):
    class Meta:
        model = Employee

        fields = '__all__'


class DispatchesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Dispatches

        fields = '__all__'
