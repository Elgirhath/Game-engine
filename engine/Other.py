import time

def Digits(var):
    i=0
    while var>=1:
        var/=10
        i+=1
    return i


def Read_var_from_file(file_lines, var_name):
    """
        Searches in *file_lines (list of lines read from the file with file.readlines()) for keyword *var_name
        and returns string value assigned to the *var_name after " "[Space] or "="[Equals] sign
    """
    result = ""
    for line in file_lines:
        match = True
        for i in range(0, len(var_name)):
            if line[i] != var_name[i]:
                match = False
            break
        if match == True and (line[len(var_name)]==" " or line[len(var_name)]=="="):
            for i in range(len(var_name), len(line)):
                if (ord(line[i])>=48 and ord(line[i])<=57) or (ord(line[i])>=65 and ord(line[i])<=90) or ord(line[i]) == 95 or (ord(line[i])>=97 and ord(line[i])<=122):
                    result+=line[i]
            break
    if result == "":
        print("Variable: ", var_name, " not found in file: ", file_lines.name)
    return result

_last_frames_times_ = []
global delta_time
delta_time = 0

def FPS():
    _last_frames_times_.append(time.clock())
    if len(_last_frames_times_)>30:
        _last_frames_times_.pop(0)
    
    if len(_last_frames_times_)>1:
        global delta_time
        delta_time = _last_frames_times_[len(_last_frames_times_)-1] - _last_frames_times_[len(_last_frames_times_)-2]
    
    if len(_last_frames_times_) >1:
        average = 0
        for i in range(0, len(_last_frames_times_) - 1):
            average += (_last_frames_times_[i+1] - _last_frames_times_[i])
        average = average / (len(_last_frames_times_) - 1)
        return 1/average
    else:
        return None
    
def Delta_time():
    if len(_last_frames_times_)>0:
        return _last_frames_times_[len(_last_frames_times_)-1]
    else:
        return 0