def Z_Update():
    import time
    from lib.Ray import Ray
    from lib import Mesh
    if len(Mesh.all_faces)<1:
        return
    for i in range(650, 651):
        for j in range(384, 385):
            start = time.clock()
#            ray_rotation_pixels = Vector.Difference((i, j), middle)
#            
#            ray_direction = main_camera.transform.forward
#            rotation_x_angle = ray_rotation_pixels[0]*main_camera.FOV/main_camera.resolution[0]
#            ray_direction = Vector.Rotate(ray_direction, main_camera.transform.up, rotation_x_angle)
#            
#            rotation_y_axis = Vector.Cross_product(ray_direction, main_camera.transform.up)
#            rotation_y_angle = ray_rotation_pixels[1]*main_camera.FOV_vertical/main_camera.resolution[1]
#            ray_direction = Vector.Rotate(ray_direction, rotation_y_axis, rotation_y_angle)
#            
#            ray = Ray(main_camera.transform.position, ray_direction)
#            for face in Mesh.all_faces:
#                if (ray.Intersect_point(face.plane())):
#                    point = ray.Intersect_point(face.plane())
#                    if (Vector.Dot_product(Vector.Difference(point, main_camera.transform.position), ray_direction)<=0):
#                        continue
#                    elif Geometry.Point_in_triangle(point, face.vertex):
#                        if z_buffer[i][j]:
#                            if Vector.Magnitude(Vector.Difference(point, main_camera.transform.position))<z_buffer[i][j]:
#                                z_buffer[i][j] = Vector.Magnitude(Vector.Difference(point, main_camera.transform.position))
#                        else:
#                            z_buffer[i][j] = Vector.Magnitude(Vector.Difference(point, main_camera.transform.position))
            start = time.clock() - start
            print(start)
                            
def Draw_z_buffer(plane):
    for i in range(0, Camera.resolution[0]):
        for j in range(0, Camera.resolution[1]):
            color = (255,0,0)
            if (z_buffer[i][j]):
                color = Vector.Scale((50,50,50), z_buffer[i][j])
                if color[0]>255:
                    color = (255, color[1], color[2])
                if color[1]>255:
                    color = (color[0], 255, color[2])
                if color[2]>255:
                    color = (color[0], color[1], 255)
                
            plane.set_at((i, j), color)
            
            
""" from lib.Screen.Draw() """
    if type(obj) is BasicStructures.Edge:
        local_origin_pos = Vector.World_to_local_space(obj.A, main_camera.transform)
        local_end_pos = Vector.World_to_local_space(obj.B, main_camera.transform)
#        if local_origin_pos[0]<Camera.clip_min and local_end_pos[0]<Camera.clip_min:
#            return
#        if local_origin_pos[0]<Camera.clip_min and  local_end_pos[0]>=Camera.clip_min:
#            scalar = (Camera.clip_min - local_end_pos[0])/Vector.Difference(local_origin_pos, local_end_pos)[0]
#            local_origin_pos = Vector.Homothety(local_origin_pos, local_end_pos, scalar)
#        if local_origin_pos[0]>=Camera.clip_min and  local_end_pos[0]<Camera.clip_min:
#            scalar = (Camera.clip_min - local_origin_pos[0])/Vector.Difference(local_end_pos, local_origin_pos)[0]
#            local_end_pos = Vector.Homothety(local_end_pos, local_origin_pos, scalar)