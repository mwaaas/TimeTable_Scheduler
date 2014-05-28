# Create your views here.
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from timetable.Form import *
from timetable.models import *
from timetable.scheduler.scheduler import *

import  pdb




class WrongRequest(Exception):
    pass

def dataToRender():
    group_information = Group.objects.all()
    lecture_data = Lecture.objects.all()

    unit_group_information = "unit_group_information"  # prefix for unit group info
    dataToRender = {"addUnitForm": AddUnit, "addGroupForm": AddGroup,
                            "addLectureForm": AddLecture, "addLectureRoom": AddLectureRoom,
                            "addGroupUnitForm": AddGroup,
                            "unit_information": Unit.objects.all(),
                            "unitGroup_information":UnitGroup.objects.all(),
                            "lecture_information": lecture_data,
                            "group_information": Group.objects.all(),
                            "unitLecture_information": UnitLecture.objects.all(),
                            "lectureRoom_information": LectureRoom.objects.all(),
                            "name":{"name":"mwas","com1":'com'},
                            "elementId":[],
                            "tab":None}


    for groupObj in group_information:

        dataToRender[str(groupObj.groupId)] = UnitGroup.objects.filter(group=groupObj)
        dataToRender[str(groupObj.groupId)+"form"] = AddGroupUnit(group=groupObj)

    for lecObj in lecture_data:
        dataToRender[lecObj.lectureId] = UnitLecture.objects.filter(lecture=lecObj)
        dataToRender[lecObj.lectureId+"form"] = AddLectureUnit(lecture=lecObj)

    return  dataToRender


def renderHomePage(request, data):

    return render_to_response("index.html", data,context_instance=RequestContext(request))



def index_view(request):
    logger.error('data to render:'+str(dataToRender()))
    return renderHomePage(request,dataToRender())


def add_unit_helper(request,addUnitForm , create_update="create"):

    if addUnitForm.is_valid():
        addUnitForm.save()
        dat = dataToRender()

    else:
        dat = dataToRender()
        if create_update == "create":
            dat["addUnitForm"] = addUnitForm
            dat["elementId"] = ["addUnit"]
        else:
            dat[create_update]=addUnitForm
            dat["elementId"] = [create_update]
    dat['tab']='#tabs-1'
    return renderHomePage(request, dat)

def add_unit_view(request):
    data = None
    if request.method == 'POST':
        addUnitForm = AddUnit(request.POST)
        return add_unit_helper(request,addUnitForm)

def delete_unit_view(request,unit_code):
    Unit.objects.get(unitCode = unit_code).delete()

    data = dataToRender()
    data["tab"] = "#tabs-1"

    return renderHomePage(request, data)

def update_unit_view(request,unit_code):
    a = Unit.objects.get(unitCode=unit_code)
    f = AddUnit(request.POST, instance=a)
    return add_unit_helper(request, f , unit_code)
def update_page_view(request,unit_code):
    data = dataToRender()
    data[unit_code] = AddUnit(instance=Unit.objects.get(unitCode=unit_code))
    data['tab']="#tabs-1"
    data["elementId"] = [unit_code]
    return renderHomePage(request, data)


def add_group_helper(request,add_group_form , save = 'save'):

    if add_group_form.is_valid():
        add_group_form.save()
        data = dataToRender()
    else:
        data = dataToRender()
        if save=='save':
            data["addGroupForm"] = add_group_form
            data["elementId"] = ["addGroup"]
        else:
            data[save+"form"] = add_group_form
            data["elementId"] = [save+"franco"]

    data["tab"] = "#tabs-2"
    return renderHomePage(request, data)

def add_group_view(request):
    add_group_form = AddGroup()
    if request.method == "POST":
        add_group_form = AddGroup(request.POST)
    return add_group_helper(request,add_group_form)


def delete_group_view(request,groupId):
    logger.error('groupId:'+groupId)
    Group.objects.get(groupId=groupId).delete()
    data = dataToRender()
    data["tab"] = "#tabs-2"
    return renderHomePage(request, data)

def update_group_view(request,groupId):
     a = Group.objects.get(groupId=groupId)
     f = AddGroup(request.POST, instance=a)
     return add_group_helper(request, f , groupId)

def update_group_page_view(request, groupId):
    data = dataToRender()
    data[groupId+"form"] = AddGroup(instance=Group.objects.get(groupId=groupId))
    data['tab']="#tabs-2"
    data["elementId"] = [groupId+"franco"]
    return renderHomePage(request, data)


def add_group_unit_view(request,groupId):
    logger.error('groupId:'+groupId)
    if request.method =="POST":
        form_data = request.POST.copy()
        form_data['group'] = groupId
        groupUnitForm = AddGroupUnitForm(form_data)

        if groupUnitForm.is_valid():
            logger.error('data is saved')
            groupUnitForm.save()
            data = dataToRender()
            data["elementId"].append(groupId+"mwas")

        else:
            data = dataToRender()
            f = AddGroupUnit(group =Group.objects.get(groupId=groupId))
            f.data = form_data
            data[str(groupId+"form")] = f  #AddGroupUnit(group=Group.objects.get(groupId=groupId), data=form_data)
            data["elementId"].append(groupId)
            data["elementId"].append(groupId+"mwas")
    data["tab"] = "#tabs-2"
    return renderHomePage(request, data)

