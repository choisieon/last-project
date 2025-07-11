from django.contrib import admin
from .models import YouthPolicy, Region, Sido, PolicyComment

admin.site.register(Region)
admin.site.register(Sido)
admin.site.register(PolicyComment)

@admin.register(YouthPolicy)
class YouthPolicyAdmin(admin.ModelAdmin):
    list_display = ['정책명', '대상연령', '정책키워드', 'like_count']
    search_fields = ['정책명', '정책키워드']

    def like_count(self, obj):
        return obj.likes.count()
    like_count.short_description = '좋아요 수'
