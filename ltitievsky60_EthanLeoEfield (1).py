from vpython import *
#Web VPython 3.2

def csv_parse(fd):
    items = []
    text = fd.text
    for line in iter(text.splitlines()):
        if len(line.strip()) > 1 :
            items.append(line.strip().split(','))
    return items
            
        
def grid(values):
    L = len(values)
    H = len(values[1])
    for i in range(L):
        for j in range(H):
            box(
                length = 4, 
                height = 4, 
                pos = vector(4*j-(2*H), 4*i-(2*L), int(values[i][j])), 
                color = vec((1/6)*int(values[i][j]),0,0)
                )

    
f = read_local_file(scene.title_anchor)
voltages = csv_parse(f)

grid(voltages)

 