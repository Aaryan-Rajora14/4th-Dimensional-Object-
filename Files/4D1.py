import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider

# Define the 16 vertices of a tesseract (4D hypercube)
vertices = np.array([[-1, -1, -1, -1], [-1, -1, -1,  1], [-1, -1,  1, -1], [-1, -1,  1,  1],
                     [-1,  1, -1, -1], [-1,  1, -1,  1], [-1,  1,  1, -1], [-1,  1,  1,  1],
                     [ 1, -1, -1, -1], [ 1, -1, -1,  1], [ 1, -1,  1, -1], [ 1, -1,  1,  1],
                     [ 1,  1, -1, -1], [ 1,  1, -1,  1], [ 1,  1,  1, -1], [ 1,  1,  1,  1]])

# Define edges (vertex pairs)
edges = [(0,1), (0,2), (0,4), (1,3), (1,5), (2,3), (2,6), (3,7), (4,5), (4,6), (5,7), (6,7),
         (8,9), (8,10), (8,12), (9,11), (9,13), (10,11), (10,14), (11,15), (12,13), (12,14),
         (13,15), (14,15), (0,8), (1,9), (2,10), (3,11), (4,12), (5,13), (6,14), (7,15)]

# Projection from 4D to 3D
def project_4d_to_3d(points_4d, angle_xy, angle_xz, angle_xw, distance=3):
    rotation_xy = np.array([[np.cos(angle_xy), -np.sin(angle_xy), 0, 0],
                            [np.sin(angle_xy), np.cos(angle_xy), 0, 0],
                            [0, 0, 1, 0], [0, 0, 0, 1]])
    
    rotation_xz = np.array([[np.cos(angle_xz), 0, -np.sin(angle_xz), 0],
                            [0, 1, 0, 0], [np.sin(angle_xz), 0, np.cos(angle_xz), 0], [0, 0, 0, 1]])
    
    rotation_xw = np.array([[np.cos(angle_xw), 0, 0, -np.sin(angle_xw)],
                            [0, 1, 0, 0], [0, 0, 1, 0], [np.sin(angle_xw), 0, 0, np.cos(angle_xw)]])
    
    # Correct matrix multiplication order
    rotated = points_4d @ rotation_xy @ rotation_xz @ rotation_xw
    
    # Avoid division errors in perspective projection
    w = 1 / (distance - rotated[:, 3] + 1e-6)
    x = rotated[:, 0] * w
    y = rotated[:, 1] * w
    z = rotated[:, 2] * w
    
    return np.column_stack((x, y, z))

# Set up the figure
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
plt.subplots_adjust(bottom=0.3)

# Initial angles
angle_xy, angle_xz, angle_xw = 0.5, 0.5, 0.5
projected = project_4d_to_3d(vertices, angle_xy, angle_xz, angle_xw)

# Plot edges
lines = []
for edge in edges:
    line, = ax.plot(projected[edge, 0], projected[edge, 1], projected[edge, 2], 'b-')
    lines.append(line)

# Set axis limits
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_zlim([-2, 2])
ax.set_title('Interactive 4D Tesseract Projection')

# Create sliders
axcolor = 'lightgoldenrodyellow'
ax_xy = plt.axes([0.25, 0.2, 0.65, 0.03], facecolor=axcolor)
ax_xz = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_xw = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)

slider_xy = Slider(ax_xy, 'XY Rotation', 0, 2*np.pi, valinit=angle_xy)
slider_xz = Slider(ax_xz, 'XZ Rotation', 0, 2*np.pi, valinit=angle_xz)
slider_xw = Slider(ax_xw, 'XW Rotation', 0, 2*np.pi, valinit=angle_xw)

# Update function for sliders
def update(val):
    global angle_xy, angle_xz, angle_xw
    angle_xy, angle_xz, angle_xw = slider_xy.val, slider_xz.val, slider_xw.val
    projected = project_4d_to_3d(vertices, angle_xy, angle_xz, angle_xw)
    
    for i, edge in enumerate(edges):
        lines[i].set_xdata(projected[edge, 0])
        lines[i].set_ydata(projected[edge, 1])
        lines[i].set_3d_properties(projected[edge, 2])
    
    fig.canvas.draw_idle()

slider_xy.on_changed(update)
slider_xz.on_changed(update)
slider_xw.on_changed(update)

plt.show()
