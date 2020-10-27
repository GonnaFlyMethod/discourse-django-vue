from django.db import models

from accounts.models import Account


class Topic(models.Model):
	topic = models.CharField(max_length=100)
	authors = models.ManyToManyField(Account)
	short_description = models.TextField(max_length=400)
	timestamp = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-timestamp',]


class Comment(models.Model):
	author = models.ForeignKey(Account, related_name='commnet_author',
		                       on_delete=models.CASCADE)
	text = models.TextField(blank=False, null=False)
	timestamp = models.DateTimeField(auto_now_add=True)

