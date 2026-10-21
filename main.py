import glfw
from OpenGL.GL import *
import glm

from camera import Camera
from shader import Shader
from obj_loader import load_obj, parse_mtl, load_texture

MODEL_PATH = "assets/pedestal.obj"
MTL_PATH = "assets/pedestal.mtl"
TEXTURE_PATH = "assets/pedestal_diffuse.png"

obj_pos = glm.vec3(0.0, 0.0, 0.0)
obj_rot = glm.vec3(0.0, 0.0, 0.0)
obj_scale = glm.vec3(1.0, 1.0, 1.0)

camera = Camera(position=(0.0, 2.5, 6.0), yaw=-90.0, pitch=-15.0, fov=45.0)
keys = {}
mouse_active = False
last_mouse_x = 0.0
last_mouse_y = 0.0
use_texture = True

# 3 luzes (Key, Fill, Back)
lights = [
    {"enabled": True, "name": "Key Light (Principal)"},
    {"enabled": True, "name": "Fill Light (Preenchimento)"},
    {"enabled": True, "name": "Back Light (Contra-luz)"}
]


def update_automatic_lights(center, scale_factor):
    s = scale_factor

    # Key Light
    lights[0]["position"] = [center.x + 3.0 * s, center.y + 4.5 * s, center.z + 3.5 * s]
    lights[0]["ambient"] = [0.08, 0.08, 0.08]
    lights[0]["diffuse"] = [1.0, 0.95, 0.85]
    lights[0]["specular"] = [1.0, 1.0, 1.0]
    lights[0]["constant"] = 1.0
    lights[0]["linear"] = 0.09
    lights[0]["quadratic"] = 0.032

    # Fill Light
    lights[1]["position"] = [center.x - 3.5 * s, center.y + 3.0 * s, center.z + 2.0 * s]
    lights[1]["ambient"] = [0.04, 0.04, 0.06]
    lights[1]["diffuse"] = [0.4, 0.45, 0.6]
    lights[1]["specular"] = [0.35, 0.4, 0.5]
    lights[1]["constant"] = 1.0
    lights[1]["linear"] = 0.09
    lights[1]["quadratic"] = 0.032

    # Back Light
    lights[2]["position"] = [center.x + 0.0 * s, center.y + 4.0 * s, center.z - 4.0 * s]
    lights[2]["ambient"] = [0.02, 0.02, 0.03]
    lights[2]["diffuse"] = [0.85, 0.60, 0.35]
    lights[2]["specular"] = [0.9, 0.7, 0.5]
    lights[2]["constant"] = 1.0
    lights[2]["linear"] = 0.09
    lights[2]["quadratic"] = 0.032


def key_callback(window, key, scancode, action, mods):
    global use_texture

    if action == glfw.PRESS:
        if key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)
        elif key == glfw.KEY_1:
            lights[0]["enabled"] = not lights[0]["enabled"]
            print(f"Luz 1: {'ON' if lights[0]['enabled'] else 'OFF'}")
        elif key == glfw.KEY_2:
            lights[1]["enabled"] = not lights[1]["enabled"]
            print(f"Luz 2: {'ON' if lights[1]['enabled'] else 'OFF'}")
        elif key == glfw.KEY_3:
            lights[2]["enabled"] = not lights[2]["enabled"]
            print(f"Luz 3: {'ON' if lights[2]['enabled'] else 'OFF'}")
        elif key == glfw.KEY_X:
            use_texture = not use_texture
            print(f"Textura: {'ON' if use_texture else 'OFF'}")

    if action == glfw.PRESS:
        keys[key] = True
    elif action == glfw.RELEASE:
        keys[key] = False


def mouse_button_callback(window, button, action, mods):
    global mouse_active, last_mouse_x, last_mouse_y
    if button == glfw.MOUSE_BUTTON_RIGHT:
        if action == glfw.PRESS:
            mouse_active = True
            last_mouse_x, last_mouse_y = glfw.get_cursor_pos(window)
        elif action == glfw.RELEASE:
            mouse_active = False


def cursor_pos_callback(window, xpos, ypos):
    global last_mouse_x, last_mouse_y
    if mouse_active:
        dx = xpos - last_mouse_x
        dy = last_mouse_y - ypos
        last_mouse_x, last_mouse_y = xpos, ypos
        camera.process_mouse(dx, dy)


