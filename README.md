# Ackermann Steering 

A very simple ackermann steering model in pygame.

## Install

`
pip3 install -r requirements
`

## Usage
`python3 src/main.py`

Use :arrow_up: and :arrow_down: keyboard keys to accelerate and break, while :arrow_left: and :arrow_right: are used to steer the vehicle.

The ackermann steering model doesn't follow "conventional" arcade game movement, it works by gradually changing the steering front wheels angle in a two axle vehicle, as to better represent a 4-wheeled vehicle.

You can read more about it [here](https://www.xarg.org/book/kinematics/ackerman-steering/).