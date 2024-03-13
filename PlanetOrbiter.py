import pygame
import math
import numpy as np # for finding smallest/largest list items
import random

pygame.init()

GREEN = (0, 255, 0)
G = 6.67430e-11  # gravitational constant 'G'
planet_mass = random.randint(50000000000000, 200000000000000)  # mass of planet
ship_mass = 1000 # mass of rocket

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Gravity Game")

# Load the background image
background_image = pygame.image.load("Textures/stars.jpg")
background_image = pygame.transform.scale(background_image, (800, 600))


# collection of possible planets
mercury = pygame.image.load('Textures/mercury.png')
venus = pygame.image.load('Textures/venus.png')
earth = pygame.image.load('Textures/earth.png')
luna = pygame.image.load('Textures/luna.png')
mars = pygame.image.load('Textures/mars.png')
jupiter = pygame.image.load('Textures/jupiter.png')
uranus = pygame.image.load('Textures/uranus.png')
neptune = pygame.image.load('Textures/neptune.png')
saturn = pygame.image.load('Textures/saturn.png')

planet_list = [mercury, venus, earth, luna, 
               mars, jupiter, uranus, neptune]
random_index = random.randint(0, 7)

# Planet attributes
planet_radius = random.randint(100, 200)
planet_x, planet_y = 400, 300
planet = pygame.transform.scale(planet_list[random_index], (planet_radius*2, planet_radius*2))
gravitational_force = 0.0
orbit_height = planet_radius + 50

# Spaceship attributes
ship_width, ship_height = 60, 60
ship_x, ship_y = 400.0, (150 - (planet_radius - 150))
throttle = 0.0
ship = pygame.image.load('Textures/rocket.png')  # Load the ship image
ship = pygame.transform.scale(ship, (ship_width, ship_height))  # Resize if needed
ship_velocity = pygame.Vector2(0.0, 0.0)  # Initial velocity
# set to decimals to prevent rounding to whole numbers
ship_angle = 0


# gets the center of the planet and ship images
ship_rect = ship.get_rect()  # Get the rectangle of the ship image
ship_rect.center = (ship_x, ship_y)  # Set the initial ship position
planet_rect = planet.get_rect()  # Get the rectangle of the planet image
planet_rect.center = (planet_x+30, planet_y+30)  # Set the planet position

# Create a list to store the spaceship's positions for the path
ship_path = []
ship_distances = [155, 150]
# keeps track of ship's change in velocity
delta_v = 50

# tracks global orbital parameters
speed = 0
apoapsis = 155
periapsis = 150
major_axis = planet_radius
distance = 150

clock = pygame.time.Clock()


