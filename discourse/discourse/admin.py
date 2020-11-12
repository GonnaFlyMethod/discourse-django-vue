from django.contrib import admin
from .models import Topic, Comment, TagOfTopic, TopicSection


admin.site.register(Topic)
admin.site.register(Comment)
admin.site.register(TagOfTopic)
admin.site.register(TopicSection)