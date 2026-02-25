Web VPython 3.2
scaleHeight = 5;
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
                     pos = vector(4*j-(2*H), 4*i-(2*L), cur*scaleHeight),
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
                z00 = float(values[i][j])*scaleHeight
                z01 = float(values[i+1][j])*scaleHeight
                z11 = float(values[i+1][j+1])*scaleHeight
                z10 = float(values[i][j+1])*scaleHeight
            except:
                continue  

            v00 = vector(4*j - 2*H, 4*i - 2*L,     z00)
            v01 = vector(4*j - 2*H, 4*(i+1) - 2*L, z01)
            v11 = vector(4*(j+1) - 2*H, 4*(i+1) - 2*L, z11)
            v10 = vector(4*(j+1) - 2*H, 4*i - 2*L,    z10)
            edges = [(v00, v01), (v01, v11), (v11, v10), (v10, v00), (v00,v11)]
            
            for v_1, v_2 in edges:
                rawZ=v_1.z/scaleHeight
                curve(pos=[v_1,v_2], color = vec(rawZ-3.5,1,3.5-rawZ), radius=.1 )
                #print(v_1.z) for debugging
            # edges as headless arrows
           # arrow(pos=v00, axis=v01-v00, color=color.black, shaftwidth=0.05, headwidth=0, headlength=0)
            #arrow(pos=v01, axis=v11-v01, color=color.black, shaftwidth=0.05, headwidth=0, headlength=0)
           # arrow(pos=v11, axis=v10-v11, color=color.black, shaftwidth=0.05, headwidth=0, headlength=0)
           # arrow(pos=v10, axis=v00-v10, color=color.black, shaftwidth=0.05, headwidth=0, headlength=0)
           # arrow(pos=v00, axis=v11-v00, color=color.black, shaftwidth=0.05, headwidth=0, headlength=0)
            #arrow(pos=v01, axis=v10-v01, color=color.black, shaftwidth=0.05, headwidth=0, headlength=0) //optional diagonal, looks prettier without
            
def get_interp_pos(v1, v2, target): #contour value - https://www.youtube.com/watch?v=G-esV7tB_5s
    if abs(v1.z - v2.z) < 0.0001: return v1 
    t = (target - v1.z) / (v2.z - v1.z)
    return v1 + t * (v2 - v1)

def grid_arrows(values, tolerance=0.5): # equipotentials
    L = len(values); H = len(values[0])
    targets = [1*scaleHeight,
    2*scaleHeight,
    3*scaleHeight,
    4*scaleHeight,
    5*scaleHeight,
    6*scaleHeight,
    ]
    

    for i in range(L - 1):
        for j in range(H - 1):
            #  corner vectors using existing mapping

            p00 = vector(4*j - 2*H, 4*i - 2*L, float(values[i][j])*scaleHeight)
            p01 = vector(4*j - 2*H, 4*(i+1) - 2*L, float(values[i+1][j])*scaleHeight)
            p11 = vector(4*(j+1) - 2*H, 4*(i+1) - 2*L, float(values[i+1][j+1])*scaleHeight)
            p10 = vector(4*(j+1) - 2*H, 4*i - 2*L, float(values[i][j+1])*scaleHeight)
            
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
scene.width = 1400
scene.height = 800
#scene.userzoom = False
scene.fov= .000002
rate(20)
f = read_local_file(scene.title_anchor)
voltages = csv_parse(f)

mesh_on = [True]; ef_on = [True]; eq_on = [True];normal_on = [True]


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


tickLength = 3;
tickWidth = .3;
axisScale = 2;
origin=[-26,-22,0]
labelOffset = 5;
def set_visible(objs, state):
    for o in objs: o.visible = state
    #axis
    arrow(pos=vec(origin[0],origin[1],0), axis=vec(48,0,0), shaftwidth=tickWidth, color = color.black, headwidth=0 )
    arrow(pos=vec(origin[0],origin[1],0), axis=vec(0,40,0), shaftwidth=tickWidth, color = color.black, headwidth=0)
    arrow(pos=vec(origin[0],origin[1],0), axis=vec(0,0,6*scaleHeight), shaftwidth=tickWidth, color = color.black, headwidth=0)
    for i in range(25):
        arrow(pos=vec(origin[0] + axisScale*i,origin[1],0), axis=vec(0,-tickLength,0), shaftwidth=tickWidth, color = color.black)
    for i in range(21):
        arrow(pos=vec(origin[0],origin[1] + axisScale*i,0), axis=vec(-tickLength,0,0), shaftwidth=tickWidth, color = color.black)
        
    for i in range(7):
        arrow(pos=vec(origin[0],origin[1],i*scaleHeight), axis=vec(-tickLength,-tickLength,0), shaftwidth=tickWidth, color = vector(i-3.5,1,3.5-i))
    label(pos = vec(origin[0]-labelOffset,origin[1]-labelOffset,6*scaleHeight+2), text = '6V')
    label(pos = vec(origin[0]-labelOffset,origin[1]-labelOffset,0*scaleHeight), text = '0V')
    label(pos = vec(origin[0]-labelOffset,origin[1]+axisScale*20+labelOffset,0), text = '20cm')
    label(pos = vec(origin[0]-labelOffset,origin[1],-labelOffset), text = '0cm')
    label(pos = vec(origin[0]+axisScale*24+labelOffset,origin[1]-labelOffset,0), text = '24cm')
    label(pos = vec(origin[0],origin[1]-labelOffset,-labelOffset), text = '0cm ')
    
    label(pos = vec(origin[0]+ 20,origin[1]-labelOffset,-labelOffset), text = 'X Distance (cm)')
    label(pos = vec(origin[0]-labelOffset,origin[1]+20 ,-labelOffset), text = 'Y Distance (cm)')
    label(pos = vec(origin[0]-labelOffset,origin[1]-labelOffset,3*scaleHeight), text = 'Voltage (V)')
    
    
def toggle_mesh(b):
    mesh_on[0] = not mesh_on[0]
    b.text = 'Voltages ' + ('ON' if mesh_on[0] else 'OFF')
    set_visible(mesh_objects, mesh_on[0])

def toggle_ef(b):
    ef_on[0] = not ef_on[0]
    b.text = 'E-Field ' + ('ON' if ef_on[0] else 'OFF')
    set_visible(ef_objects, ef_on[0])

def toggle_eq(b):
    eq_on[0] = not eq_on[0]
    b.text = 'Equipotential ' + ('ON' if eq_on[0] else 'OFF')
    set_visible(eq_objects, eq_on[0])
def toggle_xy(b):
    scene.forward = vector(0, 0, -1)
def toggle_yz(b):
    scene.forward = vector(-1, 0, 0)
def toggle_xz(b):
    scene.forward = vector(0,1, 0)
    

button(text='Mesh ON',    bind=toggle_mesh)
button(text='E-Field ON', bind=toggle_ef)
button(text='Equip ON',   bind=toggle_eq)
button(text='View xy plane',   bind=toggle_xy)
button(text='View yz plane',   bind=toggle_yz)
button(text='View xz plane',   bind=toggle_xz)

set_visible(ef_objects, ef_on[0])
#print(scene.forward)
#print(scene.camera.pos)
#print(scene.center)
print("hold shift and left mouse click to pan")

scene.userpan = True
scene.ambient = vec(0.5, 0.5, 0.5);
scene.up = vector(-.001,0,1)