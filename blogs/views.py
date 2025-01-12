from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView

from blogs.models import Category, Comment, Blog
from blogs.serializers import CategorySerializer, BlogSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from notification.utils import send_email_notification
from notification.email_templates import comment_delete_by_author_notification
from rest_framework.exceptions import PermissionDenied

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
    
    def retrieve(self, request, *args, **kwargs):
        blog = self.get_object()
        paginator = PageNumberPagination()
        paginator.page_size = 3
        comments = blog.comments.all()
        
        paginated_comments = paginator.paginate_queryset(comments,request)
        comment_serializer = CommentSerializer(paginated_comments, many=True)
        
        blog_serializer = self.get_serializer(blog)
        response_data = blog_serializer.data 
        response_data['paginated_comments'] = paginator.get_paginated_response(comment_serializer.data).data
        return Response(response_data)
    
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
    
class CommentCreateView(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        blog_id = self.kwargs.get('blog_id')    
        blog = get_object_or_404(Blog, id=blog_id, status=Blog.StatusChoices.PUBLISHED)
        return Comment.objects.filter(blog=blog)
    
    def perform_create(self, serializer):
        blog_id = self.kwargs.get('blog_id')
        blog = get_object_or_404(Blog, id=blog_id, status=Blog.StatusChoices.PUBLISHED)
        serializer.save(blog=blog, author=self.request.user)
        
class CommentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    
    def perform_update(self, serializer):
        comment = self.get_object()    
        if comment.author != self.request.user:
            raise PermissionDenied({"detail": "You are not authorized for this action."})
        serializer.save()
        
    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()    
        if request.user != comment.author and request.user != comment.blog.author:
            return Response({"detail": "You are not authorized for this action."}, status=status.HTTP_401_UNAUTHORIZED)
        if request.user == comment.blog.author:
            subject, message = comment_delete_by_author_notification(comment.author, comment.blog, comment)
            send_email_notification(comment.author, subject, message)
        self.perform_destroy(comment)
        return Response({"detail": "Comment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)