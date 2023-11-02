from django.contrib import admin
from .models import Posts, Category, Response, RegUsers
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import gettext_lazy as _


admin.site.register(Posts)
admin.site.register(Category)
admin.site.register(RegUsers)
admin.site.register(Response)

class FlatPageAdmin(FlatPageAdmin):
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': (
                'enable_comments',
                'registration_required',
                'template_name',
            ),
        }),
    )


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
