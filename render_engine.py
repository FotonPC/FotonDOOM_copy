import numpy
import numba
import pygame
import settings
import math

@numba.njit(cache=True, fastmath=True)
def trace_ray(resolution_x, rays_matrix_steps, angle, s_x, s_y, mAp, sprites):
    rays = numpy.zeros((resolution_x, 4))
    rays_sprite = numpy.zeros((resolution_x, 4))
    ar = (angle - 45) // 90
    x = s_x
    y = s_y
    x_step = rays_matrix_steps[angle][128][0]
    y_step = rays_matrix_steps[angle][128][1]
    s = False
    while mAp[int(x)][int(y)] <= 0:
        k = 0
        run = True
        while sprites[k][0] > 0:
            sp = sprites[k]

            if not s and ar % 2 == 0 and intersects(x - x_step, y - y_step, x, y, sp[0] + sp[2], sp[1], sp[0] - sp[2],
                                                    sp[1]):
                s = True
                x_sprite = x
                y_sprite = y
                k_sprite = k
                break

            if not s and ar % 2 == 1 and intersects(x - x_step, y - y_step, x, y, sp[0], sp[1] + sp[3], sp[0],
                                                    sp[1] - sp[3]):
                s = True
                x_sprite = x
                y_sprite = y
                k_sprite = k
                break

            k += 1
        x += x_step
        y += y_step
    if s:
        dx = sp[2]
        dy = sp[3]
        ox1 = x_sprite - sp[0] + dx
        oy1 = y_sprite - sp[1] + dy
        if ar % 2 == 0:
            oz = ox1 / dx / 2

        else:
            oz = oy1 / dy / 2
        ozz = ar % 2
        code = k_sprite + 500
        return numpy.array(
            [math.sqrt((x_sprite - s_x) ** 2 + (y_sprite - s_y) ** 2) * math.cos(
                math.radians(128 / resolution_x * 90 - 45)), oz,
             code, ozz])
    if 1:
        ozz = -1
        code = mAp[int(x)][int(y)]
        ox = x % 1
        oy = y % 1
        if abs(ox - 0.5) < abs(oy - 0.5):
            oz = ox
        elif abs(ox - 0.5) > abs(oy - 0.5):
            oz = oy

        return numpy.array(
            [math.sqrt((x - s_x) ** 2 + (y - s_y) ** 2) * math.cos(math.radians(128 / resolution_x * 90 - 45)), oz, code,
             ozz])
@numba.njit(cache=True, fastmath=True)
def intersects(x1, y1, x2, y2, x3, y3, x4, y4):
    dx0 = x2 - x1
    dx1 = x4 - x3
    dy0 = y2 - y1
    dy1 = y4 - y3
    p0 = dy1 * (x4 -x1) - dx1 * (y4 - y1)
    p1 = dy1 * (x4 - x2) - dx1 * (y4 - y2)
    p2 = dy0 * (x2 - x3) - dx0 * (y2 - y3)
    p3 = dy0 * (x2 - x4) - dx0 * (y2 - y4)
    return (p0 * p1 <= 0) & (p2 * p3 <= 0)
@numba.njit(cache=True, fastmath=True)
def a(res_y, x):
    return int(1 / (x + 0.00001) * res_y / 2)


