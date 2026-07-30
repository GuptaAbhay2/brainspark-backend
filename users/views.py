from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username', '').strip()
    password = request.data.get('password', '').strip()
    if not username or not password:
        return Response({'error': 'Username and password required'},
                       status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already taken'},
                       status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.create(
        username=username,
        email=f'{username}@brainspark.app',
        password_hash=hash_password(password)
    )
    return Response({**UserSerializer(user).data, 'is_new': True},
                   status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username', '').strip()
    password = request.data.get('password', '').strip()
    if not username or not password:
        return Response({'error': 'Username and password required'},
                       status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(username=username)
        if user.password_hash != hash_password(password):
            return Response({'error': 'Wrong password'},
                           status=status.HTTP_401_UNAUTHORIZED)
        return Response({**UserSerializer(user).data, 'is_new': False})
    except User.DoesNotExist:
        return Response({'error': 'User not found'},
                       status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_profile(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        return Response(UserSerializer(user).data)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_by_email(request):
    """Keep for backwards compat — strictly read only"""
    email    = request.query_params.get('email', '')
    username = request.query_params.get('username', '')
    
    if username and User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        return Response({**UserSerializer(user).data, 'is_new': False})
        
    if email and User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        return Response({**UserSerializer(user).data, 'is_new': False})
        
    return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)