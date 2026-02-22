from vpython import *
#Web VPython 3.2

def csv_parse(fd):
    items = []
    text = fd.text
    for line in iter(text.splitlines()):
        if len(line.strip()) > 1 :
            items.append(line.strip().split(','))
    return items
            
        
def eField(values):
    items = []
    L = len(values)
    H = len(values[1])
    for i in range(L):
        for j in range(H):


            ihat = 0.0
            jhat = 0.0
            cur = float(values[i][j])
            v = 0.0
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
                    
                
    
f = read_local_file(scene.title_anchor)
voltages = csv_parse(f)

eField(voltages)


