"""
Soubor jenž slouží načtení Objektu, aneb vypočítání všech důležitých informací které jsou potřeba ke zkonstruování 3D Wireframe
Dominantní framework který využívám je OpenGL a také pygame
Pomocí OpenGL vytvářím objekt a zobrazuji ho v okně pygame
"""


import os
import pygame
from pygame import mouse
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pywavefront
import sys
count_vertex = 0
faces = 0
objname = ""
scene = ""
data_f = ""

def ExportData():
    #Creating variables
    f_data = ""
    v_data = ""

    #I have list of lists, so I just convert the lists to string for better working with csv
    #And push them into the data
    for i in range(len(scene.vertices)):
        v_data += (str(scene.vertices[i]) + "\n")
    #Same here
    for a in range(len(data_f)):
        f_data += (str(data_f[a]) + "\n")
    return(v_data,f_data)
#Function that formats string for Object Information (The values I can't reach from Main-Menu.py)
def Statistics(num_vertices,num_faces):
    vertices = num_vertices
    faces = num_faces
    info = "Verticies: {} \nFaces: {}".format(vertices,faces)
    return(info)

#Draw normal x,y,z-axis
def _draw_axes():
    glBegin(GL_LINES)
    glColor3f(1, 0, 0)
    glVertex3f(-1000, 0, 0)
    glVertex3f(1000, 0, 0)
    glColor3f(0, 0, 1)
    glVertex3f(0, -1000, 0)
    glVertex3f(0, 1000, 0)
    glColor3f(1, 0, 1)
    glVertex3f(0, 0, -1000)
    glVertex3f(0, 0, 1000)
    glEnd()

def Model(scene, scene_scale, scene_trans):
    #Variables for statictics
    global count_vertex
    global faces
    global data_f
    count_vertex = 0
    glColor3f(0,0,0)
    #Creating first Matrix
    glPushMatrix()
    #Scaling and moving vertices that depends on screen
    glScalef(*scene_scale)
    glTranslatef(*scene_trans)
    #Main loop for loading vertices
    for mesh in scene.mesh_list:
        #Set geometry defition mode to Triangles
        #And start the cycle of creating vertices
        glBegin(GL_TRIANGLES)
        #Every face has vertices so checking every face
        for face in mesh.faces:
            #And every vertex in that face
            for vertex_i in face:
                #Couting that vertices
                count_vertex += 1
                #Creating Vertex with 3args with collected vertices in scene that we created in the start of main function
                #It will generate Matrix of size 3*n
                glVertex3f(*scene.vertices[vertex_i])
        glEnd()
    glPopMatrix()
    faces = len(mesh.faces)
    data_f = mesh.faces
#Function for existing Pygame
def quit():
    pygame.quit()

#Reset the view - Coords of the model
def ResetView():
        glTranslatef(1,0,0)
        x = glGetIntegerv(GL_MODELVIEW_MATRIX)
        glPopMatrix()#Pops the current Matrix of coords
        glPushMatrix()
        glTranslatef(0.0, 0.0, -10)

def main():
        global scene
        scene = pywavefront.Wavefront(objname, collect_faces=True) #Setting a scene with PyWaveFront
        #Collect faces = Collects triangle data, that means when there is a face with more than 3 vertices
        #It will be triangulated
        # pywavefront.Wavefront().mesh_list
        scene_box = (scene.vertices[0], scene.vertices[0])
        #Set up the scene box
        for vertex in scene.vertices:
            min_v = [min(scene_box[0][i], vertex[i]) for i in range(3)]
            max_v = [max(scene_box[1][i], vertex[i]) for i in range(3)]
            scene_box = (min_v, max_v)
        #PyWaveFront saves vertices data in scene.vertices and each vertex is a tuple with 3 args.
        #vertex[i] = (x,y,z) coords
        scene_size     = [scene_box[1][i]-scene_box[0][i] for i in range(3)]
        max_scene_size = max(scene_size)
        scaled_size    = 5
        scene_scale    = [scaled_size/max_scene_size for i in range(3)]
        scene_trans    = [-(scene_box[1][i]+scene_box[0][i])/2 for i in range(3)]

        #Initializing Pygame and setting UI
        pygame.init()
        pygame.display.set_caption('Wireframe viewport')
        Icon = pygame.image.load('Images/icon.png')
        pygame.display.set_icon(Icon)
        display = (800, 600)
        screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        #Colors for viewport bg
        rValue= 105.0 / 255.0
        gValue= 105.0 / 255.0
        bValue= 105.0 / 255.0
        glClearColor(rValue, gValue, bValue, 1)#RGBA
        glClear(GL_COLOR_BUFFER_BIT)    #Color Init
        gluPerspective(45, (display[0] / display[1]), 1, 500.0)
        # glColor3f(0,0,0) Idk why is it here
        glPushMatrix() #Duplicating Matrix of coords, for reseting the view
        glTranslatef(0.0, 0.0, -10) #Zoom out


        ms_l_button_down = False
        ms_w_button_down = False
        toggle = False
        reset = False
        quitPygame = False
        #Main loop that runs the whole time when Viewport is opened
        while not quitPygame:
            #Keybinds
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quitPygame = True #It was crashing when I called pygame.quit() here, so I'll just jump from this while loop and then quit the program
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # print(scene.vertices) View Matrix of Vertices
                        if toggle:
                            toggle = False
                        else:
                            toggle = True
                    if event.key == pygame.K_q:
                        ResetView()
                if event.type == pygame.MOUSEMOTION:
                    #Rotation when LMB hold, rotation depends on mouse movement
                    if ms_l_button_down == True:
                        glRotatef(event.rel[1], 1, 0, 0)
                        glRotatef(event.rel[0], 0, 1, 0)
                    elif ms_w_button_down == True:
                        #Moving the object
                        # / 100 for slower move
                        glTranslatef(event.rel[0]/100,event.rel[1]*(-1)/100,0)
                    else:
                        #Reseting color, when rotation model is red
                        glColor3f(0,0,0)
                        #pass
                if event.type == pygame.MOUSEBUTTONDOWN:
                        #Zooming object
                        if event.button == 5:glScaled(0.9,0.9,0.9)
                        if event.button == 4:glScaled(1.1,1.1,1.1)
            for event in pygame.mouse.get_pressed():
                #Getting if mouse buttons are pressed right now
                if pygame.mouse.get_pressed()[0] == 1:
                    ms_l_button_down = True
                elif pygame.mouse.get_pressed()[0] == 0:
                    ms_l_button_down = False
                if pygame.mouse.get_pressed()[1] == 1:
                    ms_w_button_down = True
                elif pygame.mouse.get_pressed()[1] == 0:
                    ms_w_button_down = False
            #Auto rotate - R
            if(toggle):
                glRotatef(1, 0, 0.5, 0)

            #Updates(clears) the colors(buffers) to preset values
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            #Controls the polygons for rasterization
            #glPolygonMode(face,mode)
            #GL_FRONT_AND_BACK - Simply describes which polygons does the "mode" applies to, in my case to every
            #GL_LINE - Polygon vertices that are "start vertices" are drawn as points and then lines between them
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            #Model function - Explaited up
            _draw_axes()
            Model(scene,scene_scale,scene_trans)
            #Update the full display Surface to the screen
            pygame.display.flip()
            #For optimalization - If program waits (even a little time) it will help to processor
            pygame.time.wait(10)


        pygame.quit()
#Drivers Code
if __name__ == "__main__":
    main()
