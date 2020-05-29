from django.db import models
from django.contrib.auth.models import User

class Classes(models.Model):
    name = models.CharField('Class Name', unique=True, max_length=30)
    teacher = models.OneToOneField(User, related_name='class_teacher', on_delete=models.CASCADE)
    student = models.OneToOneField(User, related_name='class_student', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
        
class Post(models.Model):
    post_id = models.CharField(max_length=40)
    hidden = models.BooleanField(default=True)
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE)

    response = models.CharField(max_length=500)

    def __str__(self):
        return self.student_name

    def changeStatus(self):
        if self.hidden == True:
            self.hidden = False
        else:
            self.hidden = True
        self.save()