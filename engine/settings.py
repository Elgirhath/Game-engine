from engine.Other import Read_var_from_file
config = open("engine/Config.txt", "r").readlines()

threshold = int(Read_var_from_file(config, "THRESHOLD"))
round_digits = int(Read_var_from_file(config, "ROUND"))

del config[:]