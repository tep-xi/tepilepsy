#!/usr/bin/python

from tepilepsy.widget import Widget
import pygame, numpy

class Pygame(Widget):
    def load(self, panel):
        pygame.init()
        y, x = panel.shape[:2]
        self.screen = pygame.display.set_mode((x*10, y*10))
        self.temp = pygame.surface.Surface((x, y))
        pygame.display.set_caption(self.__class__.__name__)
    def update(self, panel):
        self.render(panel, pygame.event.get())
        pygame.surfarray.blit_array(self.temp, numpy.rollaxis(panel,1))
        pygame.transform.scale(self.temp, self.screen.get_size(), self.screen)
        pygame.display.update()
    def render(self, panel, events):
        raise NotImplementedError # subclasses override this instead of update
    def unload(self):
        pygame.quit()
    
class Display(Pygame):
    def __init__(self, widget):
        self.widget = widget
    def load(self, panel):
        Pygame.load(self, panel)
        self.widget.load(panel)
        pygame.display.set_caption(self.widget.__class__.__name__)
    def render(self, panel, events):
        self.widget.update(panel)
    def unload(self):
        self.widget.unload()
        Pygame.unload(self)
