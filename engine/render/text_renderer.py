import pygame
from engine import pyinit

class MessageKey():
    def __init__(self, text, color, bold):
        self.text = text
        self.color = color
        self.bold = bold

    def __hash__(self):
        return hash((self.text, self.color, self.bold))

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

class MessageValue():
    def __init__(self, label, coordinates, to_render = True):
        self.label = label
        self.coordinates = coordinates
        self.to_render = to_render

messages_pool = dict()

def render():
    for message_key, message_value in list(messages_pool.items()):
        if not message_value.to_render:
            del messages_pool[message_key]

    for message_value in messages_pool.values():
        if message_value.to_render:
            render_message(message_value)
            message_value.to_render = False

def render_message(message_value):
    pyinit.game_display.blit(message_value.label, message_value.coordinates)

def write(text, size, coordinates, bold = 0, color = (255, 255, 255)):
    message = MessageKey(text, color, bold)
    if message in messages_pool:
        messages_pool[message].to_render = True
        return

    font = pygame.font.SysFont("Arial", size)
    if bold:
        font.set_bold(bold)
    label = font.render(str(text), 1, color)
    messages_pool[message] = MessageValue(label, coordinates, True)