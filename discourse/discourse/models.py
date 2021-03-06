from django.db import models

from ckeditor.fields import RichTextField

from accounts.models import Account

from .models_fields_validators import image_size_limit


class TagOfTopic(models.Model):
	name_of_tag = models.CharField(max_length=200)

	def __str__(self):
		return f'Tag:{self.name_of_tag}'


class Topic(models.Model):
	topic = models.CharField(max_length=100)
	author = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True,
		                       null=True, related_name='user_topics')
	views = models.IntegerField(blank=False, null=False, default=0)
	main_sphere_of_topic = models.CharField(max_length=100)
	tags = models.ManyToManyField(TagOfTopic, blank=False)
	self_url = models.CharField(max_length=1000, null=True)
	day_of_publication = models.IntegerField(null=True)
	month_of_publication = models.CharField(max_length=20, null=True)
	who_viewed = models.ManyToManyField(Account, related_name='who_viewed_t',
		                               blank=True)
	approved = models.BooleanField(default=False)
	image_of_topic = models.ImageField('Topic image', null=True, blank=True,
										upload_to='discourse/topic_images',
										validators=[image_size_limit])
	image_url = models.CharField(max_length=1000, blank=True, null=True)
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
	text = RichTextField(blank=True, null=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	likes = models.IntegerField(blank=False, null=False, default=0)
	who_liked = models.ManyToManyField(Account, related_name='who_liked_c',
		                               blank=True)

	def __str__(self):
		return self.text[:30]


class TopicSection(models.Model):
	# possible Sections:

	# Adventuares
	# Travel
	# Home
	# People
	# Free time
	# Art
	# Sport
	# Health
	# Science
	# Edication
	# Video games
	name_of_section = models.CharField(max_length=100)
	topics_included = models.ManyToManyField(Topic, blank=True)
	image_of_section = models.ImageField('Section image', null=True, blank=True,
										 upload_to='discourse/section_images')

	def __str__(self):
		return f'Section: {self.name_of_section}'

	def get_total_num_of_topics(self) -> int:
		return len(self.topics_included.all().filter(approved=True))
