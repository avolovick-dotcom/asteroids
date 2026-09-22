import pygame
from circleshape import CircleShape
from shot import Shot
from constants import *

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown_timer = 0.0
        self.lives = PLAYER_STARTING_LIVES
        self.invulnerability_timer = 0.0
        self.extra_lives_awarded = 0

    @property
    def is_invulnerable(self) -> bool:
        return self.invulnerability_timer > 0

    def lose_life(self) -> None:
        self.lives -= 1
        self.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.velocity = pygame.Vector2(0, 0)
        self.invulnerability_timer = PLAYER_RESPAWN_INVULNERABILITY_SECONDS

    def award_extra_lives(self, score: int) -> bool:
        earned = score // EXTRA_LIFE_SCORE_THRESHOLD
        gained = False
        while earned > self.extra_lives_awarded:
            self.extra_lives_awarded += 1
            self.lives = min(self.lives + 1, PLAYER_MAX_LIVES)
            gained = True
        return gained

    # in the Player class
    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        # Draw the player ship as a white polygon outline
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt) -> None:
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt) -> None:
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        if self.shot_cooldown_timer > 0:
            self.shot_cooldown_timer -= dt
        if self.invulnerability_timer > 0:
            self.invulnerability_timer -= dt

    def shoot(self):
        if self.shot_cooldown_timer > 0:
            return
        self.shot_cooldown_timer = PLAYER_SHOT_COOLDOWN_SECONDS

        shot = Shot(self.position.x, self.position.y)
        velocity = pygame.Vector2(0, 1).rotate(self.rotation)
        shot.velocity = velocity * PLAYER_SHOT_SPEED

        
    