from snake_settings import *

def text_display(word,x,y):
    font = pygame.font.SysFont(None, 75)
    text = font.render("{}".format(word), True, "#a7843b")
    return screen.blit(text,text.get_rect(center=screen.get_rect().center))

def inpt(window, clock, font, text, ranking, snake):
    input_active = True
    window.fill(0)
    pygame.display.flip()
    one_time = True
    run = True
    while run:
        text_display("Please enter your name: ", 300, 400)
        if one_time == True:
            pygame.display.flip()
            one_time = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                input_active = True
                text = ""
            elif event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    input_active = False
                    run = False
                    ranking.set_ranking((len(snake.snake) - 3) * 100, text)
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

            window.fill(0)
            text_surf = font.render(text, True, "#a7843b")
            text_display("Please enter your name: ", 300, 400)
            window.blit(text_surf, text_surf.get_rect(center=window.get_rect().center))
            pygame.display.flip()

class Save_and_Load:
    def save(self, snake):
        with open('save_file.txt', 'wb') as f: pk1.dump(snake, f)

    def get_load_info(self):
        with open('save_file.txt', 'rb') as f: arrayname1 = pk1.load(f)
        return arrayname1

class Ranking:

    def __init__(self):
        self.ranking_list = []
        if os.path.exists("rankings.txt"):
            with open("rankings.txt") as file:
                for line in file:
                    line = line.replace('\n', '')
                    splited_line = line.split(';')
                    self.ranking_list.append([splited_line[0], int(splited_line[1])])

    def set_ranking(self, score, username):
        self.ranking_list.append([username, score])
        self.ranking_list = sorted(self.ranking_list, key = lambda x: int(x[1]))
        self.ranking_list.reverse()
        f = open("rankings.txt", 'w')
        for elem in self.ranking_list:
            f.write(elem[0].__str__())
            f.write(";")
            f.write(elem[1].__str__())
            f.write("\n")

    def get_ranking(self):
        if os.path.exists("rankings.txt"):
            screen.fill(0)
            text = ""
            for elem in self.ranking_list:
                text += elem[0] + ' ' + elem[1].__str__()
            pygame.display.flip()
            one_time = True
            run = True
            input_active = True
            font = pygame.font.SysFont(None, 45)
            while run:
                if one_time == True:
                    pygame.display.flip()
                    one_time = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        input_active = True
                    elif event.type == pygame.KEYDOWN and input_active:
                        if event.key == pygame.K_RETURN:
                            input_active = False
                            run = False
                    screen.fill(0)
                    text_display("RANKING", 0,0)
                    text = font.render("{}".format(self.ranking_list[0][0] + ' ' + str(self.ranking_list[0][1])), True, "#a7843b")
                    screen.blit(text, (320, 200))
                    if (len(self.ranking_list) > 1):
                        text = font.render("{}".format(self.ranking_list[1][0] + ' ' + str(self.ranking_list[1][1])), True, "#a7843b")
                        screen.blit(text, (320, 350))
                    if (len(self.ranking_list) > 2):
                        text = font.render("{}".format(self.ranking_list[2][0] + ' ' + str(self.ranking_list[2][1])), True, "#a7843b")
                        screen.blit(text, (320, 500))
                    pygame.display.flip()