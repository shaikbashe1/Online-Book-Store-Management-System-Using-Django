from django.contrib import admin
from .models import Category, Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'price', 'stock')
    list_filter = ('category',)
    search_fields = ('title', 'author')

admin.site.register(Category)
admin.site.register(Book, BookAdmin)
