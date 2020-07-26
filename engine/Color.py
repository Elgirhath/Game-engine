white = (255,255,255)
black = (0,0,0)
grey = (127,127,127)
dark_grey = (80,80,80)
very_dark_grey = (40,40,40)
red = (255,0,0)
dark_red = (102, 0, 0)
lime = (0,255,0)
blue = (0,0,255)
yellow = (255,255, 0)
dark_green = (0,102,0)
sky = (102, 178, 255)
saddle_brown = 	(139,69,19)
orange = (255,128,0)

class Material():
    def __init__ (self, color):
        self.color = color
        
default_material = Material((0.8*255, 0.8*255, 0.8*255))