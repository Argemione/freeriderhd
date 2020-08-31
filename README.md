# freerider.py Documentation

## Track Class

**Track -**
Constructor.
- *draw_platform*: if true, generate a spawning platform from (0,0) to (80,0). (default value: True)

**show -**
Show a preview of the track in Python, using matplotlib.pyplot.

**gen_code -**
Return the code of the track as string.

**set_spawn -**
Set the spawning location at a different place than (0,0).
- *x,y*: coordinates of the bottom left corner of the new spawn.

**print_to_file -**
Export the code of the track to a file.
- *file*: string containing the path of the file.

**draw -**
Draw a line from (X[0],Y[0]), to (X[1],Y[1]), (X[2],Y[2]) and so on
- *X,Y*: lists of coordinates. Must be the same size and contain at least 2 elements each.
- *scenery*: if true, the line is drawn as a scenery. (default value: False)

**add_powerup -**
Add a powerup to the track.
- *p*: an element of the class Powerup.

**draw_circle -**
Draw a circle.
- *x,y*: coordinates of the center of the circle.
- *radius*: radius of the circle.
- *scenery*: if true, the circle is drawn as a scenery. (default value: False)

**draw_asset -**
Draw an asset.
- *x0,y0*: coordinates of the bottom left corner of the asset.
- *asset_name*: name of the file containing the freerider code for the asset. This file must be contained in the same folder.
- *scale*: scaling factor. (default value: 1)
- *scenery*: if true, the asset is drawn as a scenery. (default value: False)
- *rotation*: rotation of the asset in rad. (default value: 0)

**set_turtle -**
Set the turtle location.
- *x,y*: coordinates of the turtle.
- *theta*: direction of the turtle in rad.
- *scenery*: if true, every further move of the turtle will be drawn as scenery. (default value: False)

**move_turtle -**
Turn the turtle by an angle, and then move it by some distance, drawing a line along its trajectory.
- *distance*: distance by which the turtle is moved.
- *dtheta*: angle by which the turtle rotates before its movement.

## Class Powerup

**Powerup -**
Constructor.
- *type*: Type of the powerup. May be Powerup.STAR, BOOST, GRAVITY, SLOW_MOTION, BOMB, CHECKPOINT, ANTIGRAVITY, WARP.
- *x,y*: coordinates of the powerup.
- *angle*: direction of the powerup in rad. Only matters for BOOST and GRAVITY. (default value: 0)
- *x2,y2*: additional coordinates for WARP end portal. (default value: 0,0)
