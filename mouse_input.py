import pygame


class MouseInput:
    LEFT_BUTTON = 1
    RIGHT_BUTTON = 3

    def __init__(self):
        self.left_mouse_down = False
        self.right_mouse_down = False
        self.terminate = False
        self.mouse_up_pos = (-1, -1)
        self.mouse_up_button = 0
        self.events = []

    def update(self):
        if self.mouse_up_pos != (-1, -1):
            self.mouse_up_pos = (-1, -1)
            self.mouse_up_button = 0
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pygame.QUIT:
                self.terminate = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.left_mouse_down = True
                elif event.button == 3:
                    self.right_mouse_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.left_mouse_down = False
                elif event.button == 3:
                    self.right_mouse_down = False
                self.mouse_up_pos = pygame.mouse.get_pos()
                self.mouse_up_button = event.button

    def is_terminated(self):
        return self.terminate

    def is_mouse_clicked(self):
        return self.mouse_up_pos != (-1, -1)

    def timer_event(self):
        return any([e.type == pygame.USEREVENT for e in self.events])