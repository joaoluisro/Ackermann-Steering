import pygame
import math
pygame.init()

MIN_VEHICLE_LENGTH = 1.0
MIN_VEHICLE_AXLE_WIDTH = 1.0
RIGHT_ARROW = pygame.K_RIGHT
LEFT_ARROW = pygame.K_LEFT 
UP_ARROW = pygame.K_UP 
DOWN_ARROW = pygame.K_DOWN
MAX_SIZE = 50
WIDTH_RESOLUTION = 16
HEIGHT_RESOLUTION = 9

class VehicleState():
  
  x: float
  y: float
  heading: float
  steering_angle: float

  def __init__(self, 
                x0, 
                y0):
    self.x = x0
    self.y = y0
    self.heading = 0.0
    self.steering_angle = 0.0

  def update_state(self, 
                    velocity, 
                    acceleration, 
                    steering_angle,
                    time_step,
                    vehicle_length):
                    
    self.steering_angle = steering_angle
    self.heading += ((velocity/vehicle_length) * math.tan(math.radians(steering_angle)))
    self.x += (velocity * math.cos(math.radians(self.heading))) * time_step
    self.y += (velocity * math.sin(math.radians(self.heading))) * time_step

  def position(self):
    return [self.x, self.y]

  def print_state(self):
    print('At ({},{}) with heading {} and steering angle {}'.format(self.x, self.y, self.heading, self.steering_angle))

# acceleration/velocity/steering -> state
class Vehicle():

  velocity : float
  acceleration : float
  axle_width : float
  vehicle_length : float
  steering_angle : float
  max_steering_angle : float 
  acceleration_step: float
  time_step : float

  def __init__(self, 
                x0, 
                y0, 
                axle_width = 1.5, 
                vehicle_length = 4.0,
                max_steering_angle = 30.0,
                max_velocity = 15.0,
                acceleration_step = 0.1,
                time_step = 1.0/10,
                steer_step = 1.0):

    self.velocity = 0.0
    self.acceleration = 0.0
    self.steering_angle = 0.0

    if(vehicle_length < MIN_VEHICLE_LENGTH or axle_width < MIN_VEHICLE_AXLE_WIDTH):
      assert()
    
    self.axle_width = axle_width
    self.vehicle_length = vehicle_length
    self.state = VehicleState(x0, y0)
    self.max_steering_angle = max_steering_angle
    self.max_velocity = max_velocity
    self.acceleration_step = acceleration_step
    self.steer_step = steer_step
    self.time_step = time_step
    self.epilson = 0.1

  def accelerate(self, direction):
    self.acceleration += direction * self.acceleration_step * self.time_step 
    self.acceleration *= (direction != 0)

  def steer(self, direction):
    if abs(self.steering_angle + direction) <= self.max_steering_angle:
      self.steering_angle += direction * self.steer_step 
    elif abs(self.steering_angle) < self.epilson:
      self.steering_angle = 0.0

  def update_position(self):
    if(abs(self.velocity + self.acceleration) <= self.max_velocity):
      self.velocity += self.acceleration

    self.state.update_state(self.velocity, 
                            self.acceleration, 
                            self.steering_angle,
                            self.time_step,
                            self.vehicle_length)

  def convert_basis(self, position, screen_width, screen_height):
    x,y = position[0], position[1]
    return([round(screen_width - x), round(screen_height - y)])

  def render_vehicle(self, screen, screen_width, screen_height):
    self.update_position()
    self.state.print_state()
    pygame.draw.circle(screen, (0,0,0), self.convert_basis(self.state.position(), screen_width, screen_height), 10)

# events -> acceleration/velocity/steering
class UserInputParser():

  def __init__(self, vehicle):
    self.vehicle = vehicle
    self.left_pressed = False
    self.right_pressed = False 
    self.up_pressed = False
    self.down_pressed = False

  def parse_event(self):
    for event in pygame.event.get():

      arrow_state = pygame.key.get_pressed()
      self.right_pressed = arrow_state[RIGHT_ARROW]
      self.left_pressed = arrow_state[LEFT_ARROW]
      self.up_pressed = arrow_state[UP_ARROW]
      self.down_pressed = arrow_state[DOWN_ARROW]

      if(event.type == pygame.QUIT):
        return False

    if(self.up_pressed):
      self.vehicle.accelerate(1)
    elif(self.down_pressed):
      self.vehicle.accelerate(-1)
    else:
      self.vehicle.accelerate(0)

    if(self.left_pressed):
      self.vehicle.steer(-1)
    elif(self.right_pressed):
      self.vehicle.steer(1)
    else:
      angle = self.vehicle.steering_angle
      if(abs(angle) > self.vehicle.epilson):
        if(angle > 0):
          self.vehicle.steer(-1)
        else:
          self.vehicle.steer(1)
    return True

def main():
  screen_width = WIDTH_RESOLUTION * MAX_SIZE
  screen_height = HEIGHT_RESOLUTION * MAX_SIZE
  screen = pygame.display.set_mode([screen_width, screen_height])
  vehicle = Vehicle( 50, 50)
  input_parser = UserInputParser(vehicle)
  clock = pygame.time.Clock()
  while input_parser.parse_event():
    clock.tick(30)

    screen.fill((255,255,255))
    vehicle.render_vehicle(screen, screen_width, screen_height)
    
    pygame.display.flip()

main()
pygame.quit()