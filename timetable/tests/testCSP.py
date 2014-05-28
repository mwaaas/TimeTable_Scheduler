__author__ = 'mwas'
from django.test import TestCase
from timetable.models import *
from timetable.scheduler.CSP import *
from itertools import *

class TestCSPOne(TestCase):
    def setUp(self):
        Group.objects.create(groupId="comp/2", groupCapacity=50,
                             groupName="bachelor of computer science first year")
        Group.objects.create(groupId="biochem/2",groupCapacity=50,
                             groupName="Bachelor of biochemistry")
        Group.objects.create(groupId="biochem/3",groupCapacity=50,
                             groupName="Bachelor of biochemistry")


        Unit.objects.create(unitCode= "biochem110", unitHours= 10, unitName= "biochem")
        Unit.objects.create(unitCode="com320", unitHours=8, unitName="compiler")
        Unit.objects.create(unitCode="com321", unitHours=12, unitName="computer application")
        Unit.objects.create(unitCode="biochem220",unitHours=10,unitName="advanceBiochem")

        Lecture.objects.create(lectureId="29394168", lectureName="mwas")
        Lecture.objects.create(lectureId= "30294168", lectureName="isaac karanja")
        Lecture.objects.create(lectureId="31394168",lectureName="Bosire")


        UnitGroup(unitCode=Unit.objects.get(unitCode = "com320"),
                  group=Group.objects.get(groupId="comp/2"),
                  lecture=Lecture.objects.get(lectureId="29394168")).save()
        UnitGroup(unitCode=Unit.objects.get(unitCode="com321"),
                  group=Group.objects.get(groupId="comp/2"),
                  lecture=Lecture.objects.get(lectureId="29394168")).save()
        UnitGroup(unitCode=Unit.objects.get(unitCode="biochem110"),
                  group=Group.objects.get(groupId="biochem/2"),
                   lecture=Lecture.objects.get(lectureId="30294168")).save()
        UnitGroup(unitCode=Unit.objects.get(unitCode="biochem220"),
                  group=Group.objects.get(groupId="biochem/3"),
                  lecture=Lecture.objects.get(lectureId="31394168")).save()




        UnitLecture(unitCode =Unit.objects.get(unitCode="com320"),
                    lecture=Lecture.objects.get(lectureId="29394168")).save()
        UnitLecture(unitCode=Unit.objects.get(unitCode="biochem110"),
                    lecture=Lecture.objects.get(lectureId="30294168")).save()
        UnitLecture(unitCode=Unit.objects.get(unitCode="com321"),
                    lecture=Lecture.objects.get(lectureId='29394168')).save()
        UnitLecture(unitCode=Unit.objects.get(unitCode="biochem220"),
                    lecture=Lecture.objects.get(lectureId='31394168')).save()
        UnitLecture(unitCode=Unit.objects.get(unitCode="biochem220"),
                    lecture=Lecture.objects.get(lectureId='30294168')).save()





    def test_variable(self):
        """variables should be tuple not list"""
        a = CSP_One().get_variable()
        self.assertIsInstance(a,tuple, "get variable should return tuple")
    def test_number_of_variable(self):
        sessions = 20
        a = CSP_One().get_variable()

        self.assertEqual(len(a), sessions, "variable returned hare many or less")

    def test_object_varible(self):
        a = CSP_One().get_variable()

        for i in a:
            self.assertIsInstance(i,Session,"variable should be instance of Session")

    #testing getDomain
    def test_getDomainParameter(self):
        """getDomain parameter should be called with one parameter
        parameter : Session"""

        self.assertRaises(TypeError,CSP_One().get_domain,'parameter')

    def test_getDomain_output(self):
        """get_domain should output a tuple"""
        session = Session("biochem/2","biochem110", "30294168", 'a')
        self.assertIsInstance(CSP_One().get_domain(),tuple, "output of get_domain should be "
                                                            "a tuple")
    def test_type_of_domain(self):
        """Domain should be of type Time"""
        session = Session("biochem/2","biochem110", "30294168", 'a')
        a = CSP_One().get_domain()
        for domain in a:
            self.assertIsInstance(domain,Time,"all domain should be of type"
                                                     "Time")

    def test_no_of_domain(self):
        session = Session("biochem/2","biochem110", "30294168", 'a')
        domains = CSP_One().get_domain()
        self.assertEqual(len(domains),40,"check the number of domain produced")

        d2 = CSP_One().get_domain()

        self.assertEqual(len(d2),40)

    #Testing is_assigned complete
    def test_constrain_structure(self):
        """ should return list of constrains

            the constrain consist of a pair of scope and rel
                scope is a tuple of the variable in the constrain
                rel is tuple of allowed values
        """

        constrains = CSP_One().get_constrains()

        self.assertIsInstance(constrains,list, "the constrains should be "
                                               "list of constraints")

        self.assertGreater(len(constrains), 0, "constrains should be more than one")


        constrain = constrains[0]

        self.assertIsInstance(constrain,tuple,"constain should be a tuple")

        self.assertEqual(len(constrain), 2, "constrain should be a tuple of two elements"
                                            "scope and relation")
        scope = constrain[0]

        self.assertIsInstance(scope,tuple,"scope should be a tuple")

        rel = constrain[1]

        self.assertIsInstance(rel,Relation, "relation should be a class Relation")









class TestTime(TestCase):

    def test_initialParameter(self):
        self.assertRaises(TypeError,Time)



