from django.contrib import admin
from .models import User, Teacher, Student, Question, Subject, Subtopic, BKT, Quiz

''' Each of the following registers the applicable model within the Django admin site.
This allows for developers to easily view the data within the database and update this 
as required. '''

admin.site.register(User)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Question)
admin.site.register(Subject)
admin.site.register(Subtopic)
admin.site.register(BKT)
admin.site.register(Quiz)