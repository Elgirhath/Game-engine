import sys

import pygame
from lib import pyinit
from lib import Other
from lib.Vector import Vector
from lib import Screen
from lib import Color
from lib import Input
from lib.Quaternion import Quaternion
from lib import Mesh
import random
from lib import Importer
from lib import Collider
from lib import Rigidbody
from lib.Ray import Ray

player = Mesh.Object((0,0,0.9))
cam = Screen.Camera((0,0,0.9), resolution = (1366,768))
player.Add_camera(cam)
player.collider = Collider.Box_collider(player, (0, 0, 0), (0.1, 0.1, 0.85))

pygame.mixer.pre_init(44100, -16, 1, 512)
pyinit.init(Screen.main_camera.resolution, "The game", "window")
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)
game_exit=False;


"""**********************************************************************************
**********************************************************************************
***********************************MAIN*******************************************
**********************************************************************************
**********************************************************************************"""


walk_speed = 1.5
run_speed = 3
crouch_speed = 0.8
crouching = False

mouse_sensivity = 0.15

cam.pyramid.Update()

#test1 = Importer.Import_obj("test1.obj", (0,0,0))
#test2 = Importer.Import_obj("test2.obj", (0,0,0))

room = Importer.Import_obj("Room.obj", (0,0,0))
room.Set_material(Color.Material(Color.grey))
room.collider = None
room.rigidbody = None
room.mesh.faces[0].material = Color.Material(Color.white)
room.mesh.faces[1].material = Color.Material(Color.white)

room.mesh.faces[2].material = Color.Material(Color.grey)
room.mesh.faces[3].material = Color.Material(Color.grey)
room.mesh.faces[4].material = Color.Material(Color.grey)

room.mesh.faces[5].material = Color.Material(Color.dark_grey)
room.mesh.faces[6].material = Color.Material(Color.dark_grey)
room.mesh.faces[7].material = Color.Material(Color.dark_grey)
room.mesh.faces[8].material = Color.Material(Color.dark_grey)
        
for i in range(0, len(Mesh.all_faces)):
    if Mesh.all_faces[i] == room.mesh.faces[7]:
        Mesh.all_faces.pop(i)
        Mesh.all_faces.insert(0, room.mesh.faces[7])
        
floor_collider = Mesh.Object((0,0,0))
floor_collider.rigidbody = None
#floor_collider.rigidbody.use_gravity = False
floor_collider.collider = Collider.Box_collider(floor_collider, (0, 0, -100), (100, 100, 100))

range_collider = Mesh.Object((0,14,0))
range_collider.rigidbody = None
#range_collider.rigidbody.use_gravity = False
range_collider.collider = Collider.Box_collider(range_collider, (0, 0, 0), (100, 10, 100))

backwall_collider = Mesh.Object((0,-11,0))
backwall_collider.rigidbody = None
#backwall_collider.rigidbody.use_gravity = False
backwall_collider.collider = Collider.Box_collider(backwall_collider, (0, 0, 0), (100, 10, 100))

leftwall_collider = Mesh.Object((-20,0,0))
leftwall_collider.rigidbody = None
#leftwall_collider.rigidbody.use_gravity = False
leftwall_collider.collider = Collider.Box_collider(leftwall_collider, (0, 0, 0), (10, 100, 100))

rightwall_collider = Mesh.Object((25,0,0))
rightwall_collider.rigidbody = None
#rightwall_collider.rigidbody.use_gravity = False
rightwall_collider.collider = Collider.Box_collider(rightwall_collider, (0, 0, 0), (10, 100, 100))



all_targets = []

