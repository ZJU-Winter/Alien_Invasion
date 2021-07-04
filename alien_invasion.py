import sys
from time import sleep

import pygame
import json
import constants as c
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet, Bullet_plus_left, Bullet_plus_right
from alien import Alien
from text import Text
import sound_effects as se


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics,
        #   and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.text = Text(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Make buttons.
        self.play_button = Button(self, "Play", -0.6)
        self.goon_button = Button(self, "Continue", -0.6)
        self.score_button = Button(self, "Score", 0.2)
        self.help_button = Button(self, "Help", 1)
        self.exit_button = Button(self, "Exit", 1.8)
        self.back_button = Button(self, "Back to Menu", 3.7, 36, 190, 40)
        self.record_file = './scores.json'
        with open(self.record_file, 'r') as f:
            self.record = json.load(f)
    #   back 上一点         主menu往下一点

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_state == c.RUN:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.stats.game_state == c.MENU:
                    self._check_play_button(mouse_pos)
                    self._check_score_button(mouse_pos)
                    # self._check_continue_button(mouse_pos)
                    self._check_exit_button(mouse_pos)
                    self._check_help_button(mouse_pos)
                if self.stats.game_state == c.HELP or self.stats.game_state == c.SCORE or self.stats.game_state == c.FINAL:
                    self._check_back_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.stats.game_state == c.MENU and not c.PAUSE:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()

            # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_state = c.RUN
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

        if button_clicked and self.stats.game_state == c.MENU and c.PAUSE:
            self.stats.game_state = c.RUN
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            c.PAUSE = False
            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _check_score_button(self, mouse_pos):
        """Show information about scores when the player clicks Score."""
        button_clicked = self.score_button.rect.collidepoint(mouse_pos)
        # implement score_button here
        if button_clicked:
            self.stats.game_state = c.SCORE

    def _check_back_button(self, mouse_pos):
        """Show information about scores when the player clicks Score."""
        button_clicked = self.back_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.stats.game_state == c.FINAL:
            # Reset the game statistics.
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            self.stats.game_state = c.MENU
        elif button_clicked and self.stats.game_state != c.FINAL:
            self.stats.game_state = c.MENU

    def _check_help_button(self, mouse_pos):
        """Show information about scores when the player clicks Score."""
        button_clicked = self.help_button.rect.collidepoint(mouse_pos)
        if button_clicked:
            self.stats.game_state = c.HELP

    def _check_exit_button(self, mouse_pos):
        """Show information about scores when the player clicks Score."""
        button_clicked = self.exit_button.rect.collidepoint(mouse_pos)
        if button_clicked:
            sys.exit()

    # def _check_continue_button(self, mouse_pos):
    #     """Continue the game when the player clicks Score."""
    #     button_clicked = self.continue_button.rect.collidepoint(mouse_pos)
    #     if button_clicked and not self.stats.game_state:
    #         self.stats.game_state = True
    #
    #         # Hide the mouse cursor.
    #         pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            if self.stats.game_state == c.RUN:
                self._fire_bullet()
        elif event.key == pygame.K_z:
            if self.stats.game_state == c.RUN and self.stats.level > 3:
                self._fire_bullet_plus_left()
        elif event.key == pygame.K_c:
            if self.stats.game_state == c.RUN and self.stats.level > 3:
                self._fire_bullet_plus_right()
        elif event.key == pygame.K_r:
            if self.stats.game_state == c.DEAD:
                # Get rid of any remaining aliens and bullets.
                self.aliens.empty()
                self.bullets.empty()

                # Create a new fleet and center the ship.
                self._create_fleet()
                self.ship.center_ship()
                self.stats.game_state = c.RUN
            elif self.stats.game_state == c.PASS:
                self.bullets.empty()
                self._create_fleet()
                self.settings.increase_speed()

                # Increase level.
                self.stats.level += 1
                self.sb.prep_level()

                self.stats.game_state = c.RUN
            elif self.stats.game_state == c.MENU and c.PAUSE:
                self.stats.game_state = c.RUN
                # Hide the mouse cursor.
                c.PAUSE = False
                pygame.mouse.set_visible(False)
        elif event.key == pygame.K_p:
            if self.stats.game_state == c.RUN:
                self.stats.game_state = c.MENU
                c.PAUSE = True
                pygame.mouse.set_visible(True)

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            se.bullet_sound.play()

    def _fire_bullet_plus_left(self):
        """Create a new bullet towards left and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed - 2:
            new_bullet = Bullet_plus_left(self)
            self.bullets.add(new_bullet)
            se.bullet_sound.play()

    def _fire_bullet_plus_right(self):
        """Create a new bullet towards left and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed - 2:
            new_bullet = Bullet_plus_right(self)
            self.bullets.add(new_bullet)
            se.bullet_sound.play()

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.sb.prep_score()
            se.alien_sound.play()

        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.stats.game_state = c.PASS

    def _update_aliens(self):
        """
        Check if the fleet is at an edge,
          then update the positions of all aliens in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 1:
            # Decrement ships_left, and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Pause.
            sleep(0.1)
            self.stats.game_state = c.DEAD
            # pygame.mouse.set_visible(True)
        else:
            sleep(0.1)
            self.stats.game_state = c.FINAL
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)
        self.ship.blitme()
        # Draw the score information.
        self.sb.show_score()
        cover = pygame.Surface((pygame.display.Info().current_w, pygame.display.Info().current_h), pygame.SRCALPHA)
        cover.fill(c.COVER)

        # Draw the play button if the game is inactive.
        if self.stats.game_state == c.MENU and c.PAUSE:
            self.screen.blit(cover, (0, 0))
            self.text.title()
            self.play_button.draw_button()
            self.goon_button.draw_button()
            self.score_button.draw_button()
            self.help_button.draw_button()
            self.exit_button.draw_button()
            self.text.goon()
        elif self.stats.game_state == c.MENU and not c.PAUSE:
            self.screen.blit(cover, (0, 0))
            self.text.title()
            self.play_button.draw_button()
            self.score_button.draw_button()
            self.help_button.draw_button()
            self.exit_button.draw_button()
        elif self.stats.game_state == c.DEAD:
            # when the game stops and you still have some chances
            self.screen.blit(cover, (0, 0))
            self.text.diaplay("You dead, " + str(self.stats.ships_left) + " ships left." if self.stats.ships_left > 1
                              else "You dead, " + str(self.stats.ships_left) + " ship left.")
            self.text.goon()
        elif self.stats.game_state == c.PASS:
            # when the game stops and you still have some chances
            self.screen.blit(cover, (0, 0))
            self.text.diaplay("Cong! " + "Next Level: " + str(self.stats.level + 1))
            if self.stats.level == 3:
                self.text.diaplay("You can press z/c to fire anterolaterally now.", 1, 25, "Consolas")
            self.text.goon()
        elif self.stats.game_state == c.FINAL:
            # when the game stops and you just don't have any chances
            # update scores.json

            self.stats.score = round(self.stats.score, -1)
            if int(self.record['3']) < self.stats.score < int(self.record['2']):
                self.record['3'] = str(self.stats.score)
                self.stats.rank = 3
            elif int(self.record['2']) < self.stats.score < int(self.record['1']):
                self.record['3'] = self.record['2']
                self.record['2'] = str(self.stats.score)
                self.stats.rank = 2
            elif self.stats.score > int(self.record['1']):
                self.record['3'] = self.record['2']
                self.record['2'] = self.record['1']
                self.record['1'] = str(self.stats.score)
                self.stats.rank = 1
            elif self.stats.score == int(self.record['1']):
                self.stats.rank = 1
            elif self.stats.score == int(self.record['2']):
                self.stats.rank = 2
            elif self.stats.score == int(self.record['3']):
                self.stats.rank = 3

            with open(self.record_file, 'w') as f:
                json.dump(self.record, f)

            self.screen.blit(cover, (0, 0))

            self.text.finial(str(self.stats.score), self.stats.rank)

            self.back_button.draw_button()

        elif self.stats.game_state == c.SCORE:
            self.screen.blit(cover, (0, 0))
            self.text.record(self.record['1'], self.record['2'], self.record['3'])
            self.back_button.draw_button()

        elif self.stats.game_state == c.HELP:
            self.screen.blit(cover, (0, 0))
            self.text.help()
            self.back_button.draw_button()
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
