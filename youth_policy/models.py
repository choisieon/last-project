from django.db import models

class YouthPolicy(models.Model):
    name = models.CharField("정책명", max_length=255)
    description = models.TextField("정책설명")
    age_range = models.CharField("대상연령", max_length=50)
    keyword = models.CharField("정책키워드", max_length=100, blank=True)
    region = models.CharField("시행지역", max_length=200, blank=True)
    period = models.CharField("신청기간", max_length=200, blank=True)
    URL_ADD = models.URLField("신청URL", max_length=200, blank=True)

    def __str__(self):
        return self.name