class Target():
    def __init__ (self, obj):
        self.obj = obj
        obj.parent = self
        self.dir = None
        self.sleeping = False
        self.sleep_const = 2
        self.sleep_time = self.sleep_const
        self.speed = 3
        self.obj.mesh.faces[0].material = Color.Material(Color.white)
        self.obj.mesh.faces[1].material = Color.Material(Color.black)
        self.obj.mesh.faces[2].material = Color.Material(Color.red)
        self.obj.mesh.faces[3].material = Color.Material(Color.black)
        all_targets.append(self)
        
    
    def Reset(self):
        self.obj.mesh.faces[0].material = Color.Material(Color.white)
        self.obj.mesh.faces[1].material = Color.Material(Color.black)
        self.obj.mesh.faces[2].material = Color.Material(Color.red)
        self.obj.mesh.faces[3].material = Color.Material(Color.black)
    
    def Kill(self):
        self.obj.mesh.faces[0].material = Color.Material(Color.very_dark_grey)
        self.obj.mesh.faces[1].material = Color.Material(Color.black)
        self.obj.mesh.faces[2].material = Color.Material(Color.dark_red)
        self.obj.mesh.faces[3].material = Color.Material(Color.black)
        
target1 = Target(Importer.Import_obj("Target.obj", (0,17,0)))
target1.obj.rigidbody = None

target2 = Target(Importer.Import_obj("Target.obj", (3,14,0)))
target2.obj.rigidbody = None

target3 = Target(Importer.Import_obj("Target.obj", (-5,11,0)))
target3.obj.rigidbody = None

target4 = Target(Importer.Import_obj("Target.obj", (7,8,0)))
target4.obj.rigidbody = None

def Reset_targets():
    for target in all_targets:
        target.Reset()
        target.sleeping = False

barier = Importer.Import_obj("Barier.obj", (0,0,0))
barier.rigidbody = None
barier.collider = None
barier.mesh.faces[0].material = Color.Material(Color.very_dark_grey)
barier.mesh.faces[1].material = Color.Material(Color.dark_grey)

button1 = Importer.Import_obj("Button1.obj", (0,-1, 1.3))
button1.rigidbody = None
button1.collider = None
button1.Set_material(Color.Material(Color.white))

button2 = Importer.Import_obj("Button2.obj", (0,-1, 1.3))
button2.rigidbody = None
button2.collider = None
button2.mesh.faces[0].material = Color.Material(Color.lime)
button2.mesh.faces[1].material = Color.Material(Color.dark_green)
button2.mesh.faces[2].material = Color.Material(Color.dark_green)
button2.mesh.faces[3].material = Color.Material(Color.dark_green)
button2.mesh.faces[4].material = Color.Material(Color.dark_green)

button3 = Importer.Import_obj("Button1.obj", (2,-1, 1.3))
button3.rigidbody = None
button3.collider = None
button3.Set_material(Color.Material(Color.white))

button4 = Importer.Import_obj("Button2.obj", (2,-1, 1.3))
button4.rigidbody = None
button4.collider = None
button4.mesh.faces[0].material = Color.Material(Color.red)
button4.mesh.faces[1].material = Color.Material(Color.dark_red)
button4.mesh.faces[2].material = Color.Material(Color.dark_red)
button4.mesh.faces[3].material = Color.Material(Color.dark_red)
button4.mesh.faces[4].material = Color.Material(Color.dark_red)

box = Importer.Import_obj("Box.obj", (0,0,0))
box.rigidbody = None
box.mesh.faces[0].material = Color.Material((101, 55, 38))
box.mesh.faces[1].material = Color.Material((114, 62, 44))
box.mesh.faces[2].material = Color.Material((134, 73, 51))

guns = Importer.Import_obj("Guns.obj", (-6,0,0.8))
guns.rigidbody = None
guns.collider = None
guns.Set_material(Color.Material(Color.black))

