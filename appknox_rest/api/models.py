from django.db import models

#  class QCAs(models.Model):
#     qca_types = (
#         ("q", "question"),
#         ("a", "answer"),
#         ("c", "comment"),
#     )
#     qca_type = models.CharField(max_length=10, choices=qca_types)
#     body = models.TextField()
#     user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
#     question_id = models.ForeignKey(
#         "self",
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#         related_name="answers",
#     )
#     answer_id = models.ForeignKey(
#         "self",
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#         related_name="comments",
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     upvotes = models.IntegerField()
#     downvotes = models.IntegerField()


class User(models.Model):
    name = models.CharField(max_length=255)
    # other fields for user profile like email, password, etc.


class Question(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Answer(models.Model):
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="comment_of_question",
    )
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        related_name="comment_of_answer",
    )
    parent_comment = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="comment_of_comment",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(
        Answer, on_delete=models.CASCADE, related_name="votes", null=True, blank=True
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="votes", null=True, blank=True
    )
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="votes", null=True, blank=True
    )
    value = models.SmallIntegerField()
