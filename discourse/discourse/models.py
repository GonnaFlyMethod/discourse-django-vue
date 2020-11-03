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
	author = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True,
		                       null=True)
	to_topic = models.ForeignKey(Topic, related_name='topic_comments',
		                         on_delete=models.CASCADE, blank=True,
		                         null=True)
	text = models.TextField(blank=False, null=False)
	timestamp = models.DateTimeField(auto_now_add=True)
	likes = models.IntegerField(blank=False, null=False, default=0)
	dislikes = models.IntegerField(blank=False, null=False, default=0)
