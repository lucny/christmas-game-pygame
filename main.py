import pygame
import random
import math

# Inicializace Pygame
pygame.init()

# Konstanty
WIDTH, HEIGHT = 800, 600
FPS = 60

# Barvy
WHITE = (255, 255, 255)
BLUE = (100, 100, 255)
LIGHT_BLUE = (200, 200, 255)
BLACK = (0, 0, 0)
ACTIVE_BORDER = (255, 0, 0)  # Červený obrys pro aktivní obdélník

# Inicializace obrazovky
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snowflake Simulation")

# Načtení obrázků a zvuků
snowflake_image = pygame.image.load("media/vlocka.png")  # Nahraďte správným souborem
background_image = pygame.image.load("media/vanoce.jpg")  # Nahraďte správným souborem
collision_sound = pygame.mixer.Sound("media/ding.wav")  # Nahraďte správným souborem

# Třída pro obdélníky
class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.fill_amount = 0
        self.active = False

    def display(self):
        # Nádoba
        color = LIGHT_BLUE if not self.active else ACTIVE_BORDER
        pygame.draw.rect(screen, LIGHT_BLUE, (self.x, self.y, self.w, self.h))
        pygame.draw.rect(screen, color, (self.x, self.y, self.w, self.h), 3 if self.active else 0)

        # Hladina
        fill_height = self.h * (self.fill_amount / 100)
        pygame.draw.rect(screen, BLUE, (self.x, self.y + self.h - fill_height, self.w, fill_height))

        # Procenta
        font = pygame.font.SysFont(None, 24)
        text = font.render(f"{int(self.fill_amount)}%", True, BLACK)
        screen.blit(text, (self.x + self.w // 2 - text.get_width() // 2, self.y + self.h // 2 - text.get_height() // 2))

    def add_content(self, flake):
        flake_area = math.pi * (flake.radius ** 2)
        rect_area = self.w * self.h
        self.fill_amount = min(100, self.fill_amount + (flake_area / rect_area) * 100)

    def detect_collision(self, flake):
        return (
            self.x < flake.x < self.x + self.w and
            self.y < flake.y + flake.radius < self.y + self.h
        )

    def contains_point(self, x, y):
        return self.x < x < self.x + self.w and self.y < y < self.y + self.h

    def move(self, dx, dy):
        self.x = max(0, min(self.x + dx, WIDTH - self.w))
        self.y = max(0, min(self.y + dy, HEIGHT - self.h))

# Třída pro vločky
class Snowflake:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-50, -10)
        self.radius = random.randint(5, 10)
        self.speed = random.uniform(1, 3)

    def display(self):
        scaled_image = pygame.transform.scale(snowflake_image, (self.radius * 2, self.radius * 2))
        screen.blit(scaled_image, (self.x - self.radius, self.y - self.radius))

    def update(self):
        self.y += self.speed

    def is_off_screen(self):
        return self.y - self.radius > HEIGHT

# Hlavní smyčka
def main():
    clock = pygame.time.Clock()
    running = True

    # Herní objekty
    rectangles = [Rectangle(200, 400, 100, 200), Rectangle(400, 400, 100, 200), Rectangle(600, 400, 100, 200)]
    snowflakes = []
    active_rectangle = None

    while running:
        screen.fill(WHITE)
        screen.blit(background_image, (0, 0))  # Zobrazení pozadí

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Kliknutí myší na obdélník
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for rect in rectangles:
                    if rect.contains_point(mx, my):
                        active_rectangle = rect
                        for r in rectangles:
                            r.active = False
                        rect.active = True
                        break

        # Pohyb aktivního obdélníku
        keys = pygame.key.get_pressed()
        if active_rectangle:
            if keys[pygame.K_LEFT]:
                active_rectangle.move(-5, 0)
            if keys[pygame.K_RIGHT]:
                active_rectangle.move(5, 0)
            if keys[pygame.K_UP]:
                active_rectangle.move(0, -5)
            if keys[pygame.K_DOWN]:
                active_rectangle.move(0, 5)

        # Přidávání nových vloček
        if random.random() < 0.1:
            snowflakes.append(Snowflake())

        # Aktualizace vloček
        for flake in snowflakes[:]:
            flake.update()
            flake.display()

            for rect in rectangles:
                if rect.detect_collision(flake):
                    rect.add_content(flake)
                    snowflakes.remove(flake)
                    collision_sound.play()
                    break

            if flake.is_off_screen():
                snowflakes.remove(flake)

        # Vykreslení obdélníků
        for rect in rectangles:
            rect.display()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
