from django.db import models

class Teacher(models.Model):
    name = models.CharField('Username', max_length=30)

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField('Username', max_length=30)

    def __str__(self):
        return self.name

class Classes(models.Model):
    name = models.CharField('Class Name', unique=True, max_length=30)
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE)
    student = models.OneToOneField(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
        
class Post(models.Model):
    post_id = models.CharField(max_length=40)
    answer = models.TextField(max_length=10000)
    hidden = models.BooleanField(default=True)
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer

    def changeStatus(self):
        if self.hidden == True:
            self.hidden = False
        else:
            self.hidden = True
        self.save()