from django.contrib import admin
from blog.models import Post,Comment

admin.site.site_header='Shaxa Admin'
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    search_fields=['title','content']
    list_display=['title','published_date']
    list_filter=['published_date']
    

admin.site.register(Post,PostAdmin)
admin.site.register(Comment)