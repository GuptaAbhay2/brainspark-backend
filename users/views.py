from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, RegisterSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register new user — called from Flutter after Firebase auth"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_profile(request, user_id):
    """Get user profile by ID"""
    try:
        user = User.objects.get(id=user_id)
        return Response(UserSerializer(user).data)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_by_email(request):
    """Get or create user by email — for Firebase login"""
    email = request.query_params.get('email')
    username = request.query_params.get('username', email)
    if not email:
        return Response({'error': 'Email required'}, status=status.HTTP_400_BAD_REQUEST)
    user, created = User.objects.get_or_create(
        email=email,
        defaults={'username': username}
    )
    return Response({**UserSerializer(user).data, 'is_new': created})
