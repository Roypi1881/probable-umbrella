import pygame, random, sys

WIDTH, HEIGHT = 600, 800
PLAYER_SPEED = 7
BULLET_SPEED = 10
ALIEN_SPEED = 2
ALIEN_DROP = 32

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

class Player:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH//2-30, HEIGHT-60, 60, 20)
    def move(self, dx):
        self.rect.x += dx * PLAYER_SPEED
        self.rect.x = max(0, min(WIDTH-60, self.rect.x))
    def draw(self):
        pygame.draw.rect(screen, (0,255,0), self.rect)

class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x-5, y-15, 10, 20)
    def update(self):
        self.rect.y -= BULLET_SPEED
    def draw(self):
        pygame.draw.rect(screen, (255,255,0), self.rect)

class Alien:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 28)
        self.alive = True
    def draw(self):
        if self.alive:
            pygame.draw.rect(screen, (255,0,0), self.rect)

def create_aliens(rows=4, cols=8):
    aliens = []
    for r in range(rows):
        row = []
        for c in range(cols):
            row.append(Alien(45+c*60, 50+r*50))
        aliens.append(row)
    return aliens

def main():
    player = Player()
    bullets = []
    aliens = create_aliens()
    direction = 1
    score = 0
    running = True

    while running:
        screen.fill((8,8,16))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: player.move(-1)
        if keys[pygame.K_RIGHT]: player.move(1)
        if keys[pygame.K_SPACE] and len(bullets)<3:
            bullets.append(Bullet(player.rect.centerx, player.rect.top))

        # Move aliens
        edge = False
        for row in aliens:
            for alien in row:
                if alien.alive:
                    alien.rect.x += direction * ALIEN_SPEED
                    if alien.rect.right > WIDTH or alien.rect.left < 0:
                        edge = True
        if edge:
            direction *= -1
            for row in aliens:
                for alien in row:
                    alien.rect.y += ALIEN_DROP

        # Bullet update
        for bullet in bullets[:]:
            bullet.update()
            if bullet.rect.y < 0:
                bullets.remove(bullet)
            else:
                for row in aliens:
                    for alien in row:
                        if alien.alive and bullet.rect.colliderect(alien.rect):
                            alien.alive = False
                            bullets.remove(bullet)
                            score += 10
                            break

        # Draw
        player.draw()
        for bullet in bullets: bullet.draw()
        for row in aliens: 
            for alien in row: alien.draw()
        screen.blit(font.render(f"Score: {score}", 1, (255,255,255)), (10,10))

        # Lose condition
        for row in aliens:
            for alien in row:
                if alien.alive and alien.rect.bottom > HEIGHT-80:
                    screen.blit(font.render("GAME OVER", 1, (255,0,0)), (WIDTH//2-90, HEIGHT//2))
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    return

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()