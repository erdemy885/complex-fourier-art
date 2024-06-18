import pygame
import generate_vectors

#number of samples and image to sample from
points = generate_vectors.read_svg("fourier.svg", 10000)
#number of vector pairs
coefficients = generate_vectors.get_coefficients(points, 1000)
vectors = generate_vectors.get_vectors(coefficients)
trail = []

pygame.init()
SCREEN = {
    "width":3840,
    "height":1440,
    "half-width":3840/2,
    "half-height":1440/2
    }
#create surface for trail with per pixel alphas
trail_surface = pygame.Surface((SCREEN["width"],SCREEN["height"]), pygame.SRCALPHA)
trail_surface.fill((0, 0, 0, 0))
screen = pygame.display.set_mode((SCREEN["width"],SCREEN["height"]))
screen.fill("black")
running = True
clock = pygame.time.Clock()

#speed should range from 1-100
speed = 1
dt = 0

#moves origin to center of window
def convert_coordinates(c):
    x = c.real + SCREEN["half-width"]
    y = -c.imag + SCREEN["half-height"]
    return (x,y)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #draw and rotate vectors
    for i in range(len(vectors)):
        pygame.draw.aaline(screen, 
                           "white", 
                           convert_coordinates(vectors[i].tail), 
                           convert_coordinates(vectors[i].head))
        vectors[i].rotate(dt)
        coefficients[i] = (vectors[i].frequency, vectors[i].vec)
    
    #reattach rotated vectors
    vectors = generate_vectors.get_vectors(coefficients)

    #draw trail at end of last vector
    trail.append((vectors[len(vectors) - 1].head, 255))
    for i in range(len(trail)):
        pos, alpha = trail[i]
        if i > 0:
            color = pygame.Color("yellow")
            color.a = round(alpha)
            pygame.draw.aaline(trail_surface, 
                               color, 
                               convert_coordinates(pos), 
                               convert_coordinates(trail[i-1][0]))
        alpha -= 255 * dt
        trail[i] = (pos, alpha)
    
    #remove faded points
    trail = [point for point in trail if point[1] > 0]

    #draw trail_surface onto screen
    screen.blit(trail_surface, (0, 0))

    #update screen surface then clear it
    #not clearing trail_surface lets lines build up giving added thickness while maintainig antialiasing
    #usually you can't adjust thickness on antialiased lines, only on regular lines
    pygame.display.flip()
    screen.fill("black")
    # trail_surface.fill((0, 0, 0, 0))
    dt = clock.tick()/1000 * speed/100

pygame.quit()