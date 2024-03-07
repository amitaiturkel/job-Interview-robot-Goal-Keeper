# GoalKeeper Robot README

## Dependencies
- **math**: Provides mathematical functions.
- **threading**: Supports multithreading capabilities.
- **numpy (as np)**: Used for numerical operations and array manipulation.

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/amitaiturkel/CyberArkInterview-robot.git
   cd CyberArkInterview-robot
   # Install Dependencies using Poetry
   poetry install
   # Activate Virtual Environment
   poetry shell
   # Run the Robot
   python -c "from goalKeeper import GoalKeeper; GoalKeeper().run()"


## Assumptions
1. **Constant Step Size**: The robot uses a constant step size for forward movement.
2. **Linear Ball Trajectory**: The algorithm assumes that the trajectory of the ball is linear, allowing it to estimate the y-coordinate based on historical positions.
3. **Laser Precision**: The laser is assumed to provide precise distance measurements, and its activation is instantaneous.
4. **Facing Degree Precision**: The robot is expected to have high precision in adjusting its facing degree.
5. **Epsilon Threshold**: The `epsilon_degree` parameter is introduced as a threshold for identifying objects, specifically to determine if an object is a ball. This assumption allows for flexibility in adjusting the classification criteria.
6. **Optimization Capability**: The code assumes that certain parameters, such as `FACE_MOVEMENT` and `epsilon_degree`, can be optimized based on the capabilities and characteristics of the robot.
7. **Ideal Game Environment**: The code assumes an idealized game environment where the robot can move freely without obstacles.
8. **Game Manager Responsibilities**: Certain responsibilities, such as laser activation, rotation timing, and overall game management, are assumed to be handled by a separate entity referred to as the "robot manager" or "game manager."

## Usage
1. **Training the Model with Hyperparameters**:
   - Hyperparameters include the number of dots to follow for the linear function(or nn.Linear), step size, angle step size, and search angles.
   - These hyperparameters can be adjusted for optimal performance.

2. **Starting the Robot**:
   - Use `GoalKeeper.run()` to start the robot.

## Methods
### Movement Methods
1. **move_right()**: Move the robot to the right by a predefined step size.
2. **move_left()**: Move the robot to the left by a predefined step size.
3. **move_forward()**: Move the robot forward by a predefined step size.
4. **move_backward()**: Move the robot backward by a predefined step size.

### Rotation Methods
1. **rotate_clock_wise()**: Rotate the robot in a clockwise direction by a predefined face movement angle.
2. **rotate_unclock_wise()**: Rotate the robot in a counterclockwise direction by a predefined face movement angle.
3. **rotate_to_angle(angle)**: Rotate the robot to a specified angle.

### Laser and Object Detection Methods
1. **activate_laser()**: Activate the robot's laser sensor.
2. **get_laser_position()**: Get the position of an object detected by the robot's laser.
3. **identify()**: Identify an object detected by the robot's laser.
4. **encountered_a_ball()**: Check if the robot has encountered an object resembling a ball using laser measurements.

### Navigation and Strategy Methods
1. **go_to_location(target_x, target_y)**: Move the robot to a specified target location using a combination of rotation and forward movement.
2. **prevent_attack()**: Prevent potential attacks by strategically positioning the robot and performing effective searches.
   - Returns the estimated y-coordinate of the ball if a potential goal-scoring trajectory is detected, otherwise returns None.
3. **will_enter_goal(y_point)**: Check if the provided y-coordinate is within the goal-scoring range.
4. **estimate_ball_location()**: Estimate the current y-coordinate of the ball's position based on historical positions.

### Teammate Communication Methods
1. **handle_teammate_messages()**: Continuously listen for teammate messages using the Transceiver and process them.
2. **process_teammate_message(message)**: Process a message received from a teammate and take appropriate actions.

### Game Management Method
1. **run()**: Execute the main logic of the robot, including setup and continuous execution until the game is over.

## How to Use
1. **Import the GoalKeeper class**.
2. **Instantiate an object** of the GoalKeeper class, providing the team ID.
3. **Call the `run()` method** to start the robot's main logic.

## Notes
- The code includes various assumptions and parameters that can be adjusted based on the specific characteristics of the robot and the game environment.
- The README provides an overview of the key methods and their functionalities.
- Further adjustments and optimizations can be made based on experimental observations and the robot's performance in the actual game environment.
