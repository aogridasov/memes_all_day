from django.contrib import admin

from .models import MemeLike, MemePost


@admin.register(MemePost)
class MemePostAdmin(admin.ModelAdmin):
    pass


@admin.register(MemeLike)
class MemeLikeAdmin(admin.ModelAdmin):
    pass
