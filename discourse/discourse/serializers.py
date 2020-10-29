from rest_framework import serializers

from .models import Topic, Comment


class CommentToTopicSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		exclude = ['timestamp',]


class TopicsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Topic
        fields = '__all__'

    def get_comments(self, obj):
    	return CommentToTopicSerializer(obj.topic_comments.all(),
    		                            many=True).data