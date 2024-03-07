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


## Ideas for Improvement

### 1. Utilizing Neural Networks for Ball Location Estimation

#### Problem Statement:
The current implementation estimates the ball's location based on historical positions and a linear function. While effective, incorporating a neural network (NN) can enhance the robot's ability to predict the ball's trajectory in a more dynamic and complex game environment.

#### Idea:
Implement a neural network model to predict the ball's future positions based on historical data. Train the NN using machine learning techniques, considering factors such as varying game dynamics, player movements, and environmental conditions. This approach can improve the accuracy of the ball's predicted location, enabling the robot to make more informed decisions during gameplay.

#### Benefits:
1. **Dynamic Object Trajectory Prediction:** Neural networks can learn complex patterns in the ball's movement, allowing the robot to predict its trajectory even in situations with rapid changes or unexpected movements.
2. **Adaptability to Game Dynamics:** A trained NN can adapt to diverse game scenarios, accommodating variations in ball speed, player interactions, and overall gameplay dynamics.
3. **Real-time Decision Making:** The enhanced prediction capabilities empower the robot to make real-time decisions, adjusting its strategy based on the predicted ball location.

#### Steps:
1. Gather a dataset of historical ball positions, including diverse game scenarios.
2. Design a neural network architecture suitable for the prediction task.
3. Train the NN using the collected dataset, adjusting hyperparameters for optimal performance.
4. Integrate the trained NN into the robot's logic for real-time ball location estimation.

### 2. Object Recognition Enhancement with Deep Learning

#### Problem Statement:
The current object recognition mechanism relies on predefined criteria to identify whether an object detected by the laser is a ball or another player. This approach might face challenges in distinguishing between various objects with similar characteristics.

#### Idea:
Enhance the object recognition process by implementing deep learning techniques for more robust and accurate classification. Train a convolutional neural network (CNN) to recognize different objects based on laser sensor data, taking into account variations in shapes, sizes, and movement patterns.

#### Benefits:
1. **Improved Object Discrimination:** A CNN can learn intricate features of different objects, enhancing the robot's ability to distinguish between a ball, players, and other potential obstacles.
2. **Adaptable to Varied Environments:** The deep learning approach is more adaptable to changes in lighting conditions, background interference, and other environmental factors, providing reliability in diverse game environments.
3. **Handling Moving Objects:** The trained CNN can better handle moving objects, as it learns to recognize patterns associated with dynamic motion and adjusts its classification accordingly.

#### Steps:
1. Collect a diverse dataset of laser sensor readings for different objects (balls, players, obstacles).
2. Design a CNN architecture suitable for object classification.
3. Train the CNN using the labeled dataset to accurately identify objects.
4. Integrate the trained CNN into the robot's code for real-time object recognition during gameplay.

These enhancements not only improve static object recognition but also equip the robot to effectively deal with the challenges posed by moving objects during gameplay.

