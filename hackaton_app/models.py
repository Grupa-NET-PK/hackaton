from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile/default.jpg', upload_to='profile/')

    def __str__(self):
        return f'{self.user.username} Profil'


class FlashcardSession(models.Model):
    invitation_hash = models.CharField('Validation hash', max_length=6)
    host = models.ForeignKey(Profile, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return self.invitation_hash


class Flashcard(models.Model):
    ABCD_CHOICES = (
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
        ('d', 'D'),
    )
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    visibility = models.BooleanField()
    question = models.CharField('Question', max_length=300)
    is_abcd = models.BooleanField(default=True)
    is_openquestion = models.BooleanField(default=False)
    a = models.CharField('Option a', max_length=50, default=0)
    b = models.CharField('Option b', max_length=50, default=0)
    c = models.CharField('LOption c', max_length=50, default=0)
    d = models.CharField('Option d', max_length=50, default=0)
    abcd_answer = models.CharField(max_length=1, choices=ABCD_CHOICES, default='a')
    correct_answer = models.CharField('Correct answer', max_length=300, default=0)

    def __str__(self):
        return self.question


class UserGroup(models.Model):
    group_name = models.CharField('Group name', max_length=50)

    def __str__(self):
        return self.group_name


class Membership(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, default=0)
    user_group = models.ForeignKey(UserGroup, on_delete=models.CASCADE, default=0)
    role = models.CharField('Role', max_length=50)

    def __str__(self):
        return self.role


class AnswerFlashcard(models.Model):
    flash_card = models.ForeignKey(Flashcard, on_delete=models.CASCADE, default=0)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, default=0)
    answer = models.CharField('Answer', max_length=300)

    def __str__(self):
        return self.answer


class AssignedFlashcard(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, default=0)
    flash_card = models.ForeignKey(Flashcard, on_delete=models.CASCADE, default=0)
    expiration_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user) + " - " + self.flash_card.question