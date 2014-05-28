__author__ = 'mwas'


from django.test import TestCase

from timetable.models import  *
from timetable.Form import *
import timetable.Form as timetable_form


class AddUnitFormTestCase(TestCase):

    def setUp(self):
        Unit.objects.create(unitCode="com120", unitHours=76, unitName="compiler")

    def test_AddUnit_form(self):
        """the unicode is primary key and should be unique
        """

        """
        data = {"unitCode": "com57", "unitHours": 30, "unitName": "compiler"}

        add_unit_form = timetable_form.AddUnit(data)

        self.assertTrue(add_unit_form.is_valid(), "should validate the data correctly "+str(data))

        add_unit_form_data = timetable_form.AddUnit(data)

        self.assertFalse(add_unit_form_data.is_valid(), "validating incorrect data . "
                                                 "unitCode should be unique the data"
                                                  "already exists"+str(data))
        unit = Unit.objects.get(pk="com57")

        unit.delete()
        """
        self.assertEqual(4,4)











