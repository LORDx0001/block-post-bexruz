from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, PostSerializer, CommentSerializer, PostDetailSerializer, RegisterSerializer, LoginSerializer
from .models import User, Post, Comment
from rest_framework.generics import RetrieveAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



class RegisterAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        response_data = {'user': UserSerializer(user).data}
        return Response(response_data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            },
        ),
        responses={200: 'Login successful', 400: 'Bad request', 401: 'Invalid credentials'}
    )
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        access = AccessToken.for_user(user)
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Login successful",
            "user": UserSerializer(user).data,
            "access": str(access),
            "refresh": str(refresh)
        }, status=status.HTTP_200_OK)
    
class CreatePostAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save(author=request.user)
        return Response(self.get_serializer(post).data, status=status.HTTP_201_CREATED)
    


class ListPostAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *_ , **__):
        posts = self.get_queryset()
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

class MyPostsAPIView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def get(self, request, *args, **kwargs):
        posts = self.get_queryset()
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

class RetrievePostAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'id'


class UpdatePostAPIView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return Response({"error": "You do not have permission to update this post."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)


class DestroyPostAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return Response({"error": "You do not have permission to delete this post."}, status=status.HTTP_403_FORBIDDEN)
        super().destroy(request, *args, **kwargs)
        return Response({"message": "Post deleted successfully."}, status=status.HTTP_200_OK)

class CommentAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        comment = self.get_object()
        serializer = self.get_serializer(comment)
        return Response(serializer.data)
    
    def put(self, request, *args, **kwargs):
        comment = self.get_object()
        serializer = self.get_serializer(comment, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.delete()
        return Response(status=204)  # No Content
    
class UserAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response(status=204) 