class Gun():
    recoil_timer = 0
    recoil = False
    post_recoil = False
    recoil_time = 0.05
    post_recoil_time = 1
    image = pygame.image.load("ui/gun.png").convert_alpha()
    gun_size = image.get_rect().size
    img_ratio = gun_size[0]/gun_size[1]
    image = pygame.transform.scale(image, (int(0.8*cam.resolution[1]*img_ratio), int(0.8*cam.resolution[1])))
    magazine_size = 10
    current_ammo = 10
    bullet_icon = pygame.image.load("ui/bullet_icon.png").convert_alpha()
    bullet_size = bullet_icon.get_rect().size
    bullet_icon = pygame.transform.scale(bullet_icon, (int(Vector.Scale(bullet_size, 0.1)[0]), int(Vector.Scale(bullet_size, 0.1)[1])))
    bullet_size = (int(Vector.Scale(bullet_size, 0.1)[0]), int(Vector.Scale(bullet_size, 0.1)[1]))
    bullet_icon_empty = pygame.image.load("ui/bullet_icon_empty.png").convert_alpha()
    bullet_size_empty = bullet_icon_empty.get_rect().size
    bullet_icon_empty = pygame.transform.scale(bullet_icon_empty, (int(Vector.Scale(bullet_size_empty, 0.1)[0]), int(Vector.Scale(bullet_size_empty, 0.1)[1])))
    bullet_size_empty = (int(Vector.Scale(bullet_size_empty, 0.1)[0]), int(Vector.Scale(bullet_size_empty, 0.1)[1]))
    
    def Ammo_rect():
        rect_size = (int(cam.resolution[0]*0.4), int(cam.resolution[1]*0.15))
        rect = pygame.Surface(rect_size)
        rect.set_alpha(128)
        rect.fill(Color.black)
        rect_pos = Vector.Difference(cam.resolution, rect_size)
        horiz_space = int((rect_size[0])/(Gun.magazine_size+1)*0.7)
        vert_pos = rect_size[1]/2 - Gun.bullet_size[1]/2
        ammo = Gun.current_ammo
        for i in range(horiz_space - int(Gun.bullet_size[0]/2), 11*horiz_space - int(Gun.bullet_size[0]/2), horiz_space):
            if ammo>0:
                rect.blit(Gun.bullet_icon, (i, vert_pos))
            else:
                rect.blit(Gun.bullet_icon_empty, (i, vert_pos))
            ammo-=1
            
        text_size = 60
        text = str(Gun.current_ammo)
        font = pygame.font.SysFont("Times New Roman", text_size)
        font.set_bold(0)
        text_pos = (int(rect_size[0]*0.85 - font.size(text)[0]/2), int(rect_size[1]/2 - font.size(text)[1]/2))
        label = font.render(text, 1, Color.white)
        rect.blit(label, text_pos)
        
        pyinit.game_display.blit(rect, rect_pos)
        

training = False
start_training = False
training_init = 5
training_timer = training_init
countdown = 30
current_countdown = countdown
target_count = 0
show_score = False
score_time = 4
score_timer = score_time

step_timer = 0
walk_step_time = 0.5
run_step_time = 0.3


shot_sound = pygame.mixer.Sound("sounds/shot.wav")
empty_sound = pygame.mixer.Sound("sounds/empty_gun.wav")
step_channel = pygame.mixer.Channel(3)
footstep = pygame.mixer.Sound("sounds/footstep.wav")
footstep.set_volume(0.13)
beep_channel = pygame.mixer.Channel(4)
beep = pygame.mixer.Sound("sounds/beep.wav")
target_channel = pygame.mixer.Channel(2)
target_sound = pygame.mixer.Sound("sounds/targets_moving.wav")
reload_sound = pygame.mixer.Sound("sounds/reload.wav")


