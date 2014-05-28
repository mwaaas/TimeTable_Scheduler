__author__ = 'mwas'
import string
from timetable import models
from timetable.scheduler.CSP import Relation

class SessionTwo(object):
    def __init__(self, identifier, time):
        self.__time = time
        self.__id = identifier

    def get_time(self):
        return self.__time

    def get_id(self):
        return self.__id

    def __eq__(self, other):
        return (self.get_id(), self.get_time()) == (other.get_id(), other.get_time())

    def __hash__(self):
        return hash((self.get_id(), self.get_time()))

    def __str__(self):
        return "id is:"+str(self.get_id())+' and '+str(self.get_time())


class Relation(object):
    def __init__(self, scope):
        self.scope = tuple(scope)

    def has_variable(self, variable):
        return variable in self.scope

    def is_valid(self, variable, value, assignment):

        for var in self.scope:
            if assignment.get(var, False) and var != variable:
                if value == assignment[var]:
                    return False

        return True

class CspTwo(object):
    def __init__(self):
        self.__variable_number = 0
    def get_variable(self):
        variable = []
        var = models.TimeTable.objects.all()


        for v in var:
            variable.append(SessionTwo(v.id, v.time))

        self.__variable_number = len(variable)
        return tuple(variable)

    def get_domain(self):
        value = models.LectureRoom.objects.all().exclude(lectureRoom = 'not Assigned')
        values = []
        for v in value:
            values.append(v.lectureRoom)
        values = tuple(values)

        domains = []

        for v in range(self.__variable_number):
            domains.append(values)
        return tuple(domains)

class ConstrainTwo(object):

    def __init__(self):
        self.letters = string.ascii_lowercase

    def get_constrains(self, variable):
        """returns constrain: all sesssion with the same time should not be assiged
            the same lecture hall"""
        time = variable.get_time()
        scope = []
        #gets all variables with the same time as the parameter varibale
        variables = models.TimeTable.objects.filter(time=time)

        for val in variables:
            scope.append(SessionTwo(val.id, val.time))
        scope = tuple(scope)
        return Relation(scope),


