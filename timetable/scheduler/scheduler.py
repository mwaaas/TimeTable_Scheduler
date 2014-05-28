__author__ = 'mwas'
from timetable.scheduler.CSP import *
from timetable.scheduler.BackTrack import *
from timetable.scheduler.csp_two import *


def schedule():
    TimeTable.objects.all().delete()
    csp_one = CSP_One()
    csp = CSP(csp_one.get_variable(), csp_one.get_domain(), Constrain())
    assignments = BackTrackSearch(csp).backtrack()
    if assignments :
        save_assignments(assignments)

        csp_two = CspTwo()
        csp_t = CSP(csp_two.get_variable(), csp_two.get_domain(), ConstrainTwo())
        assignments_two = BackTrackSearch(csp_t).backtrack()

        msg = {}
        for i in assignments_two:
            msg[str(i)] = str(assignments_two[i])
        logger.error('assignment->'+str(msg))
        if assignments_two:
            save_assignment_two(assignments_two)
            logger.error('assignment passed')
        return True
    return False

def save_assignments(assig):

    #pdb.set_trace()
    for variables in assig:
        #pdb.set_trace()
        TimeTable(group_id=variables.get_groupId(),
                  unit_id=variables.get_unitCode(),
                  lectureRoom_id="not Assigned",
                  time=assig[variables].to_database_format(),
                  lectureId_id=variables.get_lecturer()
                  ).save()


def save_assignment_two(assig):
    #pdb.set_trace()
    for variables in assig:
        a = TimeTable.objects.get(id=variables.get_id())
        a.lectureRoom_id = assig[variables]
        a.save()






