from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken

from oscar.apps.catalogue.models import Product, Category
from oscar.apps.order.models import Order

from .serializers import (
    ProductSerializer, CategorySerializer, OrderSerializer,
    UserSerializer, SuplierProfileSerializer, ClientProfileSerializer
)
from .models import SuplierProfile, ClientProfile

User = get_user_model()

# ------------------------
# PRODUTOS
# ------------------------

class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            # Só fornecedor autenticado pode criar produto
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        # Aqui você pode associar o produto ao supplier, se quiser
        # Exemplo: serializer.save(supplier=self.request.user.suplier_profile)
        serializer.save()


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    
class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Associa o produto ao fornecedor autenticado
        serializer.save(supplier=self.request.user.suplier_profile)

class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        # Atualiza o produto, mantendo a associação com o fornecedor
        serializer.save(supplier=self.request.user.suplier_profile)

class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        # Deleta o produto, mantendo a associação com o fornecedor
        instance.delete()   
    

# ------------------------
# ENCOMENDAS
# ------------------------

class OrderListView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Retorna só as encomendas do cliente autenticado
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Criação da encomenda baseada no carrinho do usuário
        serializer.save(user=self.request.user)


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Garante que só o dono da encomenda veja os detalhes
        return Order.objects.filter(user=self.request.user)
class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Criação da encomenda baseada no carrinho do usuário
        serializer.save(user=self.request.user)


# ------------------------
# AUTENTICAÇÃO E REGISTRO
# ------------------------

class RegisterClientView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        try:
            user = User.objects.create_user(
                username=data['username'],
                email=data.get('email', ''),
                password=data['password'],
                first_name=data.get('first_name', ''),
                last_name=data.get('last_name', '')
            )
            ClientProfile.objects.create(
                user=user,
                contact_phone=data.get('contact_phone', ''),
                delivery_address=data.get('delivery_address', ''),
                city_code=data.get('city_code', ''),
                nif=data.get('nif', '')
            )
            return Response({'message': 'Cliente criado com sucesso.'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ClientProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = request.user
        try:
            client_profile = user.client_profile
            data = ClientProfileSerializer(client_profile).data
            return Response(data, status=status.HTTP_200_OK)
        except ClientProfile.DoesNotExist:
            return Response({'error': 'Perfil de cliente não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        


class RegisterSuplierView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        try:
            user = User.objects.create_user(
                username=data['username'],
                email=data.get('email', ''),
                password=data['password'],
                first_name=data.get('first_name', ''),
                last_name=data.get('last_name', '')
            )
            SuplierProfile.objects.create(
                user=user,
                company_name=data.get('company_name', ''),
                contact_phone=data.get('contact_phone', ''),
                company_address=data.get('company_address', ''),
                cnpj=data.get('cnpj', ''),
                ie=data.get('ie', '')
            )
            return Response({'message': 'Fornecedor criado com sucesso.'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SuplierProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            suplier_profile = user.suplier_profile
            data = SuplierProfileSerializer(suplier_profile).data
            return Response(data, status=status.HTTP_200_OK)
        except SuplierProfile.DoesNotExist:
            return Response({'error': 'Perfil de fornecedor não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            # JWT token generation (exemplo com Simple JWT)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            'user': UserSerializer(user).data,
            'client_profile': None,
            'suplier_profile': None
        }
        try:
            data['client_profile'] = ClientProfileSerializer(user.client_profile).data
        except ClientProfile.DoesNotExist:
            pass
        try:
            data['suplier_profile'] = SuplierProfileSerializer(user.suplier_profile).data
        except SuplierProfile.DoesNotExist:
            pass

        return Response(data)

# ------------------------
# CATEGORIAS
# ------------------------

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
