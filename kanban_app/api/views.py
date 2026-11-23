from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from kanban_app.models import Board, Task, Comment
from .serializers import BoardSerializer, TaskSerializer, CommentSerializer


class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Board.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(board__owner=self.request.user)

    @action(detail=False, methods=["get"], url_path="assigned-to-me")
    def assigned_to_me(self, request):
        tasks = self.get_queryset().filter(assigned_to=request.user)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="reviewing")
    def reviewing(self, request):
        tasks = self.get_queryset().filter(status="reviewing")
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        task_id = self.kwargs.get("task_id")
        return Comment.objects.filter(task_id=task_id, task__board__owner=self.request.user)

    def perform_create(self, serializer):
        task_id = self.kwargs.get("task_id")
        task = Task.objects.get(id=task_id)
        serializer.save(author=self.request.user, task=task)