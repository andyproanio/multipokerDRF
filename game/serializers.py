from rest_framework import serializers
from .models import Machine, Retail, Shop, User


class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = '__all__'


class RetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retail
        fields = '__all__'


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class VerifyPasswordSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = data.get('username')
        password = data.get('password')

        try:
            username = User.objects.get(username=user)
        except User.DoesNotExist:
            raise serializers.ValidationError("Credenciales Incorrectas")

        if not username.verify_password(password):
            raise serializers.ValidationError("Credenciales Incorrectas")

        data['user_detectado'] = username
        return data
