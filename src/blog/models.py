from django.db import models
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            while Category.objects.filter(slug=self.slug).exists():
                self.slug = f"{slugify(self.title)}-{get_random_string(4)}"
        super().save(*args, **kwargs)
  
          
    class Meta:
            verbose_name_plural = 'Categories'
    def __str__(self):
        return self.title
        


class BlogPost(models.Model):
    STATUS = [
        ('draft', 'Draft'),
        ('published', 'Published')
    ]
    title = models.CharField(max_length=250, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    featured_image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    content = RichTextUploadingField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS, default='draft')
    meta_title = models.CharField(max_length=250, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            while BlogPost.objects.filter(slug=self.slug).exists():
                self.slug = f"{slugify(self.title)}-{get_random_string(4)}"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title

class Comment(models.Model):
    BlogPost = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)