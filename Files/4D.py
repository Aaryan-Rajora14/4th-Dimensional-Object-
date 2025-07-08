import pygame
import math
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("4D Interactive Tesseract")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define tesseract vertices in 4D (16 vertices)
vertices = [
    [-1, -1, -1, -1],
    [-1, -1, -1,  1],
    [-1, -1,  1, -1],
    [-1, -1,  1,  1],
    [-1,  1, -1, -1],
    [-1,  1, -1,  1],
    [-1,  1,  1, -1],
    [-1,  1,  1,  1],
    [ 1, -1, -1, -1],
    [ 1, -1, -1,  1],
    [ 1, -1,  1, -1],
    [ 1, -1,  1,  1],
    [ 1,  1, -1, -1],
    [ 1,  1, -1,  1],
    [ 1,  1,  1, -1],
    [ 1,  1,  1,  1],
]

# Define edges connecting vertices (32 edges)
edges = []
for i in range(16):
    for j in range(i+1, 16):
        diff = sum([vertices[i][k] != vertices[j][k] for k in range(4)])
        if diff == 1:
            edges.append((i, j))

# Rotation matrices for 4D rotations
def rotation_matrix_4d(angle, i, j):
    """Create a 4D rotation matrix rotating in the plane defined by axes i and j."""
    mat = [[1 if x == y else 0 for y in range(4)] for x in range(4)]
    mat[i][i] = math.cos(angle)
    mat[i][j] = -math.sin(angle)
    mat[j][i] = math.sin(angle)
    mat[j][j] = math.cos(angle)
    return mat

def mat_vec_mult(mat, vec):
    return [sum(mat[i][j] * vec[j] for j in range(4)) for i in range(4)]

# Projection from 4D to 3D
def project_4d_to_3d(point4d, distance=2):
    w = 1 / (distance - point4d[3])
    projected = [coord * w for coord in point4d[:3]]
    return projected

# Projection from 3D to 2D
def project_3d_to_2d(point3d, distance=2):
    z = 1 / (distance - point3d[2])
    x = point3d[0] * z * WIDTH / 4 + WIDTH / 2
    y = point3d[1] * z * HEIGHT / 4 + HEIGHT / 2
    return (int(x), int(y))

# Main loop variables
angle_speed = 0.02
angle_xy = 0
angle_zw = 0
angle_xz = 0
angle_yw = 0

clock = pygame.time.Clock()

def main():
    global angle_xy, angle_zw, angle_xz, angle_yw

    running = True
    while running:
        clock.tick(60)
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle key presses for rotation control
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            angle_xy += angle_speed
        if keys[pygame.K_a]:
            angle_xy -= angle_speed
        if keys[pygame.K_w]:
            angle_zw += angle_speed
        if keys[pygame.K_s]:
            angle_zw -= angle_speed
        if keys[pygame.K_e]:
            angle_xz += angle_speed
        if keys[pygame.K_d]:
            angle_xz -= angle_speed
        if keys[pygame.K_r]:
            angle_yw += angle_speed
        if keys[pygame.K_f]:
            angle_yw -= angle_speed

        # Create rotation matrices
        rot_xy = rotation_matrix_4d(angle_xy, 0, 1)
        rot_zw = rotation_matrix_4d(angle_zw, 2, 3)
        rot_xz = rotation_matrix_4d(angle_xz, 0, 2)
        rot_yw = rotation_matrix_4d(angle_yw, 1, 3)

        # Rotate vertices
        rotated_vertices = []
        for v in vertices:
            r = mat_vec_mult(rot_xy, v)
            r = mat_vec_mult(rot_zw, r)
            r = mat_vec_mult(rot_xz, r)
            r = mat_vec_mult(rot_yw, r)
            rotated_vertices.append(r)

        # Project vertices from 4D to 3D
        projected_3d = [project_4d_to_3d(v) for v in rotated_vertices]

        # Project vertices from 3D to 2D
        projected_2d = [project_3d_to_2d(v) for v in projected_3d]

        # Draw edges
        for edge in edges:
            pygame.draw.line(screen, WHITE, projected_2d[edge[0]], projected_2d[edge[1]], 1)

        # Draw vertices
        for point in projected_2d:
            pygame.draw.circle(screen, WHITE, point, 4)

        # Display instructions
        font = pygame.font.SysFont(None, 24)
        instructions = [
            "Controls:",
            "Q/A: Rotate XY plane",
            "W/S: Rotate ZW plane",
            "E/D: Rotate XZ plane",
            "R/F: Rotate YW plane",
            "Close window to exit"
        ]
        for i, text in enumerate(instructions):
            img = font.render(text, True, WHITE)
            screen.blit(img, (10, 10 + i * 20))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