running = True
while running:
    # draws the background image
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # draws the planet and ship
    screen.blit(planet, planet_rect)  # Draw planet at its position
    screen.blit(ship, ship_rect)
	
	# saves a copy of the ship to rotate
    saved_image = pygame.image.load('Textures/rocket.png')  # Load the ship image
    saved_image = pygame.transform.scale(saved_image, (ship_width, ship_height))
    
    # tracks game time
    gtime = (pygame.time.get_ticks()) / 1000
    
    
    # function to reset game
    def reset_game():
        global ship_rect, ship_angle, ship, delta_v, ship_velocity, ship_distances
        ship_rect.center = (ship_x, ship_y)
        ship_velocity.x = 0.0
        ship_velocity.y = 0.0
        delta_v = 50
        
        # clears distances list, adds values to prevent zero list errors
        ship_distances = [155,150]
        
        # resets spin
        ship_angle = 0
        ship = pygame.transform.rotate(saved_image, ship_angle)
        ship_rect = ship.get_rect(center=ship_rect.center)
        
    # applies changes in velocity and delta v
    def apply_throttle():
        global delta_v, ship_velocity
        ship_velocity.x += throttle * math.cos(math.radians(ship_angle+90))
        ship_velocity.y += throttle * -math.sin(math.radians(ship_angle+90))
        delta_v = delta_v - throttle
        
    # function to rotate ship
    def rotate_ship(angle):
        global ship_rect, ship_angle, ship, delta_v
        ship_angle = ship_angle + angle
        ship = pygame.transform.rotate(saved_image, ship_angle)
        ship_rect = ship.get_rect(center=ship_rect.center) # re-centers ship spin
        delta_v = delta_v - (throttle/5)


    keys = pygame.key.get_pressed()
    # rotates ship
    if keys[pygame.K_a]:
        rotate_ship(10)
    if keys[pygame.K_d]:
        rotate_ship(-10)

    # moves ship
    if keys[pygame.K_w] and delta_v > 0:
        apply_throttle()
        
    # if spacebar is pressed
    if keys[pygame.K_SPACE]:
        # calls reset game function
        reset_game()

    # sets ship throttle
    if keys[pygame.K_UP]:
        throttle = throttle + 0.025
    if keys[pygame.K_DOWN]:
        throttle = throttle - 0.025
        
    # restricts thrust
    if throttle > 1:
    	throttle = 1
    if throttle < 0:
        throttle = 0
        
    # if fuel runs out
    if delta_v < 0:
        delta_v = 0.0
    
    
    # Update ship position based on its velocity
    ship_rect.x += ship_velocity.x
    ship_rect.y += ship_velocity.y
    
    # calculates gravity force on the ship based on the planet's mass
    direction = pygame.Vector2(planet_x - ship_rect.x, planet_y - ship_rect.y)
    distance = direction.length()
    ship_distances.append(distance)
    
    if distance > planet_radius and distance < 500:  # stops gravity at planet's surface
        direction.normalize_ip()
        gravitational_force = G * (planet_mass / distance**2)
        gravity = direction * gravitational_force
        ship_velocity.x += gravity.x
        ship_velocity.y += gravity.y
    
    elif distance > 500:
        # resets game
        reset_game()
    else:
        ship_velocity.x = 0.0
        ship_velocity.y = 0.0
        speed = 0
    
    # Store the current position of the spaceship for the path
    ship_path.append((int(ship_rect.x+30), int(ship_rect.y+30)))
    
    # Limit the path length to avoid consuming too much memory
    if len(ship_path) > 2:  # Check for more than 2 points in the path
        # Draw the green path
        pygame.draw.lines(screen, GREEN, False, ship_path, 2)

        # Limit the path length to avoid consuming too much memory
        if len(ship_path) > 300:
            ship_path.pop(0)
        if len(ship_distances) > 300:
            ship_distances.pop(0)
    
    
    # keeps track of the ship parameters
    speed = round(ship_velocity.length(), 3)
    orbit_goal = round(math.sqrt( (planet_mass * G) / orbit_height ), 3)
    gravitational_force = round(gravitational_force, 3)
    delta_v = round(delta_v, 3)
    percent_throttle = round(throttle*100, 3)
    
    # calculates specific energy of orbit E = (v^2 / 2) - ((G*M) / r)
    specific_energy = (speed**2 / 2) - ((G*planet_mass) / distance)
    semi_major_axis = - (G * planet_mass) / (2 * specific_energy)
    
    # calculates apoapsis and periapsis using specific energy and semi major axis
    periapsis = semi_major_axis * math.sqrt(1 + ((specific_energy*semi_major_axis) / (G*planet_mass)))
    # prevents periapsis from being negative or greater than apoapsis
    if periapsis < 0:
        periapsis = 0
    if periapsis > apoapsis:
        periapsis = apoapsis
    
    # keeps track of orbital parameters
    path_array = np.array(ship_distances)
    apoapsis = round(np.max(path_array), 3)
    periapsis = round(periapsis, 3) # uses path array due to issues with calculations
    eccentricity = round((apoapsis-periapsis) / (apoapsis+periapsis), 3)
    altitude = round(distance, 3)
    
    
    # render text
    font = pygame.font.Font(None, 26)
    speed_text = font.render(f"Velocity (m/s): {speed}", True, (255, 255, 255))
    orbit_text = font.render(f"Orbit Goal (m/s): {orbit_goal}", True, (255, 255, 255))
    gravity_text = font.render(f"Gravity (m/s^2): {gravitational_force}", True, (255, 255, 255))
    delta_text = font.render(f"Delta-V (m/s): {delta_v}", True, (255, 255, 255))
    throttle_text = font.render(f"% Thrust: {percent_throttle}", True, (255, 255, 255))
    time_text = font.render(f"Time (s): {gtime}", True, (255, 255, 255))
    apoapsis_text = font.render(f"Apoapsis (m): {apoapsis}", True, (255, 255, 255))
    periapsis_text = font.render(f"Periapsis (m): {periapsis}", True, (255, 255, 255))
    eccentricity_text = font.render(f"Eccentricity: {eccentricity}", True, (255, 255, 255))
    altitude_text = font.render(f"Altitude: {altitude}", True, (255, 255, 255))
    
    # displays speed text on the screen
    screen.blit(speed_text, (10, 10))
    screen.blit(gravity_text, (10, 30))
    screen.blit(orbit_text, (10, 50))
    screen.blit(delta_text, (10, 70))
    screen.blit(throttle_text, (10, 90))
    screen.blit(time_text, (600, 10))
    screen.blit(apoapsis_text, (600, 30))
    screen.blit(periapsis_text, (600, 50))
    screen.blit(eccentricity_text, (600, 70))
    screen.blit(altitude_text, (600, 90))
    
    
    # runs reinforcement learning for 120 seconds
    if gtime < 120:
        pass
        
    # resets game after 120 seconds    
    if gtime > 120 and gtime < 120.5:
        reset_game()

    pygame.display.update()
    clock.tick(30)

pygame.quit()
