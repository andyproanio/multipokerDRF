from .models import Machine, Retail, Shop, User
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import connection
from .serializers import MachineSerializer, RetailSerializer, ShopSerializer, UserSerializer, VerifyPasswordSerializer


class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = MachineSerializer

    def create(self, request, *args, **kwargs):
        machineId = request.data.get('id')

        if machineId:
            with connection.cursor() as cursor:
                cursor.execute(f"ALTER SEQUENCE game_machine_id_seq RESTART WITH {int(machineId)}")

        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()

        shopId = self.request.query_params.get('shopId')

        if shopId:
            queryset = queryset.filter(shopId=shopId).order_by('id')

        return queryset


class RetailViewSet(viewsets.ModelViewSet):
    queryset = Retail.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        userId = self.request.query_params.get('userId')

        if userId:
            queryset = queryset.filter(userId=userId)

        return queryset.order_by('id')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        userId = self.request.query_params.get('userId')

        if userId:
            json = queryset.filter(userId=userId).first()

            serializer = self.get_serializer(json)

            return Response(serializer.data)

        return super().list(request, *args, **kwargs)


class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ShopSerializer

    def create(self, request, *args, **kwargs):
        shopId = request.data.get('id')

        if shopId:
            with connection.cursor() as cursor:
                cursor.execute(f"ALTER SEQUENCE game_shop_id_seq RESTART WITH {int(shopId)}")

        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()

        userId = self.request.query_params.get('userId')
        retailId = self.request.query_params.get('retailId')

        if userId:
            queryset = queryset.filter(userId=userId)

        if retailId:
            queryset = queryset.filter(retailId=retailId).order_by('id')

        return queryset.order_by('id')
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        userId = self.request.query_params.get('userId')

        if userId:
            json = queryset.filter(userId=userId).first()
            
            serializer = self.get_serializer(json)
            
            return Response(serializer.data)
        
        return super().list(request, *args, **kwargs)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        userId = request.data.get('id')

        if userId:
            with connection.cursor() as cursor:
                cursor.execute(f"ALTER SEQUENCE game_user_id_seq RESTART WITH {int(userId)}")

        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['post'], url_path='verifyPassword')
    def verify_password(self, request):
        serializer = VerifyPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user_detectado']

        return Response({
            "valido": True,
            "id": user.id,
            "type": user.type
        }, status=status.HTTP_200_OK)