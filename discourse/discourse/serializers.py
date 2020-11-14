from rest_framework import serializers

from .models import Topic, Comment, TagOfTopic, TopicSection


class CommentToTopicSerializer(serializers.ModelSerializer):
	author = serializers.SlugRelatedField(slug_field="email", read_only=True)
	class Meta:
		model = Comment
		fields = '__all__'


class TopicsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="email", read_only=True)
    tags = serializers.SlugRelatedField(many=True, slug_field="name_of_tag",
    	                                read_only=True)
    class Meta:
        model = Topic
        fields = '__all__'

    def get_comments(self, obj):
    	return CommentToTopicSerializer(obj.topic_comments.all(),
    		                            many=True).data


class PostCommentSerializer(serializers.ModelSerializer):

	class Meta:
		model = Comment
		fields = '__all__'


class AttachTagsToTopicSerializer(serializers.ModelSerializer):

	class Meta:
		model = TagOfTopic
		fields = '__all__'


class SectionsSerializer(serializers.ModelSerializer):

	class Meta:
		model = TopicSection
		fields = '__all__'