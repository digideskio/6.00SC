# Problem Set 7: Simulating the Spread of Disease and Virus Population Dynamics 
# Name: Shouvik Roy
# Collaborators:
# Time: 2 hours 30 mins

import numpy
import random
import pylab

''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''


#
# PROBLEM 1
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):

        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.
        maxBirthProb: Maximum reproduction probability (a float between 0-1)
        clearProb: Maximum clearance probability (a float between 0-1).
        """

        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def doesClear(self):

        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step.
        returns: True with probability self.clearProb and otherwise returns
        False.
        """

        return random.random() < self.clearProb

    def reproduce(self, popDensity):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the SimplePatient and
        Patient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.

        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """

        reproduce_prob = random.random()
        if reproduce_prob < (self.maxBirthProb * (1 - popDensity)):
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        else:
            raise NoChildException


class SimplePatient(object):

    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """

    def __init__(self, viruses, maxPop):

        """

        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the  maximum virus population for this patient (an integer)
        """

        self.viruses = viruses
        self.maxPop = maxPop

    def getTotalPop(self):

        """
        Gets the current total virus population.
        returns: The total virus population (an integer)
        """

        return len(self.viruses)

    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """
        repr_virus = []
        current_viruses = self.viruses[:]
        for virus in current_viruses:
            if virus.doesClear():
                current_viruses.remove(virus)
        current_pop = len(current_viruses)
        for virus in current_viruses:
            try:
                repr_virus.append(virus.reproduce(float(current_pop) / self.maxPop))
            except NoChildException:
                continue
        current_viruses.extend(repr_virus)
        self.viruses = current_viruses[:]
        #print len(self.viruses)
        return len(self.viruses)


#
# PROBLEM 2
#
def simulationWithoutDrug():

    """
    Run the simulation and plot the graph for problem 2 (no drugs are used,
    viruses do not have any drug resistance).    
    Instantiates a patient, runs a simulation for 300 timesteps, and plots the
    total virus population as a function of time.    
    """
    number_of_iteration = 100
    virus_avg_density = [0 for x in range(300)]
    for x in range(number_of_iteration):
        maxBirthProb = 0.1
        clearProb = 0.05
        maxPop = 1000
        viruses = []
        time_step = []
        for i in range(1, 100):
            viruses.append(SimpleVirus(maxBirthProb, clearProb))
        patient = SimplePatient(viruses, maxPop)
        virus_density = []
        for i in range(300):
            virus_density.append(patient.update())
        # print virus_avg_density
        # print virus_density
        virus_avg_density = [(x + y) for (x, y) in zip(virus_density, virus_avg_density)]
    # print virus_avg_density
    virus_avg_density = [(x / float(number_of_iteration)) for x in virus_avg_density]
    # print virus_avg_density

    pylab.figure("Simulation without drug")
    pylab.title("Total virus population as a function of time")
    pylab.xlabel("Time Steps")
    pylab.ylabel("Virus Population Density")
    pylab.plot(range(len(virus_avg_density)), virus_avg_density, label="Virus Population Density")
    pylab.ylim(0, 800)
    pylab.legend(loc='best')
    pylab.show()

simulationWithoutDrug()
