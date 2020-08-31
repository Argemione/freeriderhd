from freerider import *
import math as m

# Create the track. If "draw_platform" is True, then a spawn platform is generated.
# The spawn platform goes from (0,0) to (80,0)
track = Track(draw_platform = True)

# A function to exlain how to draw a sinus.
def draw_sinus():
    
    def f(x):
        # "200" is the amplitude, and "0.01" the frequence
        return 200 * m.sin(0.01*x)
    
    # X coordinates start at 80
    X = [80+10*i for i in range(100)]
    Y = [ f(x) - f(X[0]) for x in X]
    
    # Main command to draw lines
    track.draw(X,Y)

draw_sinus()

# Adding a star to finish the level
track.add_powerup(Powerup(PowerupType.STAR,1072,-228))

# Specifying "scenery = True" allows drawing scenery (by opposition to physical lines)
track.draw([20,1000],[-20,-200],scenery = True)

# To show a preview of the track in Python
track.show()

# To generate the code
code = track.gen_code()
print(code)

# Alternatively, you can export to a file
track.print_to_file("hey")