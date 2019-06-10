class Rigidbody():
    def __init__(self, parent, velocity = (0,0,0), use_gravity = True):
        self.parent = parent
        self.velocity = (0,0,0)
        self.use_gravity = use_gravity
        self.time_in_air = 0
        
    def Move(self, vector):
        import Mesh
        from Vector import Vector
        last_pos = self.parent.transform.position
        
        self.parent.transform.position = Vector.Add(self.parent.transform.position, vector)
        
        if 'collider' in dir(self.parent) and self.parent.collider:
            for obj in Mesh.objects:
#                if Vector.Distance(obj.transform.position, self.parent.transform.position)>2:
#                    continue
                if obj != self.parent:
                    if self.parent.collider.Collide(obj.collider):
                        self.parent.transform.position = last_pos
                        return
            
        self.parent.transform._update_mesh_()
        
        if 'camera' in dir(self.parent):
            self.parent.camera.pyramid.Update()
            
    def Apply(self):
        from Vector import Vector
        import Other
        self.Move(Vector.Scale(self.velocity, Other.delta_time))
        
    def Dist_from_ground(self):
        from Vector import Vector
        from Ray import Ray
        ray = Ray(Vector.Local_to_world_space(self.parent.collider.center, self.parent.transform), (0,0,-1))
        if ray.Collide(self.parent).point and ray.Collide().point:
            dist_vector = Vector.Difference(ray.Collide().point, ray.Collide(self.parent).point)
            return Vector.Magnitude(dist_vector)
        else:
            return None
    
def Gravity():
    import Mesh
    from Vector import Vector
    import Other
    for obj in Mesh.objects:
        if obj.rigidbody:
            if obj.rigidbody.use_gravity:
                height = obj.rigidbody.Dist_from_ground()
                if not height or height>0.05:
                    obj.rigidbody.time_in_air += Other.delta_time
                    obj.rigidbody.velocity = Vector.Add(obj.rigidbody.velocity, Vector.Scale(g_acc, obj.rigidbody.time_in_air))
                    if height!= None and obj.rigidbody.velocity[2] < 0 and obj.rigidbody.velocity[2]*Other.delta_time < -height:
                        obj.rigidbody.velocity = (obj.rigidbody.velocity[0], obj.rigidbody.velocity[1], -height/(2*Other.delta_time))
                else:
                    obj.rigidbody.time_in_air = 0
                    if obj.rigidbody.velocity[2] < 0:
                        obj.rigidbody.velocity = (obj.rigidbody.velocity[0], obj.rigidbody.velocity[1], 0)
            obj.rigidbody.Apply()
        
g_acc = (0,0,-1)