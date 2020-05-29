from django import forms

class CreateForm(forms.Form):
    class_name = forms.CharField(max_length=30, required=True)
    teacher_username = forms.CharField(max_length=30, required=True)
    teacher_password = forms.CharField(max_length=30, required=True)
    teacher_email = forms.EmailField(required=True)
    student_username = forms.CharField(max_length=30, required=True)
    student_password = forms.CharField(max_length=30, required=True)

class SurveyForm(forms.Form):
    response = forms.CharField(max_length=500, widget=forms.Textarea)

class StudentResetForm(forms.Form):
    new_password1 = forms.CharField(max_length=30, required=True)
    new_password2 = forms.CharField(max_length=30, required=True)

    def is_valid(self):
        valid = super(StudentResetForm, self).is_valid()
        return self.cleaned_data["new_password1"] == self.cleaned_data["new_password2"]