@numba.njit(cache=True, fastmath=True)
def nh_gr(heights, heights_sprites, resolution_x, res_y, textures, sprites, sprite_textures, angle):
    render = numpy.zeros((resolution_x, res_y, 3))
    for i in range(resolution_x):
        for k in range(res_y // 2, res_y):
            render[i][k][0] = (k - 32) * 20
            render[i][k][1] = (k - 32) * 20
            render[i][k][2] = (k - 32) * 20
        c = heights_sprites[i][0] if 0 < heights_sprites[i][0] < heights[i][0] else heights[i][0]
        for j in range(min(a(res_y, c), 64)):
            if heights_sprites[i][2] < 500:  # sprites codes
                pix0 = textures[int(heights[i][2])][int((j / a(res_y, heights[i][0]) / 2 + 0.5) * res_y)][int(heights[i][1] * res_y)]
                pix1 = textures[int(heights[i][2])][int((0.5 - j / a(res_y, heights[i][0]) / 2) * res_y)][int(heights[i][1] * res_y)]

            else:
                h = int(heights_sprites[i][2]) - 500
                pg = (angle - 45) // 90
                if heights[i][3] == 0:
                    ar = 2 * sprites[h][2]
                else:
                    ar = 2 * sprites[h][3]
                pix0 = sprite_textures[h][pg][int((j / a(res_y, heights_sprites[i][0]) / 2 + 0.5) * res_y )][int(heights_sprites[i][1] * (res_y /2))]
                pix1 = sprite_textures[h][pg][int((0.5 - j / a(res_y, heights_sprites[i][0]) / 2) * res_y )][int(heights_sprites[i][1] * (res_y /2))]
                if pix0[0] == 0 and pix0[1] == 0 and pix0[2] == 0 and (j <= a(res_y, heights[i][0])):
                    pix0 = textures[int(heights[i][2])][int((j / a(res_y, heights[i][0]) / 2 + 0.5) * res_y)][
                        int(heights[i][1] * res_y)]
                if pix1[0] == 0 and pix1[1] == 0 and pix1[2] == 0 and (j <= a(res_y, heights[i][0])):
                    pix1 = textures[int(heights[i][2])][int((0.5 - j / a(res_y, heights[i][0]) / 2) * res_y)][int(heights[i][1] * res_y)]
            if (j >= a(res_y, heights[i][0])):
                if not (pix1[0] == 0 and pix1[1] == 0 and pix1[2] == 0):
                    render[i][max(0, res_y // 2 - j, -res_y + 1)][0] = a(res_y, heights[i][0]) ** 0.25 * 7 * pix1[0]
                    render[i][max(0, res_y // 2 - j, -res_y + 1)][1] = a(res_y, heights[i][0]) ** 0.25 * 7 * pix1[1]
                    render[i][max(0, res_y // 2 - j, -res_y + 1)][2] = a(res_y, heights[i][0]) ** 0.25 * 7 * pix1[2]
                if not (pix0[0] == 0 and pix0[1] == 0 and pix0[2] == 0):
                    render[i][min(res_y - 1, res_y // 2 + j)][0] = a(res_y, heights[i][0]) ** 0.25 * 7 * pix0[0]
                    render[i][min(res_y - 1, res_y // 2 + j)][1] = a(res_y, heights[i][0]) ** 0.25 * 7 * pix0[1]
                    render[i][min(res_y // 2 + j, res_y - 1)][2] = a(res_y, heights[i][0]) ** 0.25 * 7 * pix0[2]
            else:

                render[i][max(0, res_y // 2 - j, -res_y + 1)][0] = a(res_y, heights[i][0]) ** 0.25 * 7 * pix1[0] + 100
                render[i][max(0, res_y // 2 - j, -res_y + 1)][1] = a(res_y, heights[i][0]) ** 0.25 * 7 * pix1[1] + 100
                render[i][max(0, res_y // 2 - j, -res_y + 1)][2] = a(res_y, heights[i][0]) ** 0.25 * 7 * pix1[2] + 100
                render[i][min(res_y - 1, res_y // 2 + j)][0] = a(res_y, heights[i][0]) ** 0.25 * 7 * pix0[0] + 100
                render[i][min(res_y - 1, res_y // 2 + j)][1] = a(res_y, heights[i][0]) ** 0.25 * 7 * pix0[1] + 100
                render[i][min(res_y // 2 + j, res_y - 1)][2] = a(res_y, heights[i][0]) ** 0.25 * 7 * pix0[2] + 100

    render = 255 * render / render.max()
    return render


def numba_get_render(res_y, resolution_x, rays_matrix_steps, angle, s_x, s_y, mAp, textures, sprites, sprite_textures):
    heights, heights_sprite = numba_get_distance(resolution_x, rays_matrix_steps, angle, s_x, s_y, mAp, sprites)
    return nh_gr(heights, heights_sprite, resolution_x, res_y, textures,sprites,  sprite_textures, angle)


@numba.njit(parallel=True, cache=True, fastmath=True)
def numba_get_distance(resolution_x, rays_matrix_steps, angle, s_x, s_y, mAp, sprites):
    rays = numpy.zeros((resolution_x, 4))
    rays_sprite = numpy.zeros((resolution_x, 4))
    ar = (angle - 45) // 90
    for i in numba.prange(resolution_x):
        x = s_x
        y = s_y
        x_step = rays_matrix_steps[angle][i][0]
        y_step = rays_matrix_steps[angle][i][1]
        s = False
        k_sprite = 0
        while mAp[int(x)][int(y)] <= 0:
            k = 0
            run = True
            for k in range(1):
                sp = sprites[k]

                if not s and ar %2==0 and intersects(x - x_step, y - y_step, x, y, sp[0] + sp[2], sp[1], sp[0] - sp[2], sp[1]):
                    s = True
                    x_sprite = x
                    y_sprite = y
                    k_sprite = k
                    break

                if not s and ar %2==1 and intersects(x - x_step, y - y_step, x, y, sp[0], sp[1] + sp[3], sp[0], sp[1] - sp[3]):
                    s = True
                    x_sprite = x
                    y_sprite = y
                    k_sprite = k
                    break


            x += x_step
            y += y_step
        if s:
            dx = sp[2]
            dy = sp[3]
            ox1 = x_sprite - sp[0] + dx
            oy1 = y_sprite - sp[1] + dy
            if ar % 2 == 0:
                oz = ox1 / dx / 2

            else:
                oz = oy1 / dy / 2
            ozz = ar % 2
            code = k_sprite + 500
            rays_sprite[i] = numpy.array(
                [math.sqrt((x_sprite - s_x) ** 2 + (y_sprite - s_y) ** 2) * math.cos(
                    math.radians(i / resolution_x * 90 - 45)), oz,
                 code, ozz])
        if 1:
            ozz = -1
            code = mAp[int(x)][int(y)]
            ox = x % 1
            oy = y % 1
            if abs(ox - 0.5) < abs(oy - 0.5):
                oz = ox
            elif abs(ox - 0.5) > abs(oy - 0.5):
                oz = oy

            rays[i] = numpy.array(
                [math.sqrt((x - s_x) ** 2 + (y - s_y) ** 2) * math.cos(math.radians(i / resolution_x * 90 - 45)), oz, code, ozz])
    return rays, rays_sprite


class Engine3D:

    def __init__(self, x=1.5, y=1.5, angle=0, view_angle=math.radians(90), rotate_step=math.radians(1), step_length=0.1,
                 resolution_x=256, MAP=settings.MAP, res_y=128):
        self.x = x
        self.y = y
        self.angle = angle  # В градусах
        self.view_angle = view_angle
        self.rotate_step = rotate_step
        self.step_length = step_length
        self.resolution_x = resolution_x
        self.map = MAP
        self.res_y = res_y
        self.ray_step = 0.01
        self.rays_matrix_steps = numpy.zeros((360, resolution_x, 2))
        self.ray_angle_step = self.view_angle / self.resolution_x
        for i in range(360):
            current_angle = math.radians(i)
            new_arr = numpy.zeros((resolution_x, 2))
            for j in range(self.resolution_x):
                ray_step = self.ray_step
                cur_ang = current_angle - self.view_angle / 2 + self.ray_angle_step * j
                x = math.cos(cur_ang) * ray_step
                y = math.sin(cur_ang) * ray_step
                new_arr[j] = numpy.array([x, y])
            self.rays_matrix_steps[i] = new_arr
        self.map = self.map.replace("H", str(settings.BRICK_CODE))
        self.map = self.map.replace('W', str(settings.WOOD_CODE))
        self.map = self.map.replace("M", str(settings.METAL_CODE))
        self.map = self.map.replace('S', str(settings.SCIFI_CODE))
        self.map = self.map.replace("D", str(settings.DOOR_CODE))
        self.map = self.map.replace("E", str(settings.END_CODE))
        self.map = self.map.replace(" ", '0')
        self.map = self.map.split('\n')
        self.map = list(map(list, self.map))
        self.map = list(map(lambda e: list(map(int, e)), self.map))
        self.map = numpy.array(self.map)
        print(self.map)
        self.textures = numpy.zeros((100, 128, 128, 3))
        self.render2 = numpy.zeros((resolution_x, res_y, 3))
        self.sprite_textures = numpy.zeros((1000, 4, 128, 64, 3))
        self.sprites = numpy.zeros((1000, 20))
        for i in range(resolution_x):
            for j in range(res_y):
                self.render2[i][j] = numpy.array([200, 200, 200])

    def get_render(self):
        return numba_get_render(self.res_y, self.resolution_x, self.rays_matrix_steps, int(self.angle), self.x, self.y,
                                self.map, self.textures, self.sprites, self.sprite_textures)
    def b(self, x):
        return x
    def load_sprite(self, sprite_code, images, x1, x2, y1, y2, xp):
        self.sprite_textures[sprite_code] = numpy.array(
            [pygame.surfarray.array3d(pygame.image.load(i).convert_alpha()) for i in images])
        self.sprites[sprite_code][0] = x1
        self.sprites[sprite_code][1] = x2
        self.sprites[sprite_code][2] = y1
        self.sprites[sprite_code][3] = y2
        self.sprites[sprite_code][4] = xp
    def trace_ray(self):
        return trace_ray(self.resolution_x, self.rays_matrix_steps, int(self.angle), self.x, self.y, self.map, self.sprites)

    def render(self, surface):
        new_surf = pygame.surfarray.make_surface(self.get_render())
        surface.blit(new_surf, (0, 0))

    def fwd(self, n):
        sx = self.x
        sy = self.y
        self.x += math.cos(math.radians(self.angle)) * n
        self.y += math.sin(math.radians(self.angle)) * n
        if self.map[int(self.x)][int(self.y)] > 0:
            self.x = sx
            self.y = sy


    def left(self, n):
        sx = self.x
        sy = self.y
        self.x += math.cos(math.radians(self.angle - 90)) * n
        self.y += math.sin(math.radians(self.angle - 90)) * n
        if self.map[int(self.x)][int(self.y)] > 0:
            self.x = sx
            self.y = sy


    def right(self, n):
        sx = self.x
        sy = self.y
        self.x += math.cos(math.radians(90 + self.angle)) * n
        self.y += math.sin(math.radians(90 + self.angle)) * n
        if self.map[int(self.x)][int(self.y)] > 0:
            self.x = sx
            self.y = sy


    def back(self, n):
        sx = self.x
        sy = self.y
        self.x -= math.cos(math.radians(self.angle)) * n
        self.y -= math.sin(math.radians(self.angle)) * n
        if self.map[int(self.x)][int(self.y)] > 0:
            self.x = sx
            self.y = sy


    def rotate_left(self, n):
        self.angle -= n
        self.angle %= 360

    def rotate_right(self, n):
        self.angle += n
        self.angle %= 360

    def load_texture(self, texture_code, img):
        surf = pygame.image.load(img).convert()
        self.textures[texture_code] = pygame.surfarray.array3d(surf)
