class Hider:
    def __init__(self, name):
        self.name = name
        self.position = (0, 0)  # Vị trí ban đầu
        self.steps = 0

    def move(self, direction):
        # Phương thức di chuyển của Hider
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
        self.steps += 1
        if self.steps % 5 == 0:  # Phát tín hiệu mỗi 5 bước
            self.signal()

    def signal(self):
        # Phương thức phát tín hiệu
        print(f"{self.name} is signaling at position {self.position} after {self.steps} steps.")