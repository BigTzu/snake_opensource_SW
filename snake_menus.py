from snake_settings import *
import snake as snake_main
from snake_save_and_ranking import *
from algo import play_algo

class Menu:
    def __init__(self, save_and_load, ranking):
        self.font = pygame.font.Font("assets/Bebas-Regular.ttf", 75)
        self.save_and_load = save_and_load
        self.ranking = ranking

    def check_buttons(self, buttons_list, mouse_position):
        for button in buttons_list:
            if mouse_position[0] in range(button.rect.left, button.rect.right) and \
                    mouse_position[1] in range(button.rect.top, button.rect.bottom):
                button.text = button.font.render(button.text_input, True, "White")
            else:
                button.text = button.font.render(button.text_input, True, "#a7843b")
            button.update(screen)

    def check_mouse(self, button, position):
        if position[0] in range(button.rect.left, button.rect.right) and \
                position[1] in range(button.rect.top, button.rect.bottom):
            return True
        return False

     
    def ingame_menu_loop(self, snake):
        pygame.display.set_caption("Ingame Menu")

        running = True
        while running:
            title = self.font.render("INGAME MENU", True, "#a7843b")
            title_rect = title.get_rect(center=(400, 100))
            mouse_position = pygame.mouse.get_pos()

            resume_button = Button(image=pygame.image.load("assets/button_rect.png"), x_pos=400, y_pos=250,
                                 text_input="RESUME", font=self.font)
            restart_button = Button(image=pygame.image.load("assets/button_rect.png"), x_pos=400, y_pos=400,
                                 text_input="RESTART", font=self.font)
            save_button = Button(image=pygame.image.load("assets/button_rect.png"), x_pos=400, y_pos=550,
                                    text_input="SAVE", font=self.font)
            exit_button = Button(image=pygame.image.load("assets/button_rect.png"), x_pos=400, y_pos=700,
                                 text_input="EXIT", font=self.font)

            screen.blit(title, title_rect)
            self.check_buttons([resume_button, restart_button, save_button, exit_button], mouse_position)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.check_mouse(resume_button, mouse_position):
                        pygame.display.set_caption("Snake Solo Play")
                        running = False
                        return 0

                    elif self.check_mouse(restart_button, mouse_position):
                        pygame.display.set_caption("Snake Solo Play")
                        running = False
                        snake_main.play(resume=True)
                        return 1
                        
                    elif self.check_mouse(save_button, mouse_position):
                        pygame.display.set_caption("Snake Solo Play")
                        self.save_and_load.save(snake)
                        running = False
                        snake_main.play()
                        return 1

                    elif self.check_mouse(exit_button, mouse_position):
                        running = False
                        self.main_menu_loop()
                        return 1

            pygame.display.update()

    def special_mode_menu_loop(self, which_mode):
        pygame.display.set_caption("Ingame Menu")

        running = True
        while running:
            title = self.font.render("INGAME MENU", True, "#a7843b")
            title_rect = title.get_rect(center=(400, 100))
            mouse_position = pygame.mouse.get_pos()

            resume_button = Button(image=pygame.image.load("assets/button_rect.png"), x_pos=400, y_pos=250,
                                 text_input="RESUME", font=self.font)
            restart_button = Button(image=pygame.image.load("assets/button_rect.png"), x_pos=400, y_pos=400,
                                 text_input="RESTART", font=self.font)
            exit_button = Button(image=pygame.image.load("assets/button_rect.png"), x_pos=400, y_pos=550,
                                 text_input="EXIT", font=self.font)

            screen.blit(title, title_rect)
            self.check_buttons([resume_button, restart_button, exit_button], mouse_position)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.check_mouse(resume_button, mouse_position):
                        pygame.display.set_caption("Snake")
                        running = False
                    elif self.check_mouse(restart_button, mouse_position):
                        pygame.display.set_caption("Snake")
                        if which_mode == "dual":
                            snake_main.dualPlay(resume=True)
                        elif which_mode == "auto":
                            snake_main.play_algo(resume=True)
                    elif self.check_mouse(exit_button, mouse_position):
                        snake_main.play()

            pygame.display.update()

    def get_username(self, ranking, snake):
        font = pygame.font.SysFont(None, 35)
        text = ""
        inpt(screen, fpsClock, font, text, ranking, snake)
    def display_score(self, text):
        screen.fill(0)
        run = True
        text_display(text, 300, 400)
        pygame.display.flip()
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

    loaded = False

    def main_menu_loop(self):
        pygame.display.set_caption("Main Menu")
        running = True
        while running:
            screen.blit(pygame.image.load("assets/menu_background.jpg"), (0, 0))
            title = self.font.render("MAIN MENU", True, "#a7843b")
            title_rect = title.get_rect(center=(400, 100))
            mouse_position = pygame.mouse.get_pos()

            play_button = Button(image=pygame.image.load("assets/button_rect.png"), x_pos=200, y_pos=250,
                                 text_input="SINGLE PLAY", font=self.font)
            dual_play_button = Button(image=pygame.image.load("assets/button_rect.png"), x_pos=605, y_pos=250,
                                 text_input="DUAL PLAY", font=self.font)
            auto_play_button = Button(image=pygame.image.load("assets/button_rect.png"), x_pos=400, y_pos=370,
                                 text_input="AUTO PLAY", font=self.font)
            load_button = Button(image=pygame.image.load("assets/button_rect.png"), x_pos=400, y_pos=490,
                                 text_input="LOAD", font=self.font)
            ranking_button = Button(image=pygame.image.load("assets/button_rect.png"), x_pos=400, y_pos=610,
                                    text_input="RANKING", font=self.font)
            exit_button = Button(image=pygame.image.load("assets/button_rect.png"), x_pos=400, y_pos=730,
                                 text_input="EXIT", font=self.font)

            screen.blit(title, title_rect)
            self.check_buttons([play_button, dual_play_button, auto_play_button, load_button, ranking_button,
                                exit_button], mouse_position)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.check_mouse(play_button, mouse_position):
                        pygame.display.set_caption("Snake Solo Play")
                        snake_main.play(resume=True)
                    elif self.check_mouse(dual_play_button, mouse_position):
                        pygame.display.set_caption("Snake Dual Play")
                        running = False
                        snake_main.dualPlay(resume=True)
                    elif self.check_mouse(auto_play_button, mouse_position):
                        pygame.display.set_caption("Snake Auto Play")
                        running = False
                        play_algo(resume=True)
                    elif self.check_mouse(exit_button, mouse_position):
                        pygame.quit()
                        sys.exit()
                    elif self.check_mouse(ranking_button, mouse_position):
                        self.ranking.get_ranking()
                    elif self.check_mouse(load_button, mouse_position):
                        self.loaded = True
                        pygame.display.set_caption("Snake Solo Play")
                        running = False

            pygame.display.update()


class Button:
    def __init__(self, image, x_pos, y_pos, text_input, font):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.font = font
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, "#a7843b")
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)
