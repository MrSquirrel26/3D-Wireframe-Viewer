"""
 ________________________________________________________________________________
|                                                                                |
|  This does not belong to the main program, it's just something I wanted to try |
|________________________________________________________________________________|
""" 
import Viewport
from pyglet.gl import *
from pywavefront import visualization, Wavefront
rotation = 0.0

def draw_object(object, x, y):
    #I'm moving the object to the right spot and then drawing him
    glLoadIdentity()
    glTranslated(x,y, -10.0)
    glRotatef(rotation, 0.0, 1.0, 0.0)
    visualization.draw(object)

#This is called every tick in the app and rotates the object
def update(dt):
    global rotation
    rotation += 90.0 * dt
    if rotation > 360:
        rotation = 0
#Main function which is called by the button
def main():
    global rotation
    rotation = 0
    #Creating window and initializing obj as I did in the Viewport
    window = pyglet.window.Window(width=1280, height=720,caption="Full View")
    obj = Wavefront(Viewport.objname)

    #Pyglet has methods on events, simply put it means that this method get called when this event is triggred
    @window.event
    def on_draw():
        viewport_width, viewport_height = window.get_framebuffer_size()
        #glViewport - specifies the affine transformation of x and y from normalized device coordinates to window coordinates
        glViewport(0, 0, viewport_width, viewport_height)
        #gl MatrixMode - We are giving informations which matrix is the target for next operation
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        #Setting the perspective
        gluPerspective(45., float(1280)/float(720), 1., 100.)
        glMatrixMode(GL_MODELVIEW)
        window.clear()
        glLoadIdentity()
        draw_object(obj, 0.0, 0.0)
    pyglet.clock.schedule(update)
    pyglet.app.run()
    

if __name__ == "__main__":
    main()
