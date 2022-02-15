import pygame

pygame.init()
window = pygame.display.set_mode((1280, 720))


class Physic:
    def __init__(self, x, y, width, height, acc, max_velocity):
        self.x_cord = x
        self.y_cord = y
        self.hor_velocity = 0
        self.ver_velocity = 0
        self.acc = acc
        self.max_velocity = max_velocity
        self.width = width
        self.height = height
        self.previous_x = x
        self.previous_y = y
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)

    def physic_tick(self, beams):
        self.ver_velocity += 0.7
        self.x_cord += self.hor_velocity
        self.y_cord += self.ver_velocity
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)
        for beam in beams:
            if beam.hitbox.colliderect(self.hitbox):
                # self.x_cord = self.previous_x
                self.y_cord = self.previous_y
                self.ver_velocity = 0

        self.previous_x = self.x_cord
        self.previous_y = self.y_cord


class Player(Physic):
    def __init__(self):
        self.image = pygame.image.load("player.png")
        width = self.image.get_width()
        height = self.image.get_height()
        super().__init__(0, 580, width, height, 0.5, 5)

    def tick(self, keys, beams):  # will run once a loop iteration
        self.physic_tick(beams)
        if keys[pygame.K_a] and self.hor_velocity > self.max_velocity * -1:
            self.hor_velocity -= self.acc
        if keys[pygame.K_d] and self.hor_velocity < self.max_velocity:
            self.hor_velocity += self.acc
        if not (keys[pygame.K_d] or keys[pygame.K_a]):
            if self.hor_velocity > 0:
                self.hor_velocity -= self.acc
            if self.hor_velocity < 0:
                self.hor_velocity += self.acc

        # self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)

    def draw(self):
        window.blit(self.image, (self.x_cord, self.y_cord))


class Beam:
    def __init__(self, x, y, width, height):
        self.x_cord = x
        self.y_cord = y
        self.width = width
        self.height = height
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)

    def draw(self, win):
        pygame.draw.rect(win, (128, 128, 128), self.hitbox)


def main():
    run = True
    player = Player()
    clock = 0
    beams = [
        Beam(10, 650, 1000, 40)
    ]
    background = pygame.transform.scale(pygame.image.load("background.png"), (1280, 720))
    # text_image = pygame.font.Font.render(pygame.font.SysFont("arial", 48), "Score: {}".format(score), True, (0, 0, 0))
    while run:
        clock += pygame.time.Clock().tick(60) / 1000  # max 60 fps
        game_events = pygame.event.get()
        for event in game_events:
            if event.type == pygame.QUIT:  # if players closes the game window
                run = False

        keys = pygame.key.get_pressed()

        player.tick(keys,beams)

        window.blit(background, (0, 0))  # draws background
        player.draw()
        for beam in beams:
            beam.draw(window)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
