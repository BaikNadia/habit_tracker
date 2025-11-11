from django.db import models
from django.core.exceptions import ValidationError
from users.models import User


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="habits")
    place = models.CharField(max_length=100)
    time = models.TimeField()
    action = models.CharField(max_length=200)
    is_pleasant = models.BooleanField(default=False)
    related_habit = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )
    periodicity = models.PositiveSmallIntegerField(default=1)  # days
    reward = models.CharField(max_length=200, blank=True, null=True)
    duration = models.PositiveSmallIntegerField()  # seconds
    is_public = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']  # Сортировка по ID в обратном порядке (новые привычки first)
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'

    def __str__(self):
        return self.action

    def clean(self):
        # 1. Нельзя одновременно указывать вознаграждение и связанную привычку
        if self.reward and self.related_habit:
            raise ValidationError(
                "Нельзя указывать и вознаграждение, и связанную привычку."
            )

        # 2. Время выполнения <= 120 сек
        if self.duration > 120:
            raise ValidationError("Время выполнения не должно превышать 120 секунд.")

        # 3. Связанная привычка должна быть приятной
        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError("Связанная привычка должна быть приятной.")

        # 4. У приятной привычки не может быть вознаграждения или связанной привычки
        if self.is_pleasant:
            if self.reward or self.related_habit:
                raise ValidationError(
                    "У приятной привычки не может быть вознаграждения или связанной привычки."
                )

        # 5. Периодичность от 1 до 7 дней
        if self.periodicity < 1 or self.periodicity > 7:
            raise ValidationError("Привычку нужно выполнять от 1 до 7 раз в неделю.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
