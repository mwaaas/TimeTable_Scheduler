
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist



__author__ = 'mwas'

from timetable import models
from django import forms



class AddUnit(forms.ModelForm):

    class Meta:
        def __init__(self):
            pass

        model = models.Unit


class AddGroup(forms.ModelForm):

    class Meta:
        model = models.Group



class AddLecture(forms.ModelForm):

    class Meta:
        model = models.Lecture


class AddLectureRoom (forms.ModelForm):

    class Meta:
        model = models.LectureRoom



class AddGroupUnit(forms.ModelForm):

    #unitCode= forms.ModelMultipleChoiceField(models.UnitGroup.objects.filter(group=group))

    def __init__(self, *args,**kwargs):
        group = kwargs.pop('group')
        super(AddGroupUnit,self).__init__(*args,**kwargs)

        units_done = models.UnitGroup.objects.filter(group = group)

        units = list(models.Unit.objects.all())

        for b in units_done:
            try:
                units.remove(b.unitCode)
            except ValueError:
                continue


        choices = []
        for a in units:
            choices.append([a.unitCode,a.unitCode])
        self.fields['unitCode'] = forms.ChoiceField(choices=choices)

        lectures = models.Lecture.objects.all()
        choices2 = []
        for lec in lectures:
            choices2.append([lec.lectureId,lec.lectureName])
        self.fields['lecture'] = forms.ChoiceField(choices=choices2)


    class Meta:
        model = models.UnitGroup
        exclude = 'group'
class AddGroupUnitForm(forms.ModelForm):
    class Meta:
        model = models.UnitGroup

class AddLectureUnitForm(forms.ModelForm):
    class Meta:
        model = models.UnitLecture
class AddLectureUnit(forms.ModelForm):

    def __init__(self, *args,**kwargs):
        lecture = kwargs.pop('lecture')
        super(AddLectureUnit,self).__init__(*args,**kwargs)

        units_done = models.UnitLecture.objects.filter(lecture=lecture)

        units = list(models.Unit.objects.all())

        for b in units_done:
            try:
                units.remove(b.unitCode)
            except ValueError:
                continue


        choices = []
        for a in units:
            choices.append([a.unitCode,a.unitCode])
        self.fields['unitCode'] = forms.ChoiceField(choices=choices)


    class Meta:
        model = models.UnitLecture
        exclude = 'lecture'



