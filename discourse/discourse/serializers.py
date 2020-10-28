from rest_framework import serializers

from .models import Topic, Comment


class TopicsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = '__all__'


class CommentToTopicSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Comment
		exclude = ['timestamp',]