# Problem Set 6: Simulating robots
# Name:
# Collaborators:
# Time:

import math
import random

import ps6_visualize
import pylab

# === Provided classes


class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

# === Problems 1


class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        self.clean_tiles = []

    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        x = abs(int(pos.getX()))
        y = abs(int(pos.getY()))
        if not (x, y) in self.clean_tiles:
            self.clean_tiles.append((x, y))

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        return (m, n) in self.clean_tiles

    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width * self.height

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return len(self.clean_tiles)

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        randX = random.randint(0, self.width - 1)
        randY = random.randint(0, self.height - 1)
        return Position(randX, randY)

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        x = pos.getX()
        y = pos.getY()
        x_within_limit = x < self.width and x >= 0
        y_within_limit = y < self.height and y >= 0
        return x_within_limit and y_within_limit


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        self.position = room.getRandomPosition()
        self.direction = random.randint(0, 360 - 1)
        self.previous_position = self.position

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position

    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction

    def isPositionEqualToRobotPreviousPosition(self, position):
        previous_x = self.previous_position.getX()
        previous_y = self.previous_position.getY()
        x = abs(round(position.getX()))
        y = abs(round(position.getY()))
        return previous_x == x and previous_y == y

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.previous_position = self.position
        self.position = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        position = self.position.getNewPosition(self.direction, self.speed)
        found_good_position = False
        retry_count = 0
        while(not found_good_position):
            position_in_room = self.room.isPositionInRoom(position)
            if(position_in_room):
                if(not self.isPositionEqualToRobotPreviousPosition(position)):
                    retry_count += 1
                    if((not self.room.isTileCleaned(position.getX(), position.getY())) or retry_count > 4):
                        found_good_position = True
                        break
            self.direction = random.randint(0, 360 - 1)
            position = self.position.getNewPosition(self.direction, self.speed)
        self.setRobotPosition(position)
        self.room.cleanTileAtPosition(self.position)


# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current direction; when
    it hits a wall, it chooses a new direction randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        position = self.position.getNewPosition(self.direction, self.speed)
        found_good_position = False
        while(not found_good_position):
            position_in_room = self.room.isPositionInRoom(position)
            if(position_in_room):
                if(not self.isPositionEqualToRobotPreviousPosition(position)):
                    found_good_position = True
                    break
            self.direction = random.randint(0, 360 - 1)
            position = self.position.getNewPosition(self.direction, self.speed)
        self.setRobotPosition(position)
        self.room.cleanTileAtPosition(self.position)

# === Problem 3


def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    """
    trial_timespan = []
    for i in range(num_trials):
        # print "trial ", i
        robots = []
        timespan = 0
        # anim = ps6_visualize.RobotVisualization(num_robots, width, height, 0.8)
        room = RectangularRoom(width, height)
        for i in range(0, num_robots):
            robots.append(robot_type(room, speed))
        current_coverage = float(room.getNumCleanedTiles()) / room.getNumTiles()
        while(current_coverage < min_coverage):
            for robot in robots:
                robot.updatePositionAndClean()
                current_coverage = float(room.getNumCleanedTiles()) / room.getNumTiles()
                # print "current coverage is ", current_coverage
            timespan += 1
            # anim.update(room, robots)
        # anim.done()
        # Room has been cleaned to minimum coverage
        trial_timespan.append(timespan)
    # All trials completed, calculate the mean time span
    mean_timespan = sum(trial_timespan) / len(trial_timespan)
    print mean_timespan
    return mean_timespan

# print "1 robot to completely clean 5 X 5 room"
# runSimulation(1, 1, 5, 5, 1, 30, StandardRobot)
# print "1 robot to clean 75%  of a 10 X 10 room"
# runSimulation(1, 1, 10, 10, 0.75, 30, StandardRobot)
# print "3 robot to clean 90% of 10 X 10 room"
# runSimulation(3, 1, 10, 10, 0.9, 1, StandardRobot)
# print "1 robot to completely clean 20 X 20 room"
# runSimulation(1, 1, 20, 20, 1, 30, StandardRobot)
# === Problem 4
#
# 1) How long does it take to clean 80% of a 20X20 room with each of 1-10 robots?
#
# 2) How long does it take two robots to clean 80% of rooms with dimensions 
#	 20X20, 25X16, 40X10, 50X8, 80X5, and 100X4?

# === Problem 5


class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random after each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        self.direction = random.randint(0, 360 - 1)
        position = self.position.getNewPosition(self.direction, self.speed)
        found_good_position = False
        while(not found_good_position):
            position_in_room = self.room.isPositionInRoom(position)
            if(position_in_room):
                if(not self.isPositionEqualToRobotPreviousPosition(position)):
                    found_good_position = True
                    break
            self.direction = random.randint(0, 360 - 1)
            position = self.position.getNewPosition(self.direction, self.speed)
        self.setRobotPosition(position)
        self.room.cleanTileAtPosition(self.position)


def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """ 
    mean_time = []
    for robot in range(1, 11):
        mean_time.append(runSimulation(robot, 1, 20, 20, 0.8, 100, StandardRobot))

    pylab.figure("a plot showing dependence of cleaning time on number of robots")
    pylab.title("a plot showing dependence of cleaning time on number of robots")
    pylab.xlabel("Number of robots")
    pylab.ylabel("Time Steps taken to clean 80% of a 20 X 20 room")
    pylab.plot(range(1, 11), mean_time)
    pylab.show()
# showPlot1()


def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    mean_time = []
    mean_time.append(runSimulation(2, 1, 20, 20, 0.8, 30, StandardRobot))
    mean_time.append(runSimulation(2, 1, 25, 16, 0.8, 30, StandardRobot))
    mean_time.append(runSimulation(2, 1, 40, 10, 0.8, 30, StandardRobot))
    mean_time.append(runSimulation(2, 1, 50, 8, 0.8, 30, StandardRobot))
    mean_time.append(runSimulation(2, 1, 80, 5, 0.8, 30, StandardRobot))
    mean_time.append(runSimulation(2, 1, 100, 4, 0.8, 30, StandardRobot))

    pylab.figure("a plot showing dependence of cleaning time on room shape")
    pylab.title("Used 2 robots clean 80% of the room")
    pylab.xlabel("Ratio of width to height")
    pylab.ylabel("Time Steps taken")
    pylab.plot([20.0/20, 25.0/16, 40.0/10, 50.0/8, 80.0/5, 100.0/4], mean_time)
    pylab.show()

# showPlot2()

# === Problem 6

# For the parameters tested below (cleaning 80% of a 20x20 square room),
# RandomWalkRobots take approximately twice as long to clean the same room as
# StandardRobots do.


def showPlot3():
    """
    Produces a plot comparing the two robot strategies.
    """
    styles = ['b-', 'b-.']
    mean_time_standard = []
    mean_time_random = []
    for i in range(11):
        mean_time_standard.append(runSimulation(1, 1, 20, 20, 0.8, 30, StandardRobot))
    for i in range(11):
        mean_time_random.append(runSimulation(1, 1, 20, 20, 0.8, 30, RandomWalkRobot))


    pylab.figure("StandardRobot vs RandomWalkRobot")
    pylab.title("Time taken by StandardRobot vs RandomWalkRobot")
    pylab.xlabel("Trial Number")
    pylab.ylabel("Time Steps taken")
    pylab.plot(mean_time_standard, styles[0], label="StandardRobot")
    pylab.plot(mean_time_random, styles[1], label="RandomWalkRobot")
    pylab.ylim(0, max(mean_time_random))
    pylab.legend(loc='best')
    pylab.show()

showPlot3()
