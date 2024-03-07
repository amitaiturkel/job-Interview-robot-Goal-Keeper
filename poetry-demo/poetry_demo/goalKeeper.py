# Dependencies:
# - math: Provides mathematical functions.
# - threading: Supports multithreading capabilities.
# - numpy (as np): Used for numerical operations and array manipulation.
import math
import threading

import numpy as np

# Assumptions:
# Constant Step Size:
# The robot uses a constant step size for forward movement.

# Linear Ball Trajectory:
# The algorithm assumes that the trajectory of the ball is linear, allowing it to estimate the y-coordinate based on historical positions.

# Laser Precision:
# The laser is assumed to provide precise distance measurements, and its activation is instantaneous.

# Facing Degree Precision:
# The robot is expected to have a high precision in adjusting its facing degree.

# Epsilon Threshold:
# The epsilon_degree parameter is introduced as a threshold for identifying objects, specifically to determine if an object is a ball.
# This assumption allows for flexibility in adjusting the classification criteria.

# Optimization Capability:
# The code assumes that certain parameters, such as FACE_MOVEMENT and epsilon_degree, can be optimized based on the capabilities and characteristics of the robot.

# Ideal Game Environment:
# The code assumes an idealized game environment where the robot can move freely without obstacles.

# Game Manager Responsibilities:
# Certain responsibilities, such as laser activation, rotation timing, and overall game management,
# are assumed to be handled by a separate entity referred to as the "robot manager" or "game manager."


# TODO train our model with hyperparamters: the number of dots we follow to make the liner function,the step size,
# the angel step size,the search angels


# use GoalKeeper.run() to start the robort

# example so my compiler won't yell on me
ROBOT_RADIUS = 3
BALL_RADIUS = 2
FIELD_LENGTH = 30
FIELD_WIDTH = 10
GOAL_WIDTH = 5
GOAL_DEPTH = 2
EPSILON = 1e10
FACE_MOVEMENT = 2


