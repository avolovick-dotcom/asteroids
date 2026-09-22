import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from logger import log_state, log_event
from shot import Shot


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    dt = 0.0
    score = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)  
    Shot.containers = (shots, updatable, drawable)
    asteroid_field = AsteroidField()

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        
        updatable.update(dt)

        for asteroid in asteroids:
            for shot in shots:
                if shot.collides_with(asteroid):
                    score += asteroid.score_value()
                    log_event("asteroid_shot", score=score)
                    if player.award_extra_lives(score):
                        log_event("extra_life", lives=player.lives)
                    shot.kill()
                    asteroid.split()


            if not player.is_invulnerable and player.collides_with(asteroid):
                player.lose_life()
                log_event("player_hit", lives_remaining=player.lives)
                if player.lives <= 0:
                    print(f"Game over! Final score: {score}")
                    sys.exit()

        screen.fill("black")
        for object in drawable:
            object.draw(screen)

        score_surface = font.render(f"Score: {score}", True, "white")
        screen.blit(score_surface, (10, 10))
        lives_surface = font.render(f"Lives: {player.lives}", True, "white")
        screen.blit(lives_surface, (10, 46))

        log_state()
        pygame.display.flip()
        dt = clock.tick(60) / 1000



if __name__ == "__main__":
    main()
