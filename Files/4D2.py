import numpy as np
import plotly.graph_objects as go
import plotly.io as pio

# Use browser as default renderer
pio.renderers.default = 'browser'

# Define tesseract vertices
vertices = np.array([[-1, -1, -1, -1], [-1, -1, -1,  1], [-1, -1,  1, -1], [-1, -1,  1,  1],
                     [-1,  1, -1, -1], [-1,  1, -1,  1], [-1,  1,  1, -1], [-1,  1,  1,  1],
                     [ 1, -1, -1, -1], [ 1, -1, -1,  1], [ 1, -1,  1, -1], [ 1, -1,  1,  1],
                     [ 1,  1, -1, -1], [ 1,  1, -1,  1], [ 1,  1,  1, -1], [ 1,  1,  1,  1]])

# Tesseract edges
edges = [(0,1), (0,2), (0,4), (1,3), (1,5), (2,3), (2,6), (3,7),
         (4,5), (4,6), (5,7), (6,7), (8,9), (8,10), (8,12), (9,11),
         (9,13), (10,11), (10,14), (11,15), (12,13), (12,14), (13,15),
         (14,15), (0,8), (1,9), (2,10), (3,11), (4,12), (5,13), (6,14), (7,15)]

# 4D to 3D projection
def project_4d_to_3d(vertices, angle_xy=0, angle_xz=0, angle_xw=0, distance=3):
    rot_xy = np.array([[np.cos(angle_xy), -np.sin(angle_xy), 0, 0],
                       [np.sin(angle_xy), np.cos(angle_xy),  0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]])
    
    rot_xz = np.array([[np.cos(angle_xz), 0, -np.sin(angle_xz), 0],
                       [0, 1, 0, 0],
                       [np.sin(angle_xz), 0, np.cos(angle_xz), 0],
                       [0, 0, 0, 1]])
    
    rot_xw = np.array([[np.cos(angle_xw), 0, 0, -np.sin(angle_xw)],
                       [0, 1, 0, 0],
                       [0, 0, 1, 0],
                       [np.sin(angle_xw), 0, 0, np.cos(angle_xw)]])
    
    rotated = vertices @ rot_xy @ rot_xz @ rot_xw
    w = 1 / (distance - rotated[:, 3] + 1e-6)
    x = rotated[:, 0] * w
    y = rotated[:, 1] * w
    z = rotated[:, 2] * w
    return np.stack((x, y, z), axis=1)

# Frames for different angle_xw values
angle_steps = np.linspace(0, 2*np.pi, 50)
frames = []

for angle in angle_steps:
    projected = project_4d_to_3d(vertices, angle_xy=0.7, angle_xz=0.6, angle_xw=angle)
    edge_lines = []
    for edge in edges:
        edge_lines.append(go.Scatter3d(
            x=[projected[edge[0], 0], projected[edge[1], 0]],
            y=[projected[edge[0], 1], projected[edge[1], 1]],
            z=[projected[edge[0], 2], projected[edge[1], 2]],
            mode='lines',
            line=dict(color='blue', width=6),
            hoverinfo='none',
            showlegend=False
        ))
    points = go.Scatter3d(
        x=projected[:, 0], y=projected[:, 1], z=projected[:, 2],
        mode='markers',
        marker=dict(size=10, color='crimson'),
        name='Vertices',
        showlegend=False
    )
    frames.append(go.Frame(data=[*edge_lines, points], name=f'{angle:.2f}'))

# Initial plot (angle_xw = 0)
initial_proj = project_4d_to_3d(vertices, 0.7, 0.6, 0)
lines = [go.Scatter3d(
    x=[initial_proj[e[0], 0], initial_proj[e[1], 0]],
    y=[initial_proj[e[0], 1], initial_proj[e[1], 1]],
    z=[initial_proj[e[0], 2], initial_proj[e[1], 2]],
    mode='lines',
    line=dict(color='blue', width=10),
    hoverinfo='none',
    showlegend=False
) for e in edges]

points = go.Scatter3d(
    x=initial_proj[:, 0], y=initial_proj[:, 1], z=initial_proj[:, 2],
    mode='markers',
    marker=dict(size=2, color='crimson'),
    name='Vertices'
)

# Layout with slider
layout = go.Layout(
    title='Interactive 4D Tesseract Projection with XW Rotation Slider',
    scene=dict(
        xaxis=dict(range=[-2, 2], title='X'),
        yaxis=dict(range=[-2, 2], title='Y'),
        zaxis=dict(range=[-2, 2], title='Z'),
        bgcolor='black',
        aspectmode='cube'
    ),
    paper_bgcolor='black',
    font=dict(color='white'),
    updatemenus=[dict(
        type='buttons',
        showactive=False,
        y=1.05,
        x=0.8,
        xanchor='left',
        yanchor='top',
        buttons=[dict(label='Play',
                      method='animate',
                      args=[None, dict(frame=dict(duration=50, redraw=True),
                                       fromcurrent=True, mode='immediate')]),
                 dict(label='Pause',
                      method='animate',
                      args=[[None], dict(frame=dict(duration=0), mode='immediate')])]
    )],
    sliders=[{
        'steps': [{
            'method': 'animate',
            'args': [[f'{angle:.2f}'], dict(mode='immediate', frame=dict(duration=0), redraw=True)],
            'label': f'{angle:.2f}'
        } for angle in angle_steps],
        'transition': {'duration': 0},
        'x': 0.1, 'y': 0, 'currentvalue': {'prefix': 'XW Rotation: '}
    }]
)

fig = go.Figure(data=[*lines, points], layout=layout, frames=frames)
fig.show()
