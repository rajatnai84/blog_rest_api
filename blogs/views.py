from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView

from blogs.models import Category, Tag, Blog
from blogs.serializers import CategorySerializer, TagSerializer, BlogSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

class CategoryListCreateView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]

class CategoryRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    
class BlogListCreateView(ListCreateAPIView):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['author', 'category', 'tags__name']
    search_fields = ['title', 'content', 'tags__name', 'category__name']
    
    def get_queryset(self):
        status_filter = Blog.StatusChoices.PUBLISHED
        return Blog.objects.filter(status=status_filter)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
class BlogRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Blog.objects.all()
    
    def get_object(self):
        obj = super().get_object()
        if obj.author != self.request.user:
            raise ValidationError({'detail': 'You are not authorized for this action.'})
        return obj
    
class BlogChangeStatusView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk, status_name):
        try:
            blog = Blog.objects.get(id=pk)
        except:
            return Response({"detail": "Blog not founds"}, status=status.HTTP_404_NOT_FOUND)
        
        if blog.author != request.user:
            return Response({"detail": "You are not authorized for this action."}, status=status.HTTP_401_UNAUTHORIZED)
        
        if status_name not in [choice[0] for choice in Blog.StatusChoices.choices]:
            return Response({"detail": "Invalid status name."}, status=status.HTTP_400_BAD_REQUEST)
        
        
        blog.status = status_name
        if status_name == Blog.StatusChoices.PUBLISHED and not blog.published_at:
            blog.published_at = now()
        elif status == Blog.StatusChoices.DRAFT:
            blog.published_at = None
            
        blog.save()
        return Response(BlogSerializer(blog).data, status=status.HTTP_200_OK)

class BlogUserBlogsView(ListAPIView):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Blog.objects.filter(author=self.request.user)