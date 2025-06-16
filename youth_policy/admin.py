from django.contrib import admin
from .models import YouthPolicy, Region, Sido

admin.site.register(Region)
admin.site.register(Sido)

@admin.register(YouthPolicy)
class YouthPolicyAdmin(admin.ModelAdmin):
    list_display = ['정책명', '대상연령', '정책키워드', 'is_weekly_pick']
    list_filter = ['is_weekly_pick']
    search_fields = ['정책명', '정책키워드']