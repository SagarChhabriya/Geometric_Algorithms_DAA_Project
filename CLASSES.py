import pygame
import random as r
from cosmetics import * 

class point:
    def __init__(self,x,y,color,size):
        self.x = x
        self.y = y
        self.color = color
        self.radius = size
        self.completed = True

    def dynamic_color_draw(self,surface,colo):
        pygame.draw.circle(surface,colo,(self.x,self.y),self.radius)
    def update_coords(self,coords):
        self.x = coords[0]
        self.y = coords[1]
    def draw(self, surface):
        pygame.draw.circle(surface,self.color,(self.x,self.y),self.radius)

    def drawtopoint(self,screen,outr):
        pygame.draw.line(screen,self.color,(self.x,self.y),(outr.x,outr.y))

class line:
    def __init__(self,w,duration,color):
        self.w = w
        self.duration = duration
        self.elapsed = 0
        self.color = color;

    def update(self,dt):
        self.elapsed +=dt
        if self.elapsed >= self.duration:
            self.elapsed = self.duration
            self.completed = False
        else:
            self.completed = True

    def draw(self,screen,point1,point2):
        if point1.x == point2.x and point1.y == point2.y:
            self.elapsed = self.duration
            
        else:
            progress = self.elapsed / self.duration
            current_x = int(point1.x + (point2.x - point1.x) * progress)
            current_y = int(point1.y + (point2.y - point1.y) * progress)
            pygame.draw.line(screen, self.color, (point1.x,point1.y),(current_x, current_y), self.w)
            
import pygame

class Text:
    def __init__(self, text, font, font_size, color, x, y):
        self.text = text
        self.font_size = font_size
        self.color = color
        self.x = x
        self.y = y
        self.font = pygame.font.Font(font, font_size)
        self.surface = self.font.render(text, True, color)

    def update_text(self, new_text):
        self.text = new_text
        self.surface = self.font.render(new_text, True, self.color)

    def draw(self, screen):
        screen.blit(self.surface, (self.x, self.y))


class trail:
    def __init__(self, firstset,trailsize):
        self.trailcoords = firstset
        self.trailsize = trailsize
        self.allsize = []
        #define sizes. size gets smaller from n to 1
        for a in range(trailsize,0 ,-1):
            self.allsize.append(a)
        #create trailpoints from class points
        self.trailpoints = []
        for n,a in enumerate(self.trailcoords):
            self.trailpoints.append(point(a[0],a[1],(r.randint(0,255),r.randint(0,255),r.randint(0,255)),self.allsize[n]))
            
    def updatetrail(self,newpos):
        
        #update coordslist
        self.trailcoords.pop()
        self.trailcoords.insert(0,newpos)
        
        #now updating visual points list
        for n,a in enumerate(self.trailcoords):
            self.trailpoints[n].update_coords(a)
        
        
    def drawtrail(self, screen):
        for a in self.trailpoints:
            a.dynamic_color_draw(screen,(r.randint(0,255),r.randint(0,255),r.randint(0,255)))
    
    def erasetrail(self,screen,bg):
        for a in self.trailpoints:
            a.dynamic_color_draw(screen,bg)
        
        
        
        
class Button:
    def __init__(self, x, y, width, height, text,font,fontsize, color, hover_color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.font = pygame.font.Font(font, fontsize)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text,)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, pos):
        return self.rect.collidepoint(pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.check_hover(event.pos):
                self.action()

