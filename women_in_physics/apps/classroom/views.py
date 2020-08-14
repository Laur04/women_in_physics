from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.files import File
from django.core.files.storage import default_storage
from django.conf import settings
from django.template.loader import render_to_string

from .forms import CreateForm, SurveyForm, StudentResetForm
from .models import Classes, Post

def create(request):
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            class_name = form.cleaned_data['class_name'].split()
            class_name = ''.join(class_name)

            # check
            repeat_c = False
            repeat_t = False
            repeat_s = False
            repeat = False
            current_users = User.objects.all()
            for t in current_users:
                if t.username == form.cleaned_data['teacher_username']:
                    repeat_t = True
                if t.username == form.cleaned_data['student_username']:
                    repeat_s = True
            current_classes = Classes.objects.all()
            for c in current_classes:
                if c.name == class_name:
                    repeat_c = True
            if form.cleaned_data['teacher_username'] == form.cleaned_data["student_username"]:
                repeat = True
            if repeat_c or repeat_s or repeat_t or repeat:
                return render(request, 'classroom/create.html', context={'form':form, 'repeat_c':repeat_c, 'repeat_t':repeat_t, 'repeat_s':repeat_s})

            # create class
            new_teacher = User.objects.create_user(form.cleaned_data['teacher_username'], form.cleaned_data['teacher_email'], form.cleaned_data['teacher_password'])
            new_teacher.groups.add(Group.objects.get(name="teacher"))
            new_teacher.save()
            new_student = User.objects.create_user(form.cleaned_data['student_username'], "", form.cleaned_data['student_password'])
            new_student.groups.add(Group.objects.get(name="student"))
            new_student.save()
            new_class = Classes(name=class_name, teacher=new_teacher, student=new_student)
            new_class.save()
            return HttpResponseRedirect(reverse('classroom:classroom'))
        return render(request, 'classroom/create.html', context={'form':form})
    else:
        form = CreateForm()
        return render(request, 'classroom/create.html', context={'form':form})

@login_required
def reset_student(request):
    user = request.user
    if user.groups.filter(name="teacher").exists():
        if request.method == "POST":
            form = StudentResetForm(request.POST)
            if form.is_valid():
                student = user.class_teacher.student
                student.set_password(form.cleaned_data['new_password1'])
                student.save()
                return render(request, "registration/password_reset_complete.html", context={})
            return render(request, "classroom/password_reset.html", context={'form':form})
        else:
            form = StudentResetForm()
            return render(request, "classroom/password_reset.html", context={'form':form})
    else:
        return HttpResponse("You are not authorized to access this page.")

@login_required
def response(request):
    user = request.user
    classname = ""
    if user.groups.filter(name='student').exists():
        classname = user.class_student
    elif user.groups.filter(name='teacher').exists():
        classname = user.class_teacher
    else:  # user is trying to access as staff or superuser
        return HttpResponse("You are trying to access this page as a superuser or administrator. Please login as a teacher or student.")
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            find_class = Classes.objects.get(name=classname)

            new_id = "".join(form.cleaned_data['response'].split())[:60]

            new_post = Post(
                post_id=new_id,
                classes=find_class,
                response=form.cleaned_data['response']
            )
            new_post.save()

            return HttpResponseRedirect(reverse('classroom:classroom'))
        return render(request, 'classroom/survey.html', context={'form':form, 'error': True})
    else:
        form = SurveyForm()
        return render(request, 'classroom/survey.html', context={'form':form})

@login_required
def classroom(request):
    user = request.user
    person = ""
    classname = ""
    if user.groups.filter(name='student').exists():
        classname = user.class_student
        person = "student"
    elif user.groups.filter(name='teacher').exists():
        classname = user.class_teacher
        person = "teacher"
    else:  # user is trying to access as staff or superuser
        return HttpResponse("You are trying to access this page as a superuser or administrator. Please login as a teacher or student.")
    post_list = Post.objects.filter(classes=Classes.objects.get(name=classname))
    if person == 'teacher':
        return render(request, 'classroom/classroom.html', context={'post_list':post_list, "person": person})
    elif person == 'student':
        show_post_list = list()
        for item in post_list:
            if item.hidden == False:
                show_post_list.append(item)
        return render(request, 'classroom/classroom.html', context={'post_list':show_post_list, "person": person})

@login_required
def changestatus(request, post):
    to_change = Post.objects.get(post_id=str(post))
    to_change.changeStatus()
    return HttpResponseRedirect(reverse('classroom:classroom'))
