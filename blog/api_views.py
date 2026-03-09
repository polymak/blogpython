from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Blog, CustomUser
from .serializers import BlogSerializer, UserSerializer, LoginSerializer


class BlogListCreateView(generics.ListCreateAPIView):
    """API endpoint for listing and creating blogs"""
    queryset = Blog.objects.all().order_by('-created_at')
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Only admin users can create blogs via API
        if not self.request.user.is_staff and self.request.user.role != 'admin':
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()


class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    """API endpoint for retrieving, updating and deleting blogs"""
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        # Only admin users can update blogs via API
        if not self.request.user.is_staff and self.request.user.role != 'admin':
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()

    def perform_destroy(self, instance):
        # Only admin users can delete blogs via API
        if not self.request.user.is_staff and self.request.user.role != 'admin':
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        instance.delete()


class UserListCreateView(generics.ListCreateAPIView):
    """API endpoint for listing and creating users"""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only admin users can see all users
        if not self.request.user.is_staff and self.request.user.role != 'admin':
            return CustomUser.objects.none()
        return CustomUser.objects.all()

    def perform_create(self, serializer):
        # Only admin users can create users via API
        if not self.request.user.is_staff and self.request.user.role != 'admin':
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.role = 'admin'
        user.is_staff = True
        user.is_active = True
        user.save()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """API endpoint for retrieving, updating and deleting users"""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only admin users can see all users
        if not self.request.user.is_staff and self.request.user.role != 'admin':
            return CustomUser.objects.none()
        return CustomUser.objects.all()

    def perform_update(self, serializer):
        # Only admin users can update users via API
        if not self.request.user.is_staff and self.request.user.role != 'admin':
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()

    def perform_destroy(self, instance):
        # Only admin users can delete users via API
        if not self.request.user.is_staff and self.request.user.role != 'admin':
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        instance.delete()


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """API endpoint for user login"""
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None and (user.is_staff or user.role == 'admin'):
            # Create or get token
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'token': token.key,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role
                }
            })
        else:
            return Response({'error': 'Invalid credentials or insufficient permissions'}, 
                          status=status.HTTP_401_UNAUTHORIZED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """API endpoint for user logout"""
    try:
        request.user.auth_token.delete()
        return Response({'message': 'Successfully logged out'})
    except:
        return Response({'error': 'Logout failed'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def check_auth(request):
    """API endpoint to check if user is authenticated"""
    return Response({
        'authenticated': True,
        'user': {
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
            'role': request.user.role
        }
    })

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def home_api(request):
    """API endpoint for home page content"""
    return Response({
        'title': 'Welcome to BlogPython',
        'description': 'Discover our latest articles and news',
        'contact_info': {
            'email': 'polycarpemakombo@gmail.com',
            'phone': '+243822012578'
        }
    })

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def contact_api(request):
    """API endpoint for contact information"""
    return Response({
        'title': 'Contact Us',
        'email': 'polycarpemakombo@gmail.com',
        'phone': '+243822012578',
        'message': 'Feel free to reach out to us for any questions or inquiries.'
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_api(request):
    """API endpoint for dashboard summary"""
    if not (request.user.is_staff or request.user.role == 'admin'):
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    blog_count = Blog.objects.count()
    user_count = CustomUser.objects.count()

    return Response({
        'dashboard_summary': {
            'total_blogs': blog_count,
            'total_users': user_count,
            'user_info': {
                'username': request.user.username,
                'email': request.user.email,
                'role': request.user.role
            }
        }
    })
