from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()
""" [Register View]
    Creating new user
"""
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is None:
            instance.set_password(password)
        instance.save()
        return instance