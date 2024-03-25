class Seeker:
    def __init__(self, name):
        self.name = name
        self.position = (0, 0)  # Vị trí ban đầu

    def move(self, direction):
        x, y = self.position
        if direction == 'left':
            x -= 1
        elif direction == 'right':
            x += 1
        elif direction == 'up':
            y += 1
        elif direction == 'down':
            y -= 1
        self.position = (x, y)

    def search(self):
        print(f"{self.name} is searching...")