__author__ = 'mwas'
from timetable.models import *
from TimeTable_Scheduler.settings import LOGGING
import string
import itertools
import logging
import pdb

logger = logging.getLogger(__name__)
logging.basicConfig()

class LectureTime(object):
    def __init__(self,unitCode,time):
        self.unitCode = unitCode
        self.time = time

class BaseTime(object):
    def __init__(self):
        self.allTime = []


        for i in range(1, 6):
            for t in range(8, 16):
                self.allTime.append((Time(i, t, 2)))
        self.allTime = tuple(self.allTime)


class Time(object):
    def __init__(self, day, hour, duration):
        self.day = int(day)
        self.hour = int(hour)
        self.duration = int(duration)
        self.days = ('Monday', 'Tuesday', 'Wensday', 'Thursday', 'Friday')

    def getDay(self):
        return self.day

    def getHour(self):
        return self.hour

    def get_duration(self):
        return  self.duration

    def to_database_format(self):
        t = str(self.day)+':'+str(self.hour)+':'+str(self.duration)
        return t

    def __str__(self):
        txt = self.days[int(self.day)-1] + "  ("

        starting_time = self.hour
        end_time = self.hour + self.duration
        if starting_time > 12:
            starting_time -= 12
            starting_time = str(starting_time) + " Pm"
        else:
            starting_time = str(starting_time) + ' Am'

        if end_time > 12 :
            end_time -=12
            end_time = str(end_time) + " Pm"
        else:
            end_time = str(end_time) + " Am"

        txt += starting_time + "--"+end_time+" )"

        return txt

    def __eq__(self, other):
        return (self.day, self.hour, self.duration) == (other.day, other.hour, other.duration)



class Relation(object):
    """relation used to define relation in constrains"""
    def __init__(self, scope):
        self.scope = scope


    def has_variable(self, variable):
        return variable in self.scope

    def is_valid(self, variable, value, assignment):
        for var in self.scope:

            if assignment.get(var, False) and var != variable:
                if value == assignment[var]:
                    return False
        return True


class Session(object):
    def __init__(self, groupId, unitCode, lecturer, identifier):
        self.groupId = groupId
        self.unitCode = unitCode
        self.identifier = identifier
        self.lecturer = lecturer

    def get_groupId(self):
        return self.groupId

    def get_unitCode(self):
        return self.unitCode

    def get_lecturer(self):
        return self.lecturer

    #def __cmp__(self, other):
    #    if self.get_groupId() != other.get_groupId:
    #        return False
    #
    #    elif self.get_lecturer() != other.get_lecturer():
    #        return False
    #
    #    elif self.get_unitCode() != other.get_unitCode():
    #        return False
    #
    #    elif self.identifier != other.identifier:
    #        return False
    #    return True



    def __contains__(self, item):
        #pdb.set_trace()
        for i in item:
            if self.__cmp__(i):
                return True
        return False

    def __str__(self):
        a = self.groupId + "  "
        a += self.get_unitCode() + "  "
        a += self.lecturer +' '
        a += self.identifier
        return a

    def __hash__(self):
        return hash((self.groupId,self.unitCode,self.lecturer,self.identifier))

    def __eq__(self, other):
        return (self.groupId, self.unitCode, self.lecturer, self.identifier) == (other.groupId, other.unitCode,
                                                                                 other.lecturer, other.identifier)



class CSP(object):
    """  this class is used by Backtracking to assign domains  .
            parameters:
                    variable -> tuple
                    domain -> tuple
                    constarin -> class entailing the following methond
                                getConstrain(variable) which  return all the constrain
                                                    associated with the variable

            lenght of varible and domain are supossed to be the same
            example varible (x,y)
                    domain  ((a,b),(b,c))

                    if the domain has one element then all varible have the same getDomain

                    constrains is a set of constraints
                        each element in a constrain is pair of <scope> and <relation>
                        <scope> is a tuple containg variables involved in that constrain
                        <relation> is a set of values the the scope can take

                        relation can be defined explicitly and abstractly
                            for instance : varible A and B both have domain of x and y
                            constrain is that both take different value

                            to define explicitly:  ((A,B),((x,y),(y,x))

                            to define abstractly: ((A,B),Relation) where the method get_values is called with the instance
                            of Relation to result in (x,y),(y,x)
    """
    def __init__(self, variables, domains, Constrain):
        if len(variables) != len(domains):
            logger.error("varibles and domain should have the save length")
        self.variables = variables
        self.domains = domains
        self.constrain = Constrain

    def getDomain(self, variable):
        #pdb.set_trace()
        return self.domains[self.variables.index(variable)]

    def getConstrain(self, variable):
        """Returns all the constrains associated with the variable"""
        return self.constrain.get_constrains()

    def set_domain(self, variable, values):
        if not isinstance(values, tuple):
            values = tuple(values)

        self.domains = list(self.domains)
        self.domains[self.variables.index(variable)] = values
        self.domains = tuple(self.domains)




class CSP_One(object):

    def __init__(self):
        self.__number = -1  # number of variable
        self.letters = string.ascii_lowercase

    def get_variable(self):
        variable = []
        #get list of all groups in the database
        groups = Group.objects.all()

        for group in groups:
            #gets list of all units taken by the group
            unitGroup = UnitGroup.objects.filter(group=group)

            for unit in unitGroup:
                #create a Session object for all group and units
                #Each unit has (hours/2) sessions
                session_number = int(unit.unitCode.unitHours /2.0)

                for s in range(session_number):
                    #append session to variable
                    variable.append(Session(group.groupId,unit.unitCode_id,unit.lecture.lectureId,
                                            self.letters[s]))
        self.__number = len(variable)
        return tuple(variable)

    def get_domain(self):
        domain = []

        time = BaseTime().allTime
        for i in range(self.__number):
            domain.append(time)

        return tuple(domain)

class Constrain(object):

    def __init__(self):
        self.letters = string.ascii_lowercase

    def get_constrains(self, variable):
        """returns all constrains that the variable participate in """

        return self.__first_constrain(variable), self.__second_constrain(variable) # adds the two constrains in a tuple



    def __first_constrain(self, variable):
        group_id = variable.get_groupId()  # variable is of type Session

        unit_group = UnitGroup.objects.filter(group_id=group_id)

        # contains all the variables participating in the constrain including the parameter variable
        scope = []  # contains all variables with the same group and unit
        for unit in unit_group:
            #each unit is divided into session of 2hours . From the specified hours per week specified in Unit
            session_number = int(unit.unitCode.unitHours /2)
            for i in range(session_number):
                scope.append(Session(unit.group_id, unit.unitCode_id, unit.lecture_id, self.letters[i]))

        scope = tuple(scope)  # scope should be tuple

        #first constrain : all session with the same group and unit should not have the same time value
        return Relation(scope)

    def __second_constrain(self, variable):
        lecture = variable.lecturer   # lecturer teaching the session

        # all the units sharing lecture with the variable
        shared_lectures = UnitGroup.objects.filter(lecture_id=lecture)

        scope = []  # contains all variable with the same lecturer
        for lec in shared_lectures:
            #each unit is divided into session of 2 hours
            session_number = int(lec.unitCode.unitHours)/2

            for i in range(session_number):
                scope.append(Session(lec.group_id, lec.unitCode_id, lec.lecture_id, self.letters[i]))

        scope = tuple(scope)   # scope should be a tuple

        # second constrain all session sharing  a lecturer should have different time values
        return Relation(scope)

    def __third_constrain(self, variable):
        pass





