# -*- coding: utf-8 -*-
# vispy: gallery 30
# -----------------------------------------------------------------------------
# 2014, Almar Klein
# Distributed under the terms of the new BSD License.
# -----------------------------------------------------------------------------
 
""" Visualization of traveling through space.
"""
 
import time
 
import numpy as np
 
from vispy import gloo
from vispy import app
from vispy.util.transforms import perspective, rotate
 
 
vertex = """
#version 120
 
uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;
uniform float u_time_offset;
 
attribute vec3  a_position;
attribute float a_radius;
 
 
varying float v_pointsize;
 
void main (void) {
 
    
    // convert to z=north pole
    vec3 pos = a_position;
 
    vec4 v_eye_position = u_view * u_model * vec4(pos, 1.0);
    gl_Position = u_projection * v_eye_position;
 
    // stackoverflow.com/questions/8608844/...
    //  ... resizing-point-sprites-based-on-distance-from-the-camera
    float radius = 1;
    vec4 corner = vec4(radius, radius, v_eye_position.z, v_eye_position.w);
    vec4  proj_corner = u_projection * corner;
    
    
    gl_PointSize = 50.0 * a_radius * proj_corner.x / proj_corner.w;
    v_pointsize = gl_PointSize;
}
"""
 
fragment = """
#version 120
varying float v_pointsize;
 
uniform float u_scaleparameter1;
 
void main()
{
    float x = 2.0*gl_PointCoord.x - 1.0;
    float y = 2.0*gl_PointCoord.y - 1.0;
    float r2 = (x*x + y*y);
    float a;
    
    if (r2> 1) {
        a = 0;
    } else {
        a = sqrt(1-r2);
    }
    
    
    a = u_scaleparameter1 * sqrt(2*a);
    
    
    gl_FragColor = vec4(a, a , a , 1.0);
}
 
"""
 
N = 100000  # Number of stars 
SIZE = 100
SPEED = 4.0  # time in seconds to go through one block
NBLOCKS = 10
 
 
class Canvas(app.Canvas):
 
    def __init__(self, stardata):
        global positions;
        app.Canvas.__init__(self, title='Spacy', keys='interactive')
        self.size = 800, 600
        
        self.program = gloo.Program(vertex, fragment)
        self.view = np.eye(4, dtype=np.float32)
        self.model = np.eye(4, dtype=np.float32)
        self.projection = np.eye(4, dtype=np.float32)
        
        self.timer = app.Timer('auto', connect=self.update, start=True)
        
        # Set uniforms (some are set later)
        self.program['u_model'] = self.model
        self.program['u_view'] = self.view
        self.program['u_scaleparameter1'] = 0.2
        
        # Set attributes
        #self.program['a_position'] = np.zeros((N, 3), np.float32)
        #self.program['a_offset'] = np.zeros((N,), np.float32)
        
        # Compute the positions of the stars as vectors, normalized to length 1
        self.positions = positions = np.zeros((stardata.shape[0], 3), np.float32)
        rightascention, declination = stardata.T/180*np.pi
        
        distance = np.random.random(declination.shape)
        radius = np.random.random(declination.shape)
        
        positions[:,0] = distance * np.cos(declination) * np.sin(rightascention)
        positions[:,2] = distance * -np.cos(declination) * np.cos(rightascention)
        positions[:,1] = distance * np.sin(declination)
        
        
        
        
        self.program['a_position'] = np.array(positions, np.float32)
        self.program['a_radius'] = np.array(radius, np.float32)
        #self.program['a_position'] = np.array(stardata, np.float32)
         
    
    def on_initialize(self, event):
        gloo.set_state(clear_color='black', depth_test=False,
                       blend=True, blend_equation='func_add',
                       blend_func=('one', 'one'))
 
    def on_key_press(self, event):
        if event.text == ' ':
            if self.timer.running:
                self.timer.stop()
            else:
                self.timer.start()
    def on_mouse_move(self, event):
        data = event.pos
        rx = np.pi*(data[1]-300)/3
        ry = np.pi*(data[0]-300)/3
        self.view = self.program['u_view'] = rotate(rotate(np.eye(4), rx, 1,0,0),ry, 0,1,0)
        
        
 
        print ('event', self.view)
        self.update()
 
    def on_resize(self, event):
        width, height = event.size
        gloo.set_viewport(0, 0, width, height)
        far = SIZE*(NBLOCKS-2)
        self.projection = perspective(100.0, width / float(height), 0.1, 10.0)
        self.program['u_projection'] = self.projection
 
    def on_draw(self, event):
 
        
        # Draw
        gloo.clear()
        self.program.draw('points')
        
    
    def on_close(self, event):
        self.timer.stop()
    
 
 
if __name__ == '__main__':
    # Load the data file
    import os
    filename = os.path.join(os.path.dirname(__file__), 'hygxyz.csv')
    try:
        data = np.genfromtxt(
            fname = '/Users/rob/Projecten/python/vispy/examples/demo/gloo/hygxyz.csv',
            skip_header = 1,
            delimiter = ',',
            usecols = (10, 11),
            )
    except:
        raise IOError('Could not open %s. Please download it from https://raw.githubusercontent.com/astronexus/HYG-Database/master/hygxyz.csv' % filename)
        
        
    c = Canvas(data[:100,:])
    c.show()
    app.run()
