from django.contrib import admin
from posts.models import Likes, Tag,Post,Follow,Stream

# Register your models here.

admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Stream)
admin.site.register(Likes)
