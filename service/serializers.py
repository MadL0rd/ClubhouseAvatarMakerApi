from rest_framework import serializers
from service.models import Border, Code, SettingJson


class BorderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Border
        fields = '__all__'


class NewBorderSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField()

    class Meta:
        model = Border
        fields = ['id', 'brand', 'title', 'image', 'colorable', 'code']


class CodeSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField()

    class Meta:
        model = Code
        fields = ['id', 'brand', 'name', 'description']


class SettingJsonSerializer(serializers.ModelSerializer):

    class Meta:
        model = SettingJson
        fields = '__all__'
