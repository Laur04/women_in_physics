from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from .forms import CreateForm, LoginForm, SurveyForm
from .models import Classes, Teacher, Student, Post

def create(request):
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            class_name = form.cleaned_data['class_name'].split(' ')
            class_name = ''.join(class_name)

            # check
            repeat_c = False
            repeat_t = False
            repeat_s = False
            current_teachers = Teacher.objects.all()
            for t in current_teachers:
                if t.name == form.cleaned_data['teacher_username']:
                    repeat_t = True 
            current_students = Student.objects.all()
            for s in current_students:
                if s.name == form.cleaned_data['student_username']:
                    repeat_s = True
            current_classes = Classes.objects.all()
            for c in current_classes:
                if c.name == class_name:
                    repeat_c = True
            if repeat_c or repeat_s or repeat_t:
                return render(request, 'classroom/create.html', context={'form':form, 'repeat_c':repeat_c, 'repeat_t':repeat_t, 'repeat_s':repeat_s})

            # create class
            new_teacher = Teacher(name=form.cleaned_data['teacher_username'])
            new_teacher.save()
            new_student = Student(name=form.cleaned_data['student_username'])
            new_student.save()
            new_class = Classes(name=class_name, teacher=new_teacher, student=new_student)
            new_class.save()
            return HttpResponseRedirect(reverse('classroom:login'))
        return render(request, 'classroom/create.html', context={'form':form})
    else:
        form = CreateForm()
        return render(request, 'classroom/create.html', context={'form':form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                person = Teacher.objects.get(name=form.cleaned_data['username'])
                classroom = person.classes
                return HttpResponseRedirect(reverse('classroom:classroom', kwargs={'classname':classroom, 'person':'teacher'}))
            except ObjectDoesNotExist:
                try:
                    person = Student.objects.get(name=form.cleaned_data['username'])
                    classroom = person.classes
                    return HttpResponseRedirect(reverse('classroom:classroom', kwargs={'classname':classroom, 'person':'student'}))
                except ObjectDoesNotExist:
                    return render(request, 'classroom/login.html', context={'form':form, 'error':True})
        return render(request, 'classroom/login.html', context={'form':form})
    else:
        form = LoginForm()
        return render(request, 'classroom/login.html', context={'form':form})

def survey(request, classname):
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            find_class = Classes.objects.get(name=classname)
            new_id = form.cleaned_data['ans'].split(' ')
            new_id = ''.join(new_id)[:40]
            new_post = Post(post_id=new_id, answer=form.cleaned_data['ans'], classes=find_class)
            new_post.save()
            return HttpResponseRedirect(reverse('classroom:classroom', kwargs={'classname':classname, 'person':'student'}))
        return render(request, 'classroom/survey.html', context={'form':form})
    else:
        form = SurveyForm()
        return render(request, 'classroom/survey.html', context={'form':form})

def classroom(request, classname, person):
    post_list = Post.objects.filter(classes=Classes.objects.get(name=classname))
    if person == 'teacher':
        return render(request, 'classroom/classroom.html', context={'post_list':post_list, 'classname':classname, 'person':person})
    elif person == 'student':
        show_post_list = list()
        for item in post_list:
            if item.hidden == False:
                show_post_list.append(item)
        return render(request, 'classroom/classroom.html', context={'post_list':show_post_list, 'classname':classname, 'person':person})

def changestatus(request, classname, person, post):
    to_change = Post.objects.get(post_id=str(post))
    to_change.changeStatus()
    return HttpResponseRedirect(reverse('classroom:classroom', kwargs={'classname':classname, 'person':'teacher'}))

