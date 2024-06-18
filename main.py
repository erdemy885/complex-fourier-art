import pygame
import generate_vectors

pygame.init()
SCREEN = {
    "width":1280,
    "height":720,
    "half-width":1280/2,
    "half-height":720/2
    }
screen = pygame.display.set_mode((SCREEN["width"],SCREEN["height"]))
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

#1000 samples from pi.svg
points = generate_vectors.read_svg("pi.svg", 1000)
#100 pairs of vectors
coefficients = generate_vectors.get_coefficients(points, 100)
vectors = generate_vectors.get_vectors(coefficients)
trail = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #draw trail at end of last vector
    trail.append((vectors[len(vectors) - 1].head, 255))
    for i in range(len(trail)):
        pos, alpha = trail[i]
        if i > 0:
            color = (round(alpha), round(alpha), 0)
            pygame.draw.aaline(screen, 
                               color, 
                               convert_coordinates(pos), 
                               convert_coordinates(trail[i-1][0]))
        alpha -= 255 * dt
        trail[i] = (pos, alpha)
    
    #remove faded points
    trail = [point for point in trail if point[1] > 0]

    #draw and rotate vectors
    for i in range(len(vectors)):
        pygame.draw.aaline(screen, 
                           "white", 
                           convert_coordinates(vectors[i].tail), 
                           convert_coordinates(vectors[i].head))
        vectors[i].rotate(dt)
        coefficients[i] = (vectors[i].frequency, vectors[i].vec)
    
    vectors = generate_vectors.get_vectors(coefficients)

    pygame.display.flip()
    screen.fill("black")
    dt = clock.tick()/1000 * speed/100

pygame.quit()