from django.core.urlresolvers import reverse
from django.http import response
from timetable.models import *
from timetable.Form import *
from timetable.views import *

from django.test import TestCase, SimpleTestCase


class TimetableViewTestCase(TestCase):

    def setUp(self):
        """create data : unit , group , UnitGroup , UnitLecture and lecture room
         and initianlize string representin data in form"""

        self.unit_information = "unit_information"
        self.group_information = "group_information"
        self.lecture_information = "lecture_information"
        self.group_unit_information = "group_unit_information"
        self.lecture_unit_information = "lecture_unit_information"
        self.lecture_room_informaiton = "lecture_room_information"


        Group.objects.create(groupId="compSci1yr", groupCapacity=50,
                             groupName="bachelor of computer science first year")


        Unit.objects.create(unitCode="com320", unitHours=90, unitName="compiler")

        Unit.objects.create(unitCode= "biochem110", unitHours= 10, unitName= "biochem")

        Lecture.objects.create(lectureId="29394168", lectureName="mwas")

        Lecture.objects.create(lectureId= "30294168", lectureName="isaac karanja")

        LectureRoom.objects.create(lectureRoom="lec2b", capacity=40)

        UnitGroup.objects.create(unitCode=Unit(unitCode="com320", unitHours=90, unitName="compiler"),
                                 group=Group(groupId='compSci1yr', groupCapacity=50,
                                               groupName='bachelor of computer science first year'))

        UnitLecture.objects.create(unitCode=Unit(unitCode="com320", unitHours=90, unitName="compiler"),
                                   lecture=Lecture(lectureId="29394168", lectureName="mwas"))



    def test_index_view(self):
        resp = self.client.get(reverse('index_view'))
        self.assertEqual(resp.status_code, 200, "status should be 200")

        self.page_reload(resp)


    def test_add_unit_view(self):
        unit_information = {"unitCode": "com320", "unitHours": 8, "unitName": "compiler"}
        resp = self.client.post(reverse('add_unit_view'), unit_information, follow=True)


        self.assertEquals(resp.status_code, 200, "problem with the add_unit_view url")

        # add_unit_view should render index template with the added information
        #unit_information_from_template = resp.context["unit_information"]

        #print "unit_information from template:",unit_information_from_template[1].unitCode
        #self.assertTrue(unit_information in unit_information_from_template, "add_unit_view is not"
                                                                            #"adding the recored")

        #reloads page with all information and forms in the context
        self.page_reload(resp)

        # should receive post request only
        #self.assertRaises(WrongRequest,self.client.get(reverse('add_unit_view')))


    def test_add_group_view(self):

        group_information = {"groupId": "biochem1yr", "groupCapacity": 50, "groupName":"Bachelor of"
                                                                                       "Biochemistry"}

        resp = self.client.post(reverse("add_group_view"),group_information, follow = True)

        self.assertEqual(resp.status_code, 200, "status code should be 200 for add_group_view")

        group_information_from_template = resp.context["group_information"]

        #self.assertTrue(group_information in group_information_from_template, "add_group_view is not"
                                                                              #"adding data")
        # should reload the page
        self.page_reload(resp)

        # should receive post request only
        #self.assertRaises(WrongRequest, self.client.get(reverse("add_group_view")))



    def test_add_group_unit_view(self):

        group_unit_information = {"groupId": "compSci1yr", "unitCode": "biochem110"}
        """
        resp = self.client.post(reverse("add_group_unit_view"), group_unit_information)
        reverse

        self.assertEqual(resp.status_code, 200, "status code should be 200 for add_group_unit_view")

        group_unit_information_from_template = resp.context["group_unit_information"]

        self.assertTrue(group_unit_information in group_unit_information_from_template, "add_group_unit"
                                                                                        "view is not "
                                                                                        "adding data")

        #should reload the page
        self.page_reload(resp)

        # should accept post request only
        self.assertRaises(WrongRequest, self.client.get(reverse("add_group_unit_view")))
        """
    def test_add_lecture_view(self):

        lecture_information = {"lectureId": "30394168", "lectureName": "isaac karanja"}

        resp = self.client.post(reverse("add_lecture_view"), lecture_information, follow=True)

        self.assertEqual(resp.status_code, 200)

        lecture_information_from_template = resp.context["lecture_information"]

        #self.assertTrue(lecture_information in lecture_information_from_template, "add_lecture_view does"
                                                                                  #"not add data")

        #should reload the page
        self.page_reload(resp)

        # should accept post request only
        #self.assertRaises(WrongRequest, self.client.get(reverse("add_lecture_view")))

    def test_add_lecture_unit_view(self):

        lecture_unit_information = {"unitCode":"biochem110", "lectureName":"isaac karanja"}
        """
        resp = self.client.post(reverse("add_lecture_unit_view", kwargs={'lectureId':"29394168"}))


        self.assertEqual(resp.status_code, 200)

        lecture_unit_information_from_template = resp.context["lecture_unit_information"]

        self.assertTrue(lecture_unit_information in lecture_unit_information_from_template,
                        "add_lecture_unit_view is not adding data")

        # should reload the page
        self.page_reload(resp)

        # should accept post only request
        self.assertRaises(WrongRequest, self.client.get(reverse("add_lecture_unit_view")))
        """
    def test_add_lecture_room_view(self):

        lecture_room_information = {"lectueRoom":"lec2a", "capacity":50}

        resp = self.client.post(reverse("add_lecture_room_view"), lecture_room_information, follow=True)

        self.assertEqual(resp.status_code, 200)

        lecture_room_information_form_template = resp.context["lectureRoom_information"]

        #self.assertTrue(lecture_room_information in lecture_room_information_form_template,
                        #"add_lecture_room_view does not add data")

        #should reload the page
        self.page_reload(resp)

        # should accept post only request
        #self.assertRaises(WrongRequest, self.client.get(reverse("add_lecture_room_view")))

    def page_reload(self, resp):
        self.assertTemplateUsed(resp, "index.html", "index template should be rendered")

        self.assertTrue("addUnitForm" in resp.context, " render index template with addUnitForm")
        self.assertTrue("addGroupForm" in resp.context, "render index template with addGroupForm")
        self.assertTrue("addLectureForm" in resp.context, "render index template with addLectureForm")
        self.assertTrue("addGroupUnitForm" in resp.context, "render index template with addGroupUnitForm")

        self.assertTrue("addLectureRoom" in resp.context, "render index template with addLectureRoomForm")


        self.assertEqual(resp.context["addGroupForm"], AddGroup, "AddGroup form not rendered in index template")
        self.assertEqual(resp.context["addLectureForm"], AddLecture, "AddLecture form not rendered in index template")




        self.assertTrue("unit_information" in resp.context, "should render context with unit information")
        self.assertTrue("group_information" in resp.context, "should render webpage with context that "
                                                             "contain group information")
        self.assertTrue("unitGroup_information" in resp.context, "context should contain unit group information")
        self.assertTrue("unitLecture_information" in resp.context, "context should contain unitlecture"
                                                                   "information")
        self.assertTrue("lecture_information" in resp.context, 'context should contain lecture information')
        self.assertTrue("lectureRoom_information" in resp.context, "context should contain lectureRoom"
                                                                   "information")

        #unit_information = resp.context["unit_information"]
        #unit_object = Unit.objects.get(unitCode="com320")
        #print 'unit_information:', unit_information[1].unitCode
        #self.assertEqual(unit_information[1], unit_object.unitCode, "should deliver the whole list")









































