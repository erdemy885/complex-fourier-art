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
    "width":1920,
    "height":1080,
    "half-width":1920/2,
    "half-height":1080/2
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
            color = (round(alpha), round(alpha), 0)
            pygame.draw.aaline(screen, 
                               color, 
                               convert_coordinates(pos), 
                               convert_coordinates(trail[i-1][0]))
        alpha -= 255 * dt
        trail[i] = (pos, alpha)
    
    #remove faded points
    trail = [point for point in trail if point[1] > 0]

    pygame.display.flip()
    screen.fill("black")
    dt = clock.tick()/1000 * speed/100

pygame.quit()