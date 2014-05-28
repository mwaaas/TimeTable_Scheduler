from django.conf.urls import patterns
from django.conf.urls import *
from TimeTable_Scheduler import settings


__author__ = 'mwas'

urlpatterns = patterns('timetable.views',
                       url(r'^index/', 'index_view', name="index_view"),
                       url(r'^add_unit/', 'add_unit_view', name="add_unit_view"),
                       url(r'^add_group/', 'add_group_view', name="add_group_view"),
                       url(r'^add_lecture/', 'add_lecture_view', name="add_lecture_view"),
                       url(r'^add_lecture_room/', 'add_lecture_room_view',
                           name="add_lecture_room_view"),
                       url(r'^add_group_unit/([\w\s\W]+)/', 'add_group_unit_view', name='add_group'
                                                                                '_unit_view'),
                       url(r'^add_lecture_unit/([\w\s\W]+)/$', 'add_lecture_unit_view',
                           name="add_lecture_unit_view"),
                       url(r'^delete_unit/([\w\s\W]+)/', 'delete_unit_view', name='delete_unit_view'),
                       url(r'^delete_group/([\w\s\W]+)/', 'delete_group_view',name='delete_group'),
                       url(r'^update_unit/([\w\s\W]+)/', 'update_unit_view', name='update_unit'),
                       url(r'^update_page/([\w\s\W]+)/', 'update_page_view', name='update_page'),

                       url(r'^update_group/([\w\s\W]+)/', "update_group_view", name="update_group"),
                       url(r'^update_group_page/([\w\s\W]+)/',"update_group_page_view", name="update_group_page"),

                       url(r'^delete_group_unit/([\w\s\W]+)/([\w\s\W]+)/', "delete_group_unit_view", name="delete_group_unit"),

                       url(r'delete_lecture_room/([\w\s\W]+)/', 'delete_lecture_room_view', name = 'delete_lecture_room'),
                       url(r'update_lecture_room_page/([\w\s\W]+)/', 'lecture_room_update_page_view', name='lecture_room_update_page'),
                       url(r'update_lecture_room/([\w\s\W]+)/', 'update_lecture_room_view', name='update_lecure_room'),

                       url(r'delete_lecture/([\w\s\W]+)/', 'delete_lecture_view', name='delete_lecture'),
                       url(r'update_lecture_page/([\w\s\W]+)/', 'lecture_update_page_view', name='update_lecture_page'),
                       url(r'update_lecture/([\w\s\W]+)/', 'update_lecture_view', name='update_lecture'),
                       url(r'delete_lecture_unit/([\w\s\W]+)/([\w\s\W]+)/', 'delete_lecture_unit_view', name = 'delete_lecture_unit'),

                       url(r'schedule/','schedule_view', name='schedule'),

                       )






