import numpy as np
import math
import pygame
import random


'''NOTE: THE SCALING OF DATA SUCH AS RADIUS, ORBITAL RADIUS etc. ARE MIGHT NOT BE ACCURATE AND ARE JUST FOR REPRESENTATION
YOU CAN USE REAL DATA FOR MOON RADIUS AND PLANET'S ORBIT AND USE SOME SCALING FACTOR TO MAKE IT FIT THE SCREEN. up to you :) 
'''

pygame.init()

WIDTH = 1500
HEIGHT = 800
SUN_RAD = 90
SUN_COLOR = (240,184,19)
SUN_MASS = 1.989e30
G = 6.67430e-11

class Planet:
    def __init__(self, a, b, planet_rad, planet_color,planet_mass):
        self.planet_mass = planet_mass
        self.planet_color = planet_color
        self.planet_rad = planet_rad
        self.a = a
        self.b = b
        self.orb_vel = math.sqrt(G * SUN_MASS / (0.5 * (a+b) * 1.496e11))   
        self.orbital_period = 2 * math.pi * 0.5 * (a+b) / self.orb_vel
        self.orbital_frequency = 2 * np.pi / self.orbital_period
        self.x = WIDTH // 2 + a
        self.y = HEIGHT // 2
        self.positions = []
        self.t = 0 

    def update_pos(self, t):
        theta = self.orbital_frequency * t
        x = self.a * math.cos(theta)
        y = self.b * math.sin(theta)
        self.x = WIDTH // 2 + x
        self.y = HEIGHT // 2 + y
        self.positions.append((self.x, self.y))

    def draw_planet(self, window):
        dt = 0.001
        self.update_pos(self.t)
        pygame.draw.circle(window, self.planet_color, (int(self.x), int(self.y)), self.planet_rad)
        self.t += dt
        if len(self.positions) > 1:
            pygame.draw.lines(window, "gray", False, self.positions, 5)


class Moon:
    def __init__(self,orb_rad,moon_rad,host_planet,moon_color,freq_norm):
        self.freq_norm = freq_norm
        self.orb_rad = orb_rad
        self.moon_rad = moon_rad
        self.moon_color = moon_color
        self.host_planet = host_planet
        self.moon_orbVel = math.sqrt(G*self.host_planet.planet_mass/self.orb_rad*1.496e11)
        self.moon_orbital_period = 2*math.pi*self.orb_rad/self.moon_orbVel
        self.moon_orbFreq = 2 * math.pi * self.orb_rad/(self.freq_norm*self.moon_orbital_period)
        self.x = WIDTH//2 + self.host_planet.a + self.orb_rad
        self.y = HEIGHT//2
        self.positions = []
        self.t = 0

    def update_pos(self,t):
        theta = self.moon_orbFreq * t
        x = self.orb_rad*math.cos(theta)
        y = self.orb_rad*math.sin(theta)
        self.x = self.host_planet.x + x
        self.y = self.host_planet.y + y
        self.positions.append((self.x, self.y))

    def draw_moon(self,window):
        dt = 0.001
        self.update_pos(self.t)
        pygame.draw.circle(window,self.moon_color,(int(self.x),int(self.y)),self.moon_rad)
        self.t += dt
        if len(self.positions) > 1:
            pygame.draw.lines(window,"lightblue",False,self.positions,1)
        if len(self.positions) > 600:
            self.positions = self.positions[600:]
        
    


window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ORBITAL SYSTEM")

running = True
planet1 = Planet(300, 100, 7, "blue",5.97e24)
moon1 = Moon(15,3,planet1,"gray",1500)

planet2 = Planet(500,150,8,"orange",5.97e24)
moon2 = Moon(15,2,planet2,"white",1500)

planet3 = Planet(600,180,8,"red",5.97e24)
moon3 = Moon(15,3,planet3,"yellow",1500)

planet4 = Planet(800,300,8,"pink",5.97e24)
moon4 = Moon(15,3,planet4,"orange",1500)

pos_x = [random.randint(0,WIDTH) for i in range(5000)]
pos_y = [random.randint(0,HEIGHT) for j in range(5000)]



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill("black")
    
    for _ in range(len(pos_x)):
        pygame.draw.circle(window,(255,255,255),(pos_x[_],pos_y[_]),random.randint(1,2))
    pygame.draw.circle(window, SUN_COLOR, (WIDTH // 2 - 100, HEIGHT // 2), SUN_RAD)
    planet1.draw_planet(window)
    moon1.draw_moon(window)
    planet2.draw_planet(window)
    moon2.draw_moon(window)
    planet3.draw_planet(window)
    moon3.draw_moon(window)
    planet4.draw_planet(window)
    moon4.draw_moon(window)
    


    pygame.display.flip()
    pygame.time.delay(5)

pygame.quit()
