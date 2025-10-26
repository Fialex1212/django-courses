from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from .models import ActivationCode
from users.models import UserCourseAccess
from .serializers import ActivateCodeSerializer


class ActivateCodeView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ActivateCodeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code_str = serializer.validated_data["code"]

        try:
            code = ActivationCode.objects.select_related("course").get(code=code_str)
        except ActivationCode.DoesNotExist:
            return Response({"error": "Неверный код"}, status=status.HTTP_404_NOT_FOUND)

        if code.is_used():
            return Response(
                {"error": "Код уже использован"}, status=status.HTTP_400_BAD_REQUEST
            )

        code.activated_by = request.user
        code.used_at = timezone.now()
        code.save()

        UserCourseAccess.objects.get_or_create(user=request.user, course=code.course)

        return Response(
            {
                "message": f"Курс '{code.course.title}' успешно активирован!",
                "course_id": code.course.id,
                "course_title": code.course.title,
            },
            status=status.HTTP_200_OK,
        )
