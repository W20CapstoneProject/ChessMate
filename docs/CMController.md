# CMController
Python 3.6.5 (https://www.python.org/downloads/release/python-365/)

CMController was created for use with our own custom Merlin (Not Marlin) firmware for control of the 3D BCN Moveo Arm. 
It enables serial communication with Merlin to send instructions based on cartesian coordinates or simple steps assigned to each stepper. 

The list of available serial instructions are:
base (76)
shoulder (7)
elbow (-120)
wrist (23)
grip (1)
move (76, 7, -120, 23, 1)

The number within the brackets is the desired steps for each motor. The move instruction will send the steps to the steppers in the following sequence: Base, Shoulder, Elbow, Wrist, Grip.

Grip will only take in a 1 or 0 indicating open or closed respectively.

The CMController is also used by the ChessMate program for it's integration with Merlin. ChessMate has access to the following three commands:
1. start() - Used to connect Merlin via serial commuication.
2. execute_move() - Use to execute a given chess move. Sends step instructions to Merlin for execution. 
3. end() - Close connection to Merlin and destruct properly.

This combination of commands allows ChessMate to play a game of chess with the 3D Moveo Arm.

### Getting Started:
1. Clone our repo
2. Go to ChessMa†e/CMController. This directory contains the setup.py file for package initalization.
3. Enter the following command to install the CMController package. Note: this will install the package in "editable" mode.
See more at (https://docs.pytest.org/en/latest/goodpractices.html) for why this method was chosen.
```
pip install -e .
```
The CMController will now be installed on can be used with other modules throughout the project.


### Creating the Virtual Environement
For this project I have used Virtualenv (https://virtualenv.pypa.io/en/latest/) to manage the package dependencies. Please refer 
to the documentation on creating a virtual environment (https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

Once your virtual environment is created and activated the dependencies for the project can be downloaded using the following command in the root directory containing requirments.txt:
```
pip install -r requirements.txt
```

### Command Line Interface
CMController comes with a simple CLI for sending instructions directly to Merlin via terminal or monitor. Run cli.py to begin sending instructions to Merlin.

