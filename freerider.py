import math as m
import matplotlib.pyplot as plt
from enum import Enum

class PowerupType(Enum):
    
    STAR = "T"
    BOOST = "B"
    GRAVITY = "G"
    SLOW_MOTION = "S"
    BOMB = "O"
    CHECKPOINT = "C"
    ANTIGRAVITY = "A"
    WARP = "W"

class Powerup:
    
    def __init__(self,type,x,y,angle=0,x2=0,y2=0):
        self.type = type
        self.x , self.y = x,y
        self.angle = angle
        self.x2 , self.y2 = x2,y2
    
    def to_string(self):
        s = self.type.value + " " + translate(self.x) + " " + translate(-self.y)
        if self.type == PowerupType.BOOST or self.type == PowerupType.GRAVITY:
            s += " " + translate(self.angle)
        if self.type == PowerupType.WARP:
            s += " " + translate(self.x2) + " " + translate(-self.y2)
        return s
    
    def plot(self):
        X = [self.x-10,self.x+10,self.x+10,self.x-10,self.x-10]
        Y = [self.y-10,self.y-10,self.y+10,self.y+10,self.y-10]
        plt.plot(X,Y,color="green")
        plt.text(self.x,self.y,self.type.value,color="green")
    
    def shift(self,dx,dy):
        self.x += dx
        self.x2 += dx
        self.y += dy
        self.y2 += dy


def distance(x1,y1,x2,y2):
    return m.sqrt((x2-x1)**2 + (y2-y1)**2)

def translate(n):
    
    n = round(n)
    
    def aux(n):
        if n<10:
            return str(n)
        elif n < 32:
            return chr(97+n-10)
        else:
            print(n)
            return "AAAAAAAAAA"
    
    s = ""
    q = abs(n)
    r = 0
    while q >= 32:
        q,r = q // 32, q % 32
        s = aux(r)+s
    s = aux(q)+s
    if n < 0:
        s = "-" + s
    return s

def translate_back(x):
    
    def aux(symbol):
        try:
            return int(symbol)
        except ValueError:
            return ord(symbol)-97+10
    
    positive = True
    if x[0] == "-":
        positive = not(positive)
        x = x[1:]
    
    s = 0
    multiplier = 1
    n = len(x)
    for i in range(n):
        s += multiplier * aux(x[-i-1])
        multiplier *= 32
    if not(positive):
        s = -s
    return s
        

