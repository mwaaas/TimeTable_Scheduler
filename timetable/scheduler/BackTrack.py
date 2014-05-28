__author__ = 'mwas'
from timetable.scheduler.CSP import *
import pdb
import random



class BackTrackSearch(object):
    """ This object contains methods to do bactrack search given csp
                parameter :
                 CSP   : constrain satisfaction problem definition
                 """
    def __init__(self,csp):
        self.__csp = csp
        self.__assignment = {}
        self.__inference_data = {}

    def __assignment_is_complete(self):
        keys = self.__assignment

        variable = self.__csp.variables

        for val in variable:
            if val not in keys:
                return False

        return True

    def __unassigned_variables(self):
        """returns all the variables that are not assigned"""
        unsigned_variables = []
        for variables in self.__csp.variables:
            if variables not in self.__assignment:
                unsigned_variables.append(variables)

        return tuple(unsigned_variables)
    def __select_unassigned_variable(self):
        keys = self.__assignment.keys()
        #logger.error('keys->'+str(keys))
        variables = self.__csp.variables

        #for val in variables:
            #logger.error('value select->'+str(val))

            #if not val in keys:
        #    #    logger.error('ans->'+str(val))
        #    #    return val
        #    for v in keys:
        #        if v == val:
        #            break
        #    logger.error('ans->'+str(val))
        #    return val

        return self.__unassigned_variables()[0]


    def __test_value_consistency(self, constrain, variable, value):

        if constrain.has_variable(variable):
            return constrain.is_valid(variable, value, self.__assignment)
        else:
            raise ValueError

    def value_is_consistent(self, variable, value):
        """returns boolean if variable is consitent with the value"""
        constrains = self.__csp.constrain.get_constrains(variable)

        for constrain in constrains:
            if self.__test_value_consistency(constrain, variable, value):
                continue
            else:
                return False
        return True



    def inference(self, variable, value):
        return self.forward_checking(variable,value)


    def del_inference(self, inference):
        """adds all the values that had been deleted by the inference

        parameter inference  is a dictionary containing variables an the values deleted
        """

        for variable in inference:
            domains = list(self.__csp.getDomain(variable))

            deleted_values = inference[variable]

            for value in deleted_values:
                if value not in domains:
                    domains.append(value)

            self.__csp.set_domain(variable, tuple(domains))

    def forward_checking(self, variable, value):
        """
        deletes the value in other unassinged_variables if it is not consistent

        assumes that:
                value is already consistent to the assignments
                variable has be already added to the assignment
        """

        unassinged_variables = self.__unassigned_variables()
        inference = {}

        for val in unassinged_variables:
            values = self.__csp.getDomain(val)   # values of the variable
            removed_values = []

            values = list(values)
            # if any value in the variable is inconsistent to be removed
            for v in values:
                if not self.value_is_consistent(val, v):
                    try:
                        values.remove(v)
                        removed_values.append(v)
                    except ValueError:
                        raise ValueError

            #if any values have been removed form values add to the inference
            if removed_values:
                inference[val] = tuple(removed_values)
                self.__csp.set_domain(val, tuple(removed_values))

            if len(values) == 0:
                if inference:
                    self.__inference_data[variable] = inference

                return False
        if inference:
            self.__inference_data[variable] = inference

        return True

    def __domain_random_generator(self, domain):
        """ domain should be a tuple
        """
        used_domain = []

        domains= list(domain)
        dom = domains[:]
        domain =tuple(domains)

        while len(dom) != 0:
            value = random.choice(dom)
            dom.remove(value)
            yield value



    def backtrack(self):

        if self.__assignment_is_complete():
            return self.__assignment

        variable = self.__select_unassigned_variable()

        if variable:  # if there is variable
            domains = self.__csp.getDomain(variable)
            random_domain = self.__domain_random_generator(domains)
            for value in random_domain:
                valid = self.value_is_consistent(variable, value)
                if valid:
                    self.__assignment[variable] = value  # add value if it is consistent with the constarins
                    #inference boolean
                    #warning method inference alters domain data of variables
                    #inference = self.inference(variable, value)

                    #logger.error('inference->'+str(inference))
                    #if inference:
                    result = self.backtrack()

                    if result:
                        return result
                    # if a failure noticed by either inference or backtrack
                    #remove the assignment and undo the changes done by inference
                    inference = self.__inference_data.get(variable, False)

                    #if inference:
                        #self.del_inference(inference)
                    del self.__assignment[variable]
        return False








