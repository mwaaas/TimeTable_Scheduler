
from django.db import models


class Group(models.Model):
    groupId = models.CharField(verbose_name="group id",max_length=255, primary_key=True)  # primary key
    groupCapacity = models.IntegerField()
    groupName = models.CharField(max_length=500, blank=True, null=True)  # not required


class Unit(models.Model):

    unitCode = models.CharField(max_length=255, primary_key=True)
    unitHours = models.IntegerField()
    unitName = models.CharField(max_length=255, blank=True, null=True)  # not required


class Lecture(models.Model):

    lectureId = models.CharField(max_length=255, primary_key=True)  # primary key
    lectureName = models.CharField(max_length=255, blank=True, null=True) # not required


class UnitLecture(models.Model):

    unitCode = models.ForeignKey(Unit)
    lecture = models.ForeignKey(Lecture)


    class Meta:
        unique_together = ("unitCode", "lecture")



class UnitGroup(models.Model):
    unitCode = models.ForeignKey(Unit)
    group = models.ForeignKey(Group)
    lecture = models.ForeignKey(Lecture)

    class Meta:
        unique_together = ("unitCode", "group")


class LectureRoom(models.Model):
    lectureRoom = models.CharField(max_length=255, primary_key=True)
    capacity = models.IntegerField()

    def __str__(self):
        return str(self.lectureRoom)

    def __eq__(self, other):
        return str(self.lectureRoom) == str(other.lectureRoom)

class TimeTable(models.Model):
    group = models.ForeignKey(Group)
    unit = models.ForeignKey(Unit)
    lectureRoom = models.ForeignKey(LectureRoom)
    lectureId = models.ForeignKey(Lecture)
    time = models.CharField(max_length=255, primary_key=False)
    #sessionId = models.CharField()

    class Meta:

        unique_together = ("group", "unit", "lectureRoom",'time')







