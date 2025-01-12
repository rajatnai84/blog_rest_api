from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)

class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return str(self.name)

class Blog(models.Model):
    class StatusChoices(models.TextChoices):
        DRAFT="Draft"
        PUBLISHED="Published"

    title = models.TextField()
    content = models.TextField(null=True)
    banner = models.ImageField(upload_to='banners/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.DRAFT
    )

    def save(self, *args, **kwargs):
        if self.status == self.StatusChoices.PUBLISHED and self.published_at is None:
            self.published_at = now()
        elif self.status == self.StatusChoices.DRAFT:
            self.published_at = None
        super().save(*args,**kwargs)
        
class Comment(models.Model):
    content = models.TextField()
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.author) + " " + str(self.blog.title)

