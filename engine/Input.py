import pygame

class axis():
    def __init__(self, positive, negative):
        self.positive = positive
        self.negative = negative

def Get_axis(axis_name):
    if not axis_name in globals():
        print("There is no axis named: ", axis_name)
        return
    else:
        axis = eval(axis_name)
        if Get_key(axis.negative):
            if Get_key(axis.positive):
                return 0
            else:
                return -1
        elif Get_key(axis.positive):
            return 1
        else:
            return 0

def Get_key(key_name):
    if len(key_name)==1:
        key_name = key_name.lower()
    else:
        key_name = key_name.upper()
    
    if pygame.key.get_pressed()[eval("pygame.K_" + key_name)]:
        return 1
    return 0

def Get_key_down(key_name):
    current_value = Get_key(key_name)
    if not key_name in _keys_down_:
        _keys_down_[key_name] = current_value
        return 0
    else:
        if _keys_down_[key_name] == 0:
            _keys_down_[key_name] = current_value
            return current_value
        else:
            _keys_down_[key_name] = current_value
            return 0
        
def Get_key_up(key_name):
    current_value = Get_key(key_name)
    if not key_name in _keys_down_:
        _keys_down_[key_name] = current_value
        return 0
    else:
        if _keys_down_[key_name] == 1:
            _keys_down_[key_name] = current_value
            if current_value == 0:
                return 1
            else:
                return 0
        else:
            _keys_down_[key_name] = current_value
            return 0
    
    
def Get_button(button_name):
    if pygame.key.get_pressed()[eval("pygame.K_" + buttons[button_name])]:
        return 1
    return 0

def Get_button_down(button_name):
    return Get_key_down(buttons[button_name])

def Get_button_up(button_name):
    return Get_key_up(buttons[button_name])

def Mouse_button(button_number):
    if pygame.mouse.get_pressed()[button_number]:
        return 1
    
def Mouse_button_down(button_number):
    current_value = Mouse_button(button_number)
    if not str(button_number) in _keys_down_:
        _keys_down_[str(button_number)] = current_value
    else:
        if not _keys_down_[str(button_number)]:
            _keys_down_[str(button_number)] = current_value
            return current_value
        else:
            _keys_down_[str(button_number)] = current_value
            return 0

horizontal = axis('d', 'a')
vertical = axis('w', 's')

buttons = {'Jump': 'SPACE', 'Grab': 'e'}
_keys_down_ = {'Default': 'NULL'}
