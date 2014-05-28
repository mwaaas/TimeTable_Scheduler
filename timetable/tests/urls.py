from django.core.urlresolvers import reverse
from django.test import TestCase
import timetable.urls as Url
from timetable.views import  *

__author__ = 'mwas'


class UrlTestCase(TestCase):

    def test_urls(self):


        self.assertEqual(reverse("index_view"), '/timetable/index/', "add index_view url")


        self.assertEqual(reverse('add_unit_view'), '/timetable/add_unit/')

        self.assertEqual(reverse('add_group_view'), '/timetable/add_group/')

        self.assertEqual(reverse('add_lecture_view'), '/timetable/add_lecture/')

        self.assertEqual(reverse('add_lecture_room_view'), '/timetable/add_lecture_room/')

    def test_add_group_unit_view(self):

        self.assertEqual(reverse('add_group_unit_view', args=["compSci1yr"]), '/timetable/add_group_unit/compSci1yr/')
        self.assertEqual(reverse('add_lecture_unit_view', args=["29394168"]), '/timetable/add_lecture_unit/29394168/')

    def test_number_of_urls(self):
        self.assertEqual(len(Url.urlpatterns), 21, "urls specified in the timtable url should be 7")






