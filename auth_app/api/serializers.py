from rest_framework import serializers
from auth_app.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["fullname", "email", "password", "repeated_password"]

    def validate(self, attrs):
        if attrs["password"] != attrs["repeated_password"]:
            raise serializers.ValidationError({"password": "Passwörter stimmen nicht überein."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("repeated_password")
        return User.objects.create_user(**validated_data)