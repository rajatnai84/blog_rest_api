from rest_framework import serializers
from .models import Category, Tag, Blog, Comment
from rest_framework.exceptions import ValidationError
from django.utils.timezone import now

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id','name')

class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = Comment
        fields = (
            'id',
            'content', 
            'blog', 
            'author', 
            'author_name', 
            'created_at', 
            'updated_at'
        )
        read_only_fields=(
            'author', 'created_at', 'updated_at', 'blog'
        )
class BlogSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField(max_length=50),write_only=True, required=False)
    tag_details = TagSerializer(many=True, read_only=True, source='tags')
    
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True
    )
    category_details = CategorySerializer(read_only=True,source='category')
    
    total_comments = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Blog
        fields = '__all__'
        read_only_fields=(
            'author',
            'created_at',
            'published_at',
            'updated_at',
        )
    
    def create(self, validated_data):
        tag_names = validated_data.pop('tags', [])
        category = validated_data.get('category')
        status = validated_data.get('status', Blog.StatusChoices.DRAFT)
        if status == Blog.StatusChoices.PUBLISHED:
            validated_data['published_at'] = now()
            
        blog = Blog.objects.create(**validated_data)
        if category:
            blog.category = category
            blog.save()
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name)
            blog.tags.add(tag)
        return blog
    
    def update(self, instance, validated_data):
        tag_names = validated_data.get('tags')
        category = validated_data.get('category')
        
        if tag_names:
            instance.tags.clear()
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=name)
                instance.tags.add(tag)
        
        if category:
            instance.category = category
        
        for attr, value in validated_data.items():
            if attr not in ['tags', 'category']:  
                setattr(instance, attr, value)

            
        instance.save()
        return instance
    
    def validate_status(self, value):
        if self.instance:
            if value == Blog.StatusChoices.PUBLISHED and not self.instance.published_at:
                raise ValidationError({"detail":"If blog is published it have publishing date-time."})
        return value
    
    def get_total_comments(self, obj):
        return obj.comments.count()
