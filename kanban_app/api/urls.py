from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import BoardViewSet, TaskViewSet, CommentViewSet


router = DefaultRouter()
router.register(r"boards", BoardViewSet, basename="board")
router.register(r"tasks", TaskViewSet, basename="task")


urlpatterns = [
    path(
        "tasks/<int:task_id>/comments/",
        CommentViewSet.as_view({"get": "list", "post": "create"}),
        name="task-comments",
    ),
    path(
        "tasks/<int:task_id>/comments/<int:pk>/",
        CommentViewSet.as_view({"delete": "destroy"}),
        name="task-comment-detail",
    ),
] + router.urls