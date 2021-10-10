from django.contrib import admin

from .models import *

admin.site.register(Category)
# admin.site.register(LostItem)


class ItemImageInLine(admin.TabularInline):
    model = Image
    extra = 1


@admin.register(Item)
class AdminItemDisplay(admin.ModelAdmin):
    fields = ('user', 'title', 'description', 'date_lost', 'category', 'phone')
    search_fields = ('title', )
    inlines = (ItemImageInLine, )