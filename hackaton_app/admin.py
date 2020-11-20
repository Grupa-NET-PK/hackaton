from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Profile)
admin.site.register(FlashcardSession)
admin.site.register(Flashcard)
admin.site.register(UserGroup)
admin.site.register(Membership)
admin.site.register(AnswerFlashcard)