while not game_exit:
    pyinit.game_display.fill(Color.black)
    mouse_move = (0,0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_exit = True
        if event.type == pygame.MOUSEMOTION:
            mouse_move = event.rel

    
    if pyinit.display_mode == "window" and Vector.Magnitude(mouse_move)<2:
        mouse_move = (0,0)
            
    cam.transform.Rotate(mouse_sensivity*mouse_move[1], cam.transform.left)
    cam.transform.Rotate(mouse_sensivity*mouse_move[0], (0, 0, -1))
    
    player_move = Vector.Normalize((Input.Get_axis('horizontal'), Input.Get_axis('vertical')))

    if Input.Get_key_down("lctrl"):
        if crouching:
            cam.transform.Translate((0,0,0.9))
            crouching = False
        else:
            cam.transform.Translate((0,0,-0.9))
            crouching = True

    if Input.Get_key("lshift"):
        if crouching:
            crouching = False
            cam.transform.Translate((0,0,0.9))
        move_speed = run_speed
    elif not crouching:
        move_speed = walk_speed
    else:
        move_speed = crouch_speed

    right_move_vec = Vector.Scale(cam.transform.right, player_move[0])
    forward_move_vec = Vector.Scale(cam.transform.forward, player_move[1])
    move_vec = (Vector.Add(right_move_vec, forward_move_vec)[0], Vector.Add(right_move_vec, forward_move_vec)[1], 0)
    move_vec = Vector.Normalize(move_vec)
    move_vec = Vector.Scale(move_vec, move_speed)
    
    player.rigidbody.Move(Vector.Scale(move_vec, Other.delta_time))
    
    if Vector.Magnitude(move_vec)>0 and step_timer<=0:
        if player.rigidbody.Dist_from_ground() and player.rigidbody.Dist_from_ground() <=0.05:
            if move_speed == walk_speed:
                step_channel.play(footstep)
                step_timer = walk_step_time
            elif move_speed == run_speed:
                step_channel.play(footstep)
                step_timer = run_step_time
    
    if step_timer>0:
        step_timer -= Other.delta_time

    if Input.Get_key_down('escape'):
        game_exit = True
        
    if Input.Get_key_down('space') and player.rigidbody.Dist_from_ground() and player.rigidbody.Dist_from_ground() <= 0.05:
        if crouching:
            crouching = False
            cam.transform.Translate((0,0,0.9))
        player.rigidbody.velocity = Vector.Add(player.rigidbody.velocity, (0,0,3))
        
    if Input.Mouse_button_down(0):
        if Gun.current_ammo>0:
            shot_sound.play()
            aim_ray = Screen.Ray_on_pixel(cam.middle_pixel)
            obj = aim_ray.Collide(ignore = [player, range_collider]).other
            if obj:
                if obj.parent.name == "Target":
                    obj.parent.parent.Kill()
                    obj.parent.parent.sleeping = True
                    if training:
                        target_count+=1
    
            Gun.recoil = True
            Gun.current_ammo-=1
        else:
            empty_sound.play()

    if Gun.recoil:
        cam.transform.Rotate(4*Other.delta_time/Gun.recoil_time, cam.transform.right)
        Gun.recoil_timer += Other.delta_time
        if Gun.recoil_timer > Gun.recoil_time:
            Gun.recoil_timer = 0
            Gun.recoil = False
            Gun.post_recoil = True
            
    if Gun.post_recoil:
        cam.transform.Rotate(-5*Other.delta_time/Gun.post_recoil_time, cam.transform.right)
        Gun.recoil_timer += Other.delta_time
        if Gun.recoil_timer > Gun.post_recoil_time:
            Gun.recoil_timer = 0
            Gun.post_recoil = False
            
    if training:
        current_countdown -= Other.delta_time
        if current_countdown <= 0:
            training = False
            show_score = True
            score_timer = score_time
            Reset_targets()
        for target in all_targets:
            if target.dir:
                target.obj.transform.Translate(Vector.Scale(target.dir, Other.delta_time))
                if target.obj.transform.position[0]>9:
                    target.dir = (-target.speed, 0, 0)
                if target.obj.transform.position[0]<-9:
                    target.dir = (target.speed, 0, 0)
            else:
                rand = random.randint(0,1)
                if rand == 0:
                    rand = 1
                target.dir = (rand*target.speed, 0, 0)
            if target.sleeping:
                target.sleep_time -= Other.delta_time
                if target.sleep_time < 0:
                    target.Reset()
                    target.sleep_time = target.sleep_const
                    target.sleeping = False
                    
            
    Rigidbody.Gravity()
    Screen.Render()
    if cam.resolution == (800, 600):
        pyinit.game_display.blit(Gun.image, (15,185))
        
    elif cam.resolution == (1366, 768):
        pyinit.game_display.blit(Gun.image, (190,238))
        
    if show_score:
        score_timer -= Other.delta_time
        if score_timer < 0:
            show_score = False
        font = pygame.font.SysFont("Arial", 20)
        text = "Trafiłeś " + str(target_count) + " tarcz!"
        Screen._write_(text, 20, (int(cam.resolution[0]*0.5) - int(font.size(text)[0]/2), int(cam.resolution[1]*(0.3))), 2, Color.orange)

    if Vector.Distance(player.transform.position, button1.transform.position) < 1:
        font = pygame.font.SysFont("Arial", 20)
        text = "Wciśnij E, aby zresetować tarcze"
        Screen._write_(text, 20, (int(cam.resolution[0]*0.5) - int(font.size(text)[0]/2), int(cam.resolution[1]*(0.7))), 2, Color.orange)
        if Input.Get_key_down("e"):
            Reset_targets()
            

    if Vector.Distance(player.transform.position, button3.transform.position) < 1:
        if not training:
            font = pygame.font.SysFont("Arial", 20)
            text = "Wciśnij E, aby rozpocząć trening"
            Screen._write_(text, 20, (int(cam.resolution[0]*0.5) - int(font.size(text)[0]/2), int(cam.resolution[1]*(0.7))), 2, Color.orange)
            if Input.Get_key_down("e"):
                start_training = True
                Reset_targets()
                
        else:
            font = pygame.font.SysFont("Arial", 20)
            text = "Wciśnij E, aby zatrzymać trening"
            Screen._write_(text, 20, (int(cam.resolution[0]*0.5) - int(font.size(text)[0]/2), int(cam.resolution[1]*(0.7))), 2, Color.orange)
            if Input.Get_key_down("e"):
                target_sound.stop()
                training = False

    if Vector.Distance(player.transform.position, guns.transform.position) < 2 and Gun.current_ammo<Gun.magazine_size:
        font = pygame.font.SysFont("Arial", 20)
        text = "Wciśnij R, aby uzupełnić amunicję"
        Screen._write_(text, 20, (int(cam.resolution[0]*0.5) - int(font.size(text)[0]/2), int(cam.resolution[1]*(0.7))), 2, Color.orange)
        if Input.Get_key_down("r"):
            Gun.current_ammo = Gun.magazine_size
            reload_sound.play()
                
    if start_training:
        font = pygame.font.SysFont("Arial", 30)
        if training_timer>3:
            text = "Traf jak najwiecej tarcz w 30 sekund!"
        else:
            text = str(int(training_timer)+1)
        Screen._write_(text, 30, (int(cam.resolution[0]*0.5) - int(font.size(text)[0]/2), int(cam.resolution[1]*(0.5))), 2, Color.orange)
    
    if start_training:
        if int(training_timer) < 4 and  int(training_timer) > int(training_timer - Other.delta_time):
             beep_channel.play(beep)
        training_timer -= Other.delta_time
        
    if training_timer<0:
        training_timer = training_init
        start_training = False
        target_channel.play(target_sound, -1)
        training = True
        current_countdown = countdown
        target_count = 0
        Reset_targets()
        
    if training:
        font = pygame.font.SysFont("Arial", 15)
        text = "Czas: " + str(int(current_countdown))
        Screen._write_(text, 20, (int(cam.resolution[0]*0.03) - int(font.size(text)[0]/2), int(cam.resolution[1]*(0.1))), 2, Color.orange)
        
        font = pygame.font.SysFont("Arial", 15)
        text = "Trafione: " + str(target_count)
        Screen._write_(text, 20, (int(cam.resolution[0]*0.9) - int(font.size(text)[0]/2), int(cam.resolution[1]*(0.1))), 2, Color.orange)

        
    pygame.draw.circle(pyinit.game_display, Color.red, (cam.middle_pixel), int(0.003*cam.resolution[0]))
    Gun.Ammo_rect()
    Other.FPS()
    
    pygame.display.update()
    
pygame.quit()
#quit()