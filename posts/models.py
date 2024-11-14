from django.db import models
from django.db.models.signals import post_save,post_delete
from django.urls import reverse
from django.utils.text import slugify
import uuid
from django.contrib.auth.models import User
# Create your models here.


# uploading user files to specific directory
def user_directory_path(instance,filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Tag(models.Model):
    title = models.CharField(max_length=100, verbose_name='Tag')
    slug=models.SlugField(null=False, unique=True, default=uuid.uuid1)
    
    class Meta:
        verbose_name='Tag'
        verbose_name_plural='Tags'
    # def get_absolute_url(self):
    #     return reverse('tags', args=[self.slug])
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            print(f"Saving Tag with title: {self.title}, slug: {self.slug}")

        return super().save(*args,**kwargs)
        
        
class Post(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    pictures = models.ImageField(upload_to=user_directory_path, verbose_name='Picture', null=True)
    captions=models.CharField(max_length=1000000, verbose_name='Caption')
    postedTime= models.DateTimeField(auto_now_add=True)
    tag = models.ManyToManyField(Tag,related_name='tags')
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    like=models.IntegerField(default=0)
    
    
    def get_absolute_url(self):
        return reverse("post-details", args=[str(self.id)])
    
    def __str__(self):
        return self.captions
    
    
    
class Follow(models.Model):
    follower=models.ForeignKey(User, on_delete=models.CASCADE,related_name='follower')
    following=models.ForeignKey(User, on_delete=models.CASCADE,related_name='following')
    
class Stream(models.Model):
    stream_following=models.ForeignKey(User, on_delete=models.CASCADE,related_name='stream_following')
    stream_user=models.ForeignKey(User, on_delete=models.CASCADE,related_name='stream_user')
    post=models.ForeignKey(Post, on_delete=models.CASCADE,null=True)
    date=models.DateTimeField()
    
    def add_post(sender,instance,*args, **kwargs):
        post = instance
        user=post.user
        followers = Follow.objects.all().filter(following=user)
        for follower in followers:
            stream=Stream(post=post, stream_user=follower.follower, date=post.postedTime, stream_following=user)
            stream.save()

class Likes(models.Model):

    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_likes")
    Post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="Post_likes")

            
post_save.connect(Stream.add_post, sender=Post)
    


            
        
        


    
    
    
    
    