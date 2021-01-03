from django.db import models


class RecentBlogPostQueryset(models.QuerySet):
    def last_ten(self):
        return self.order_by('-date_created')[:10]


class RecentBlogPostManager(models.Manager):
    def get_queryset(self):
        return RecentBlogPostQueryset(self.model, using=self._db).last_ten()
