import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    first_name = None
    last_name = None
    email = models.EmailField(unique=True, verbose_name=("Email address"))
    telegram = models.CharField(
        unique=True, null=True, blank=True, verbose_name=("Telegram nick")
    )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, null=True, blank=True)

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions_set",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "telegram"]

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class UserCourseAccess(models.Model):
    wuser = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="course_accesses"
    )
    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE)
    activated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Course Access"
        verbose_name_plural = "Courses Accesses"


class UserLessonAccess(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    lesson = models.ForeignKey("courses.Lesson", on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Lesson Access"
        verbose_name_plural = "Lesson Accesses"
