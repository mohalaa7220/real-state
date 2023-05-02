from django.contrib import admin
from .models import Comments, Testimonials


# Register your models here.


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('text', "rating", 'product',
                    'user', 'created_at', 'updated_at')
    ordering = ('-rating',)


@admin.register(Testimonials)
class TestimonialsAdmin(admin.ModelAdmin):
    list_display = ('text',  'user', 'created_at', 'updated_at',)
