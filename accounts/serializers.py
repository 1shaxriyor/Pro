from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    role = serializers.ChoiceField(choices=[('customer', 'Buyurtma beruvchi'),
                                           ('worker', 'Buyurtma oluvchi')])

    job = serializers.ChoiceField(choices=[
        ('svarshik', 'Svarshik'),
        ('suvokchi', 'Suvokchi'),
        ('elektrik', 'Elektrik'),
        ('usta', 'Usta'),
    ], required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone',
                  'password', 'password2', 'role', 'job')

    def validate(self, attrs):
        # Parollar mos emas
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Parollar mos emas!"})

        # Agar user worker bo‘lsa job majburiy bo‘ladi
        if attrs.get('role') == 'worker' and not attrs.get('job'):
            raise serializers.ValidationError({"job": "Usta uchun kasb tanlash shart!"})

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2', None)
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone',
                  'telegram_id', 'role', 'job')
        read_only_fields = ('username', 'email')