def framebuffer_size_callback(window, width, height):
    if height > 0:
        glViewport(0, 0, width, height)


def process_camera_inputs(dt):
    if keys.get(glfw.KEY_W, False): camera.process_keyboard("FORWARD", dt)
    if keys.get(glfw.KEY_S, False): camera.process_keyboard("BACKWARD", dt)
    if keys.get(glfw.KEY_A, False): camera.process_keyboard("LEFT", dt)
    if keys.get(glfw.KEY_D, False): camera.process_keyboard("RIGHT", dt)
    if keys.get(glfw.KEY_E, False): camera.process_keyboard("UP", dt)
    if keys.get(glfw.KEY_Q, False): camera.process_keyboard("DOWN", dt)


def main():
    if not glfw.init():
        return

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(1280, 720, "Computação Gráfica - Atividade Parcial", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_cursor_pos_callback(window, cursor_pos_callback)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

    glEnable(GL_DEPTH_TEST)
    glClearColor(0.08, 0.08, 0.12, 1.0)

    shader = Shader("shaders/vertex_shader.glsl", "shaders/fragment_shader.glsl")

    vao, vbo, vertex_count = load_obj(MODEL_PATH)
    material = parse_mtl(MTL_PATH)
    texture_id = load_texture(TEXTURE_PATH)

    print("Aplicação iniciada. Controles: W,A,S,D | Teclas 1-3 (Luzes) | X (Textura) | ESC (Sair)")

    last_time = glfw.get_time()

    while not glfw.window_should_close(window):
        current_time = glfw.get_time()
        dt = current_time - last_time
        last_time = current_time

        process_camera_inputs(dt)

        scale_val = max(obj_scale.x, obj_scale.y, obj_scale.z)
        update_automatic_lights(obj_pos, scale_val)

        l_str = f"L1:{'ON' if lights[0]['enabled'] else 'OFF'} L2:{'ON' if lights[1]['enabled'] else 'OFF'} L3:{'ON' if lights[2]['enabled'] else 'OFF'}"
        glfw.set_window_title(window, f"Atividade Parcial | {l_str} | Textura: {'ON' if use_texture else 'OFF'}")

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        shader.use()

        w, h = glfw.get_framebuffer_size(window)
        glViewport(0, 0, w, h)
        aspect = w / max(1, h)
        shader.set_mat4("projection", camera.get_projection_matrix(aspect))
        shader.set_mat4("view", camera.get_view_matrix())
        shader.set_vec3("viewPos", camera.position)

        for i, light in enumerate(lights):
            shader.set_bool(f"lights[{i}].enabled", light["enabled"])
            shader.set_vec3(f"lights[{i}].position", light["position"])
            shader.set_vec3(f"lights[{i}].ambient", light["ambient"])
            shader.set_vec3(f"lights[{i}].diffuse", light["diffuse"])
            shader.set_vec3(f"lights[{i}].specular", light["specular"])
            shader.set_float(f"lights[{i}].constant", light["constant"])
            shader.set_float(f"lights[{i}].linear", light["linear"])
            shader.set_float(f"lights[{i}].quadratic", light["quadratic"])

        shader.set_bool("useTexture", use_texture)

        model = glm.mat4(1.0)
        model = glm.translate(model, obj_pos)
        model = glm.rotate(model, glm.radians(obj_rot.x), glm.vec3(1, 0, 0))
        model = glm.rotate(model, glm.radians(obj_rot.y), glm.vec3(0, 1, 0))
        model = glm.rotate(model, glm.radians(obj_rot.z), glm.vec3(0, 0, 1))
        model = glm.scale(model, obj_scale)
        shader.set_mat4("model", model)

        shader.set_vec3("material.Ka", material["Ka"])
        shader.set_vec3("material.Kd", material["Kd"])
        shader.set_vec3("material.Ks", material["Ks"])
        shader.set_float("material.shininess", material["shininess"])

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        shader.set_int("texture_diffuse", 0)

        glBindVertexArray(vao)
        glDrawArrays(GL_TRIANGLES, 0, vertex_count)
        glBindVertexArray(0)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glDeleteVertexArrays(1, [vao])
    glDeleteBuffers(1, [vbo])
    glDeleteTextures(1, [texture_id])
    glfw.destroy_window(window)
    glfw.terminate()


if __name__ == "__main__":
    main()