class GoalKeeper:
    def __init__(self):
        self.robot_radius = ROBOT_RADIUS
        self.ball_radius = BALL_RADIUS
        self.field_length = FIELD_LENGTH
        self.field_width = FIELD_WIDTH
        self.goal_width = GOAL_WIDTH
        self.goal_depth = GOAL_DEPTH
        self.location = (self.goal_depth + self.robot_radius, self.field_length / 2)  # assuming we start at the middle of the goal
        # and that (0,0) is up right corner
        self.facing_degree = 0  # faceing the enemey goal
        self.step_size = self.robot_radius / 2
        self.message_check_thread = threading.Thread(target=self.check_teammate_messages)
        self.message_check_thread.daemon = True
        self.message_check_thread.start()
        self.last_seen = []
        self.search_dirction = 1
        self.epsilon_degree = EPSILON
        self.team_mate_position = (-1, -1)  # Initialized as out of board so won't interrupt
        # in goal detection before coordinates are sent

    def move_right(self):
        """
        Move the robot to the right by a predefined step size.

        Returns:
            None

        Explanation:
        - Calculates the new position based on the direction '1', representing moving to the right.
        - Checks if the new position is within the field limits using `is_within_field_limits`.
        - Updates the robot's location if the new position is within limits.
        """
        new_x, new_y = self.calculate_new_position(90)  # 90 represents moving right by a single step
        if self.is_within_field_limits(new_x, new_y):
            self.location = (new_x, new_y)

    def move_left(self):
        """
        Move the robot to the left by a predefined step size.

        Returns:
            None

        Explanation:
        - Calculates the new position based on the direction '-1', representing moving to the left.
        - Checks if the new position is within the field limits using `is_within_field_limits`.
        - Updates the robot's location if the new position is within limits.
        """
        new_x, new_y = self.calculate_new_position(-90)  # -1 represents moving left by a single step

        # Check if the new position is within the field limits
        if self.is_within_field_limits(new_x, new_y):
            # Update the location if within limits
            self.location = (new_x, new_y)

    def move_forward(self):
        """
        Move the robot to the forward by a predefined step size.

        Returns:
            None

        Explanation:
        - Calculates the new position based on the direction '0', representing moving to the left.
        - Checks if the new position is within the field limits using `is_within_field_limits`.
        - Updates the robot's location if the new position is within limits.
        """
        # Calculate the new position after moving forward
        new_x, new_y = self.calculate_new_position(0)  # 0 represents moving forward by a single step

        # Check if the new position is within the field limits
        if self.is_within_field_limits(new_x, new_y):
            # Update the location if within limits
            self.location = (new_x, new_y)

    def move_backward(self):
        """
        Move the robot to the backward by a predefined step size.

        Returns:
            None

        Explanation:
        - Calculates the new position based on the direction '180', representing moving to the left.
        - Checks if the new position is within the field limits using `is_within_field_limits`.
        - Updates the robot's location if the new position is within limits.
        """
        new_x, new_y = self.calculate_new_position(180)  # 180 represents moving backward by a single step

        if self.is_within_field_limits(new_x, new_y):  # Check if the new position is within the field limits
            # Update the location if within limits
            self.location = (new_x, new_y)

    def calculate_new_position(self, direction):
        """
        Calculate the new position of the robot based on the given direction.

        Parameters:
        - direction (int): The direction in degrees. 0 represents moving forward,
                            180 represents moving backward, and 1/-1 represent
                            moving right/left, respectively.

        Returns:
        tuple: A tuple containing the new x and y coordinates of the robot.

        Explanation:
        - The method uses the current facing degree of the robot and the specified
            direction to calculate the new position.
        - If the direction is 0, it calculates the movement based on the current
            facing degree.
        - If the direction is 180, it calculates the movement in the opposite direction.
        - For other directions (90/-90), it calculates lateral movement.

        Math Explanation:
        - The method uses trigonometric functions (cosine and sine) to calculate
            the delta x and delta y based on the step size and the angle.
        - The new x and y coordinates are then calculated by adding the delta x and
            delta y to the current location.

        Assumptions: the rotate is by degrees

        """

        radian_angle = math.radians(self.facing_degree + direction)

        # We want to move self.step_size with direction degrees, so to update the coordinates we draw a triangle,
        # with the hypotenuse being the movement we want to do (size=self.step_size) and the degree between the
        # hypotenuse and the adjacent is direction,in order to get the size of the opposite we calculate
        # step_size * cos(direction) and in order to get the adjacent we calculate step_size * sin(direction).

        delta_x = self.step_size * math.cos(radian_angle)
        delta_y = self.step_size * math.sin(radian_angle)

        new_x = self.location[0] + delta_x
        new_y = self.location[1] + delta_y

        return new_x, new_y

    def is_within_field_limits(self, x, y):
        # Check if the new position is within the field limits
        return 0 <= x <= self.field_width and 0 <= y <= self.field_length

    def rotate_clockwise(self):
        """
        Rotate the robot in a clockwise direction by a predefined face movement angle.

        Returns:
            None

        Explanation:
        - Updates the facing degree by subtracting the predefined face movement angle.
        - Performs a safety check by ensuring the facing degree is within the range [0, 360).
        Assumptions:
        - The `FACE_MOVEMENT` value can be optimized based on the capabilities of the robot.
        The optimal value should take into account the robot's agility and responsiveness to changes in facing direction.
        Adjustments to `FACE_MOVEMENT` can be made experimentally to find the most efficient rotation speed.
        """
        self.facing_degree = (self.facing_degree - FACE_MOVEMENT) % 360

    def rotate_counter_clockwise(self):
        """
        Rotate the robot in a counterclockwise direction by a predefined face movement angle.

        Returns:
            None

        Assumptions:
        - The `FACE_MOVEMENT` value can be optimized based on the capabilities of the robot.
        The optimal value should take into account the robot's agility and responsiveness to changes in facing direction.
        Adjustments to `FACE_MOVEMENT` can be made experimentally to find the most efficient rotation speed.

        Explanation:
        - Updates the facing degree by adding the predefined face movement angle.
        - Performs a safety check by ensuring the facing degree is within the range [0, 360).
        The modulus operation is applied, although not strictly necessary for safety.
        """
        self.facing_degree = (self.facing_degree + FACE_MOVEMENT) % 360

    def activate_laser(self):
        pass

    def get_laser_poisiton(self):
        """
        Get the position of an object detected by the robot's laser.

        Returns:
        tuple: A tuple containing the x and y coordinates of the detected object.

        Explanation:
        - The method first activates the robot's laser sensor to measure the distance
        to the detected object.
        - It then calculates the x and y coordinates of the object based on the
        measured distance and the current facing degree of the robot.
        - The trigonometric functions (cosine and sine) are used to determine the
        object's position relative to the robot.

        """
        distance = self.activate_laser()
        radian_angle = math.radians(self.facing_degree)
        object_x = self.location[0] + distance * math.cos(radian_angle)
        object_y = self.location[1] + distance * math.sin(radian_angle)
        return object_x, object_y

    def idenifiy(self):
        """
        Identify an object detected by the robot's laser.

        Returns:
        tuple: A tuple containing the identification code, x, and y coordinates of the detected object.

        Explanation:
        - The method retrieves the position of the detected object using the
        `get_laser_poisiton` method.
        - It then checks if the object is at the boundaries of the field, indicating
        that the laser hasn't seen anything.
        - It compares the detected object's position with the latests teammate's position
        to determine if the laser saw a teammate.
        - If the object is not at the field boundaries and is not the teammate,
        it is identified as a ball or player from the other team.
        """
        object_x, object_y = self.get_laser_poisiton()

        # Check if the object is at the boundaries of the field
        if object_x == 0 or object_x == self.field_length or object_y == 0 or object_y == self.field_width:
            return 0, object_x, object_y  # The laser hasn't seen anything

        # Check if the object is a teammate
        if object_x == self.team_mate_position[0] and object_y == self.team_mate_position[1]:
            return 0, object_x, object_y  # The laser saw the teammate
        else:
            return 1, object_x, object_y  # The laser saw a ball or player from the other team

    def rotate_to_angle(self, angle):
        """
        Rotate the robot to a specified angle.

        Args:
            angle (float): The target angle in degrees.

        Returns:
            None
         Assumptions:
        - The robot is designed to support significant changes in angle, and not small steps.
        - The function ensures that the angle is within the range [0, 360) by adjusting it if necessary.
        - The adjusted angle is assigned to the robot's `self.facing_degree` attribute.
        """

        self.facing_degree = angle % 360

    def go_to_location(self, target_x, target_y):
        """
        Move the robot to a specified target location using a combination of rotation and forward movement.

        Args:
            target_x (float): The x-coordinate of the target location.
            target_y (float): The y-coordinate of the target location.

        Returns:
            None

        Assumptions:
        - The robot uses a constant step size for forward movement.
        - The game maneger will translate those constant step as steps and not as one big jump

         Explanation:
        - Delta X and Delta Y Calculation:
          - `delta_x`: The difference between the target's x-coordinate and the robot's current x-coordinate.
          - `delta_y`: The difference between the target's y-coordinate and the robot's current y-coordinate.

        - Angle Calculation using Arctangent (atan2):
        - The arctangent of the quotient of `delta_y` and `delta_x` is calculated using `math.atan2`.
            The `atan2` function avoids division by zero errors and provides the correct angle in all quadrants.
        - In mathematical terms, `atan2(delta_y, delta_x)` returns the angle whose tangent is the quotient
            `delta_y / delta_x`, taking into account the signs of both arguments to determine the correct quadrant.

        - Adjustment for Target Angle:
          - The calculated angle to the target is adjusted by adding 360 and taking the modulus with 360.
            This ensures the angle is in the range [0, 360).

        - Movement to Target:
          - The robot rotates to the calculated angle using `rotate_to_angle`.
          - The robot moves forward by a constant step size until it reaches the target location
        """
        # Calculate the angle to the target location
        delta_x = target_x - self.location[0]
        delta_y = target_y - self.location[1]
        target_angle = (math.degrees(math.atan2(delta_y, delta_x)) + 360) % 360

        distance_to_target = math.sqrt(delta_x**2 + delta_y**2)

        self.rotate_to_angle(target_angle)

        while distance_to_target > 0:
            # Move the robot forward by the constant step size
            self.move_forward()

            # Update the remaining distance
            distance_to_target -= self.step_size

    def Transceiver(self):
        pass

    def handle_teammate_messages(self):
        """
        Continuously listens for teammate messages using the Transceiver and processes them.
        """
        while True:
            message = self.Transceiver()
            if message:
                self.process_teammate_message(message)

    def process_teammate_message(self, message):
        """
        Process a message received from a teammate and take appropriate actions.

        Args:
            message (str): The message received from the teammate.

        Returns:
            None

        Explanation:
        - If the message is "Go to base," the robot moves to a predefined base location.
        - If the message indicates the location of the ball at the right or left corner, the robot moves to the respective corner.
        - If the message is "you are looking in the wrong direction," the robot adjusts its search direction.
        - If the message starts with "position:", the robot extracts coordinates and updates information about the teammate.

        Assumptions:
        - The format of the message is predefined for accurate processing.
        - The extracted coordinates are expected to be in the format "x,y." """
        if message == "Go to base":
            self.go_to_location(self.goal_depth + self.robot_radius, self.field_length / 2)
            # Logic explanation: The robot aligns itself with the center of the field and moves forward.

        elif message == "ball at the right corner":
            # Move the robot to a position near the right corner based on predefined coordinates
            self.go_to_location(self.goal_width + self.robot_radius, (self.field_length + self.goal_width) / 2)
            # Logic explanation: The robot aligns itself with the right corner when
            # (self.field_length + self.goal_width)/2 is the lower end of football gate.

        elif message == "ball at the left corner":
            # Logic explanation: The robot aligns itself with the left corner and moves forward,
            # (self.field_length - self.goal_width)/2 is the upper end of football gate.
            self.go_to_location(self.goal_width + self.robot_radius, (self.field_length - self.goal_width) / 2)

        elif message.startswith("position: "):
            # Extract coordinates from the message
            coordinates_str = message[len("position: ") :]
            try:
                # Convert extracted coordinates to integers
                x, y = map(int, coordinates_str.split(","))
                self.team_mate_position = (x, y)

            except ValueError:
                print("Invalid position format in the message.")

    def prevent_attack(self):
        """
        Prevent potential attacks by strategically positioning the robot and performing effective searches.

        Returns:
            float: If a potential goal-scoring trajectory is detected, returns the estimated y-coordinate
                of the ball. Otherwise, returns None.

        Explanation:
        - Initialize the flag to indicate whether the target location has been reached.
        - Ensure the robot is facing the correct direction for effective searching.
        - Check if the robot is not already at a strategic position.
        - Move the robot to a strategic position near the center of the field.

        - Implement a search until the target is found and prevented.
        - Identify objects using the laser.
        - When the robot encounters an object identified as a ball, append the coordinates to the list `last_seen`.
            Logic explanation: When the robot encounters an object identified as a ball,
            it appends the coordinates of the object to the list `last_seen`.
            This is done to track the trajectory of the ball based on the historical positions.
        - If there are not enough historical positions, continue searching.
        - If enough historical positions are available, estimate the y-coordinate of the ball's current position.
        - If the trajectory indicates the ball will enter the goal, return the estimated y-coordinate.
        """
        not_found = True
        self.rotate_to_angle(90)
        self.search_direction = 1

        if (self.goal_depth + self.robot_radius, self.field_length / 2) != self.location:
            self.go_to_location(self.goal_depth + self.robot_radius, self.field_length / 2)

        while not_found:
            if self.facing_degree < 270 and self.facing_degree > 90:
                self.rotate_to_angle(90)

            idenifiy = self.idenifiy()

            if idenifiy[0] == 0:
                if self.search_direction:  # Change direction if the teammate instructs
                    self.rotate_clockwise()
                else:
                    self.rotate_counter_clockwise()

            else:
                if self.encountered_a_ball():
                    self.last_seen.append((idenifiy[1], idenifiy[2]))  # Object identified coordinates

                    if len(self.last_seen) < 2:
                        continue
                    if len(self.last_seen) == 2 and self.last_seen[1][0] - self.last_seen[0][0] > 0:  # ball going in enemey
                        # gate dirctions
                        continue
                    else:
                        y_estimation = self.estimate_ball_location()
                        if self.will_enter_goal(y_estimation):
                            return y_estimation
        return None

    def will_enter_goal(self, y_point):
        """
        Check if the provided y-coordinate is within the goal-scoring range.

        Args:
            y_point (float): The y-coordinate to be checked.

        Returns:
            bool: True if the y-coordinate indicates the ball will enter the goal, False otherwise.
        """
        return ((self.field_length - self.goal_width) / 2) <= y_point <= ((self.field_length + self.goal_width) / 2)

    def estimate_ball_location(self):
        """
        Estimate the current y-coordinate of the ball's position based on historical positions.

        Returns:
            float: The estimated y-coordinate of the ball.

        Explanation:
        - Create arrays of x and y coordinates from the two most recent historical positions.
        - Delete the first historical position, as it is no longer needed.
        - Fit a linear function (degree 1) to the remaining historical positions using polyfit.
        - Update the first historical position with the last one, and remove the last one from the list.
        - Calculate the estimated y-coordinate using the fitted linear function.

        Note:
        our estimate_ball_location is blind to diractions, its sees only linear function but we dirction in the function
        """
        x_values = np.array([self.last_seen[0][0], self.last_seen[1][0]])
        y_values = np.array([self.last_seen[0][1], self.last_seen[1][1]])

        # Delete the first item as it is no longer needed
        self.last_seen[0] = self.last_seen[-1]
        self.last_seen.pop()

        # Fit a linear function (degree 1) using polyfit
        coefficients = np.polyfit(x_values, y_values, 1)
        slope, intercept = coefficients

        # Calculate and return the estimated y-coordinate
        return self.last_seen[0][0] * slope + intercept

    def encountered_a_ball(self):
        """
        Check if the robot has encountered an object resembling a ball using laser measurements.

        Returns:
            bool: True if a potential ball is detected, False otherwise.

        Explanation:
        - Obtain the length of the side adjacent to the ball (distance to the detected object) using the laser.
        - Set the length of the side opposite to the ball as the predefined robort radius.
        - Calculate the angle (degree) using the arctangent of the quotient of side_opposite and side_adjacent.
        - Temporarily adjust the robot's facing degree to one side within the epsilon threshold for checking.
        - Identify objects using the laser in the adjusted direction.
        - If an object is found, return False because we found a robort.
        - Reset the robot's facing degree to its original direction.
        - Adjust the robot's facing degree to the other side within the epsilon threshold for checking.
        - Identify objects using the laser in the adjusted direction.
        - If an object is found, return True.
        - Reset the robot's facing degree to its original direction.
        - If no potential Robort is detected on either side,the target is a ball return True.

        Note:
        The epsilon_degree is a threshold used to check if an object is a ball based on laser measurements.
        - In dynamic environments where the ball may be moving or to optimize the robot's classification sensitivity,
        epsilon_degree allows for a margin of error in the facing direction during the ball detection process.
        This flexibility ensures that the robot can effectively identify balls even with slight variations in facing direction.
        The optimal value for epsilon_degree may be adjusted based on the specific characteristics of the robot's sensors
        and the dynamic nature of the environment.
        """
        # Obtain laser measurements for calculations
        side_adjacent = self.activate_laser()
        side_opposite = self.robot_radius

        # Calculate the angle using arctangent
        degree = math.degrees(math.atan(side_opposite / side_adjacent))

        # Temporarily adjust the robot's facing degree to one side within the epsilon threshold for checking
        temp_degree = self.facing_degree
        self.facing_degree = self.facing_degree + degree - self.epsilon_degree

        # Identify objects using the laser in the adjusted direction
        found = self.idenifiy()
        if found[0] != 0:
            return False

        # Reset the robot's facing degree to its original direction
        self.facing_degree = temp_degree

        # Adjust the robot's facing degree to the other side within the epsilon threshold for checking
        self.facing_degree = self.facing_degree - (degree - self.epsilon_degree)

        # Identify objects using the laser in the adjusted direction
        found = self.idenifiy()
        if found[0] != 0:
            return False

        # Reset the robot's facing degree to its original direction
        self.facing_degree = temp_degree

        # If no potential robort is detected on either side,the target is smaller, its a ball return True
        return True

    def run(self):
        # do all the set up for the first step of the game
        while not self.game_over():
            ball_y = self.prevent_attack()
            self.go_to_location(self.goal_depth + self.robot_radius, ball_y)
            # Logic explanation: The target x-coordinate is consistently set to `self.goal_depth + self.robot_radius`.
            # Placing the robot at this x-coordinate aligns it with the goalpost's edge, offering optimal coverage
            # to block potential goal-scoring trajectories from the opponent.
