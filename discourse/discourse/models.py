from django.db import models

from accounts.models import Account


class Topic(models.Model):
	topic = models.CharField(max_length=100)
	author = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True,
		                       null=True)
	views = models.IntegerField(blank=False, null=False, default=0)
	who_viewed = models.ManyToManyField(Account, related_name='who_viewed_t',
		                               blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-timestamp',]

	def __str__(self):
		return self.topic


class Comment(models.Model):
	author = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True,
		                       null=True)
	to_topic = models.ForeignKey(Topic, related_name='topic_comments',
		                         on_delete=models.CASCADE, blank=True,
		                         null=True)
	text = models.TextField(max_length=2000, blank=False, null=False)
	timestamp = models.DateTimeField(auto_now_add=True)
	likes = models.IntegerField(blank=False, null=False, default=0)
	who_liked = models.ManyToManyField(Account, related_name='who_liked_c',
		                               blank=True)

	def __str__(self):
		return self.text[:30]
