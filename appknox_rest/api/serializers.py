from rest_framework import serializers
from .models import User, Comment, Answer, Vote, Question


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    answer = serializers.PrimaryKeyRelatedField(queryset=Answer.objects.all())
    parent_comment = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Comment
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())

    class Meta:
        model = Answer
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
    #
    #     # Check if the serializer is being used for a single object
        view = self.context.get("view")
        if view and view.action == "retrieve":
            # Get all comments for the question
            comments = Comment.objects.filter(answer=instance)
            comments_serializer = CommentSerializer(comments, many=True)
            representation["comments"] = comments_serializer.data
            # Get all votes for the question
            votes = Vote.objects.filter(answer=instance)
            votes_serializer = VoteSerializer(votes, many=True)
            representation["votes"] = votes_serializer.data

        return representation


class QuestionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Question
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Check if the serializer is being used for a single object
        if self.context.get("view").action == "retrieve":
            # Get all answers for the question
            answers =  Answer.objects.filter(question=instance)
            answers_serializer = AnswerSerializer(answers, many=True)
            representation["answers"] = answers_serializer.data

            # Get all comments for the question
            comments = Comment.objects.filter(question=instance)
            comments_serializer = CommentSerializer(comments, many=True)
            representation["comments"] = comments_serializer.data

            # Get all votes for the question
            votes = Vote.objects.filter(question=instance)
            votes_serializer = VoteSerializer(votes, many=True)
            representation["votes"] = votes_serializer.data

        return representation


class VoteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Vote
        fields = "__all__"

    def create(self, validated_data):
        user = validated_data.get("user")
        answer = validated_data.get("answer")
        question = validated_data.get("question")
        comment = validated_data.get("comment")
        # handle if user votes multiple t
        if (
            Vote.objects.filter(
                user=user, answer=answer, question=question, comment=comment
            ).exists()
            or (answer and Vote.objects.filter(user=user, answer=answer).exists())
            or (question and Vote.objects.filter(user=user, question=question).exists())
            or (comment and Vote.objects.filter(user=user, comment=comment).exists())
        ):
            raise serializers.ValidationError(
                "User has already voted for this question, answer or comment."
            )

        return super().create(validated_data)