class Track():
    
    def __init__(self, draw_platform = True):
        
        self.path = ""
        self.physical = []
        self.scenery = []
        self.x_spawn , self.y_spawn = 0,0
        self.powerups = []
        plt.figure("track_plot")
        
        # Turtle
        self.x_turtle , self.y_turtle = 0,0
        self.turtle_scenery = False
        
        if draw_platform:
            self.draw([0,80],[0,0])
    
    # Show the track in Python using matplolib.pyplot
    def show(self):
        
        plt.figure("track_plot")
        
        # Plot physical lines
        for X,Y in self.physical:
            plt.plot(X,Y,color="black")
        
        # Plot scenery
        for X,Y in self.scenery:
            plt.plot(X,Y,color="gray")
            
        # Plot powerups
        for p in self.powerups:
            p.plot()
        
        # Plot spawn area
        Xspawn, Yspawn = [0,80,80,0,0,80,0,80],[0,0,80,80,0,80,80,0]
        Xspawn, Yspawn = [x+self.x_spawn for x in Xspawn],[y+self.y_spawn for y in Yspawn]
        plt.plot(Xspawn, Yspawn ,color="red")
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()
    
    # Generate the code to export to freerideer
    def gen_code(self):
        
        self.shift_all(-self.x_spawn-40,-self.y_spawn-50)
        
        def aux(list):
            
            s = ""
            first = True
            for (X,Y) in list:
                if not(first):
                    s += ","
                first = False
                
                first2 = True
                for i in range(len(X)):
                    if not(first2):
                        s += " "
                    first2 = False
                    s += translate(X[i])+" "+translate(-Y[i])
            
            return s
        
        sp = ""
        first = True
        for p in self.powerups:
            if not(first):
                sp += ","
            first = False
            sp += p.to_string()
        
        code = aux(self.physical) + "#" + aux(self.scenery) + "#" + sp
        self.shift_all(self.x_spawn+40,self.y_spawn+50)
        
        return code
    
    # Set the spawning area location
    def set_spawn(self,x,y):
        
        self.x_spawn,self.y_spawn = x,y
    
    # Generate the code and print it to a file
    def print_to_file(self,file):
        
        code = self.gen_code()
        
        f = open(self.path+file+".txt", "w")
        f.write(code)
        f.close()
        return code
    
    # Draw X,Y to the track
    def draw(self,X,Y,scenery=False):
        if scenery:
            self.scenery.append((X,Y))
        else:
            self.physical.append((X,Y))
    
    # Add powerup
    def add_powerup(self,p):
        self.powerups.append(p)
    
    # Shift the whole track by (dx,dy)
    def shift_all(self,dx,dy):
        
        for (X,Y) in self.physical:
            for i in range(len(X)):
                X[i] += dx
                Y[i] += dy
        for (X,Y) in self.scenery:
            for i in range(len(X)):
                X[i] += dx
                Y[i] += dy
        for p in self.powerups:
            p.shift(dx,dy)
    
    # Draw a circle centered at (x,y)
    def draw_circle(self,x,y,radius,scenery=False):
        
        n = int(radius * 2 * m.pi / 10)
        X = [x+radius]
        Y = [y]
        for i in range(1,n+1):
            alpha = m.pi*2*i/n
            X.append(x+radius*m.cos(alpha))
            Y.append(y+radius*m.sin(alpha))
        self.draw(X,Y,scenery)
    
    def draw_asset(self,x0,y0,asset_name,scale=1,scenery=False,rotation=0):
        
        anchor="SO"
        
        # Opening file
        f = open("C:/users/robin/Desktop/freeriderhd/assets/"+asset_name+".txt", "r")
        raw_drawing = f.readline()[:-2]
        f.close()
        
        asset = []
        
        # Splitting the drawing into lines
        lines = raw_drawing.split(",")
        for line in lines:
            
            # Translating into decimal coordinates
            coordinates = line.split(" ")
            n = len(coordinates)
            coordinates2 = [translate_back(x) for x in coordinates]
            X = [coordinates2[2*i] for i in range(n//2)]
            Y = [-coordinates2[2*i+1] for i in range(n//2)]
            asset.append((X,Y))
        
        # Finding the anchor point
        min_y,max_y = 0,0
        x_min_y,x_max_y = [],[]
        first = True
        for X,Y in asset:
            for i in range(len(X)):
                if Y[i] < min_y or first:
                    min_y = Y[i]
                    x_min_y = [X[i]]
                elif Y[i] == min_y:
                    x_min_y.append(X[i])
                
                if Y[i] > max_y or first:
                    max_y = Y[i]
                    x_max_y = [X[i]]
                elif Y[i] == max_y:
                    x_max_y.append(X[i])
                
                first = False
        
        anchor_x , anchor_y = 0,0
        if anchor == "SO":
            anchor_x , anchor_y = min(x_min_y) , min_y
        if anchor == "NO":
            anchor_x , anchor_y = min(x_max_y) , max_y
        
        # Shifting toward 0,0
        for X,Y in asset:
            for i in range(len(X)):
                X[i] -= anchor_x
                Y[i] -= anchor_y
                
        # Scaling
        for X,Y in asset:
            for i in range(len(X)):
                X[i] *= scale
                Y[i] *= scale
        
        # Rotating
        for X,Y in asset:
            for i in range(len(X)):
                cos,sin = m.cos(rotation),m.sin(rotation)
                X[i] , Y[i] = X[i]*cos - Y[i]*sin , X[i]*sin + Y[i]*cos
        
        # Shifting to definitive position
        # Shifting toward 0,0
        for X,Y in asset:
            for i in range(len(X)):
                X[i] += x0
                Y[i] += y0
        
        for X,Y in asset:
            for i in range(len(X)):
                X[i] = X[i]
                Y[i] = Y[i]
        
        # Drawing
        for X,Y in asset:
            self.draw(X,Y,scenery)

    def set_turtle(self,x,y,theta,scenery=False):
        
        self.x_turtle , self.y_turtle = x,y
        self.theta_turtle = theta
        self.turtle_scenery = scenery
        
    def move_turtle(self,distance,dtheta):
        
        self.theta_turtle += dtheta
        new_x = self.x_turtle + distance*m.cos(self.theta_turtle)
        new_y = self.y_turtle + distance*m.sin(self.theta_turtle)
        self.draw([self.x_turtle,new_x],[self.y_turtle,new_y],self.turtle_scenery)
        self.x_turtle , self.y_turtle = new_x , new_y