def delete_group_unit_view(request, groupId, unitCode):
    UnitGroup.objects.filter(group=groupId).filter(unitCode=unitCode).delete()

    data=dataToRender()
    data["tab"] = "#tabs-2"
    data["elementId"].append(groupId+"mwas")

    return  renderHomePage(request,data)


def add_lecture_view(request):
    if request.method == 'POST':
        add_lecture_form = AddLecture(request.POST)

        if (add_lecture_form.is_valid()):
            add_lecture_form.save()
            data = dataToRender()
        else:
            data = dataToRender()
            data["addLectureForm"] = add_lecture_form
            data["elementId"].append("addLecture")
        data['tab'] = "#tabs-3"
        return renderHomePage(request, data)

def delete_lecture_view(request , lectureId):
    Lecture.objects.get(lectureId=lectureId).delete()
    data = dataToRender()
    data['tab'] = "#tabs-3"
    return renderHomePage(request,data)

def lecture_update_page_view(request, lectureId):
    data = dataToRender()
    data[lectureId+"form"] = AddLecture(instance=Lecture.objects.get(lectureId=lectureId))
    data['tab'] = "#tabs-3"
    data["elementId"] = [lectureId+"franco"]
    return renderHomePage(request, data)

def update_lecture_view(request , lectureId):
    a = Lecture.objects.get(lectureId=lectureId)
    f = AddLecture(request.POST, instance=a)

    if f.is_valid():
        f.save()
        data = dataToRender()

    else:
        data = dataToRender()
        data[lectureId+"form"]=f
        data["elementId"] = [lectureId+"franco"]
    data['tab'] = "#tabs-3"

    return renderHomePage(request, data)

def add_lecture_unit_view(request, lectureId):
    form_data = request.POST.copy()
    form_data['lecture'] = lectureId
    lectureUnitForm = AddLectureUnitForm(form_data)

    if lectureUnitForm.is_valid():
        lectureUnitForm.save()
        data = dataToRender()
        data["elementId"].append(lectureId+"mwas")

    else:
        data = dataToRender()
        f = AddLectureUnit(lecture=Lecture.objects.get(lectureId=lectureId))
        f.data = form_data
        data[str(lectureId+"form")] = f  #AddGroupUnit(group=Group.objects.get(groupId=groupId), data=form_data)
        data["elementId"].append(lectureId)
        data["elementId"].append(lectureId+"mwas")
    data["tab"] = "#tabs-3"
    return renderHomePage(request, data)

def delete_lecture_unit_view(request,lectureId,unitCode):
    UnitLecture.objects.filter(lecture=lectureId).filter(unitCode=unitCode).delete()

    data=dataToRender()
    data["tab"] = "#tabs-3"
    data["elementId"].append(lectureId+"mwas")

    return  renderHomePage(request,data)

def add_lecture_room_view(request):

    if request.method == 'POST':
        add_lecture_room_form = AddLectureRoom(request.POST)

        if add_lecture_room_form.is_valid():
            add_lecture_room_form.save()
            data = dataToRender()

        else:
            data = dataToRender()
            data["addLectureRoom"] = add_lecture_room_form
            data["elementId"].append("addLectureRoom")
        data['tab'] = "#tabs-4"
        return renderHomePage(request, data)

    return HttpResponseRedirect(reverse("index_view"))

def delete_lecture_room_view(request, lecRum):
    LectureRoom.objects.get(lectureRoom=lecRum).delete()
    data = dataToRender()
    data['tab'] = "#tabs-4"
    return renderHomePage(request, data)

def lecture_room_update_page_view(request , lecRum):
    data = dataToRender()
    data['tab'] = "#tabs-4"
    data[lecRum+"updateForm"] = AddLectureRoom(instance=LectureRoom.objects.get(lectureRoom =lecRum))
    data["elementId"].append((lecRum+'form'))

    return renderHomePage(request, data)

def update_lecture_room_view(request , lecRum):
    lecRoom = LectureRoom.objects.get(lectureRoom=lecRum)
    f = AddLectureRoom(request.POST,instance=lecRoom)

    if f.is_valid():
        f.save()
        data = dataToRender()

    else:
        data = dataToRender()
        data[lecRum+"updateForm"] = f
        data["elementId"].append(lecRum+'form')
    data['tab'] = "#tabs-4"
    return renderHomePage(request, data)

def schedule_view(request):
    data = schedule()
    t = TimeTable.objects.all()
    return render_to_response("timetable.html", {'schedule': data, 'timetable': t},
                              context_instance=RequestContext(request))








