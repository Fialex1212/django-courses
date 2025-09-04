from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, RegisterSerializer
from .models import User


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = []


class MeView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
