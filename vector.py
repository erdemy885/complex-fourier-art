import cmath

class vector:
    def __init__(self, tail, vec, frequency):
        self.tail = tail
        self.vec = vec
        self.head = tail + vec
        self.frequency = frequency

    def rotate(self, theta):
        rotation = 2 * cmath.pi * self.frequency * theta
        self.vec = self.vec * cmath.exp(1j * rotation)
        self.head = self.tail + self.vec
    
    def __str__(self):
        return(f'Tail:{self.tail} Vector:{self.vec} Head:{self.head} Frequency:{self.frequency} Magnitude:{abs(self.vec)}')