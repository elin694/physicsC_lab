from vpython import *
#Web VPython 3.2


def csv_parse(fd):
    items = []
    text = fd.text
    for line in iter(text.splitlines()):
        if len(line.strip()) > 1 :
            items.append(line.strip().split(','))
    return items
            
        
def eField(values): #efield
    items = []
    L = len(values)
    H = len(values[1])
    for i in range(L):
        for j in range(H):


            ihat = 0.0
            jhat = 0.0
            cur = float(values[i][j])
            v = 0.0
            
            #fwd/back pass diff, depending on availability
            if(i-1 > 0):
                v=float(values[i-1][j])
                jhat -= (v - cur)/(.02)# up
            if(i+1 < L):
                v=float(values[i+1][j])
                jhat -= ((v - cur)/(-0.02))# down
            if(j-1 > 0):
                v=float(values[i][j-1])
                ihat -= (v - cur)/(-0.02)# left
            if(j+1 < H):
                v=float(values[i][j+1])
                ihat -= (v - cur)/(.02)# right
                
                m = (ihat ** 2 + jhat ** 2) ** .5
                tuning = 1.5
                ihat *= tuning
                jhat *= tuning
            arrow(
                     pos = vector(4*j-(2*H), 4*i-(2*L), cur),
                     color = vec(1/6 * m ,0,0),
                     axis = vec(ihat/m, jhat/m, 0),
                     opacity = .01 * m
                    )


def grid(values): # mesh potentials. vPython triangles/quads are such a nightmare to work with
    L = len(values)
    H = len(values[0])

    for i in range(L - 1):
        for j in range(H - 1):

            try: #would have saved time earlier
                z00 = float(values[i][j])
                z01 = float(values[i+1][j])
                z11 = float(values[i+1][j+1])
                z10 = float(values[i][j+1])
            except:
                continue  

            v00 = vector(4*j - 2*H, 4*i - 2*L,     z00)
            v01 = vector(4*j - 2*H, 4*(i+1) - 2*L, z01)
            v11 = vector(4*(j+1) - 2*H, 4*(i+1) - 2*L, z11)
            v10 = vector(4*(j+1) - 2*H, 4*i - 2*L,    z10)

            # edges as headless arrows
            arrow(pos=v00, axis=v01-v00, color=color.black, shaftwidth=0.05, headwidth=0, headlength=0)
            arrow(pos=v01, axis=v11-v01, color=color.black, shaftwidth=0.05, headwidth=0, headlength=0)
            arrow(pos=v11, axis=v10-v11, color=color.black, shaftwidth=0.05, headwidth=0, headlength=0)
            arrow(pos=v10, axis=v00-v10, color=color.black, shaftwidth=0.05, headwidth=0, headlength=0)
            arrow(pos=v00, axis=v11-v00, color=color.black, shaftwidth=0.05, headwidth=0, headlength=0)
            #arrow(pos=v01, axis=v10-v01, color=color.black, shaftwidth=0.05, headwidth=0, headlength=0) //optional diagonal, looks prettier without
            
def get_interp_pos(v1, v2, target): #contour value - https://www.youtube.com/watch?v=G-esV7tB_5s
    if abs(v1.z - v2.z) < 0.0001: return v1 
    t = (target - v1.z) / (v2.z - v1.z)
    return v1 + t * (v2 - v1)

def grid_arrows(values, tolerance=0.5): # equipotentials
    L = len(values); H = len(values[0])
    targets = range(0, 6) 

    for i in range(L - 1):
        for j in range(H - 1):
            #  corner vectors using existing mapping

            p00 = vector(4*j - 2*H, 4*i - 2*L, float(values[i][j]))
            p01 = vector(4*j - 2*H, 4*(i+1) - 2*L, float(values[i+1][j]))
            p11 = vector(4*(j+1) - 2*H, 4*(i+1) - 2*L, float(values[i+1][j+1]))
            p10 = vector(4*(j+1) - 2*H, 4*i - 2*L, float(values[i][j+1]))
            
            edges = [(p00, p01), (p01, p11), (p11, p10), (p10, p00)]
            
            for t_val in targets:
                pts = []
                for v1, v2 in edges:
                    #target potential lies on this edge?
                    if (v1.z <= t_val < v2.z) or (v2.z <= t_val < v1.z):
                        pts.append(get_interp_pos(v1, v2, t_val))

                if len(pts) == 2:
                    #connect
                    curve(pos=[pts[0], pts[1]], color=color.red, radius=0.05)

scene.background = color.white
f = read_local_file(scene.title_anchor)
voltages = csv_parse(f)

mesh_on = [True]; ef_on = [True]; eq_on = [True]

def capture(before):
    return [o for o in scene.objects if o not in before]

before = list(scene.objects)
grid_arrows(voltages)
eq_objects = capture(before)

before = list(scene.objects)
eField(voltages)
ef_objects = capture(before)

before = list(scene.objects)
grid(voltages)
mesh_objects = capture(before)

def set_visible(objs, state):
    for o in objs: o.visible = state

def toggle_mesh(b):
    mesh_on[0] = not mesh_on[0]
    b.text = 'Mesh ' + ('ON' if mesh_on[0] else 'OFF')
    set_visible(mesh_objects, mesh_on[0])

def toggle_ef(b):
    ef_on[0] = not ef_on[0]
    b.text = 'E-Field ' + ('ON' if ef_on[0] else 'OFF')
    set_visible(ef_objects, ef_on[0])

def toggle_eq(b):
    eq_on[0] = not eq_on[0]
    b.text = 'Equip ' + ('ON' if eq_on[0] else 'OFF')
    set_visible(eq_objects, eq_on[0])

button(text='Mesh ON',    bind=toggle_mesh)
button(text='E-Field ON', bind=toggle_ef)
button(text='Equip ON',   bind=toggle_eq)