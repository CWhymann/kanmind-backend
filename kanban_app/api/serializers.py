from rest_framework import serializers
from kanban_app.models import Board, Task, Comment


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["id", "title", "owner"]
        read_only_fields = ["owner"]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "description", "status", "board", "assigned_to"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "content", "task", "author"]
        read_only_fields = ["author"]