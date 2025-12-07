
# NEED FIX

from copy import copy
import sys
sys.path.append('./')

from Moon.python.Engine import Camera
from Moon.python.Inputs import *
from Moon.python.Window import *
from Moon.python.Rendering.Shapes import *
from Moon.python.Rendering.Text import *
from Moon.python.Vectors import *
from Moon.python.Engine.Camera import *

window = Window(title="Test")
window.set_wait_fps(FPS_VSYNC_CONST)

window_events = WindowEvents()

cm = CameraMachine2D(*window.get_size().xy)
cm_zoom = 1

GRAVITY = Vector2f(0, 0.8)
SIM = True
FRICTION_GROUND = 0.9
SLOUMO = True
DEBUG = True

font = Font(r"Moon\data\fonts\GNF.ttf")
text = Text(font)


BoxRect = RectangleShape(1, 1)
BoxLine = LineShape().init_points()

class BoxTypes(Enum):
    STATIC = 0
    DYNAMIC = 1

class Box:
    def __init__(self, pos: Vector2f, size: Vector2f, type: BoxTypes):
        self.pos = pos
        self.size = size
        self.type = type

        self.speed = Vector2f(0, 0)

    def set_speed(self, speed: Vector2f):
        self.speed = speed
        return self

    def update(self, dt: float):
        if self.type == BoxTypes.DYNAMIC:
            self.speed += GRAVITY * dt
            self.pos += self.speed * dt

    def draw(self):
            #ws = window.get_size(use_cache=True)
            #ps = window.convert_view_coords_to_window_coords(*self.pos.xy, cm.get_view())
            #if ps.x >= 0 and ps.x <= ws.x and ps.y >= 0 and ps.y <= ws.y:

            if self.type == BoxTypes.STATIC:
                BoxRect.set_position(self.pos)
                BoxRect.set_size(self.size)
                BoxRect.set_outline_color(Color(200, 200, 200))
                BoxRect.set_outline_thickness(1)
                BoxRect.set_color(COLOR_TRANSPARENT)

                BoxLine.set_start_point(self.pos)
                BoxLine.set_end_point(self.pos + self.size)
                BoxLine.set_color(Color(200, 200, 200))
                window.draw(BoxLine)
                BoxLine.set_start_point(Vector2f(self.pos.x + self.size.x, self.pos.y))
                BoxLine.set_end_point(Vector2f(self.pos.x, self.pos.y + self.size.y))
                window.draw(BoxLine)
                
                window.draw(BoxRect)

            if self.type == BoxTypes.DYNAMIC:
                BoxRect.set_position(self.pos)
                BoxRect.set_size(self.size)
                BoxRect.set_outline_color(Color(100, 100, 200))
                BoxRect.set_outline_thickness(1)
                BoxRect.set_color(COLOR_TRANSPARENT)
                window.draw(BoxRect)

                BoxLine.set_start_point(self.pos + self.size / 2)
                BoxLine.set_end_point(self.pos + self.size / 2 + self.speed)
                BoxLine.set_color(COLOR_RED)
                window.draw(BoxLine)

        
            

            



class Engine:
    def __init__(self):
        self.__static_boxes: list[Box] = []
        self.__dynamic_boxes: list[Box] = []

    def clear_dynamic_boxes(self):
        self.__dynamic_boxes.clear()

    def clear_static_boxes(self):
        self.__static_boxes.clear()

    def add_box(self, box: Box):
        if box.type == BoxTypes.STATIC:
            self.__static_boxes.append(box)
        elif box.type == BoxTypes.DYNAMIC:
            self.__dynamic_boxes.append(box)

    def render(self):
        for box in self.__static_boxes:
            box.draw()
        for box in self.__dynamic_boxes:
            box.draw()

    def render_debug(self):
        cm.reapply(window)
        for box in self.__dynamic_boxes:
            pos_in_window = window.convert_view_coords_to_window_coords(box.pos.x, box.pos.y, cm.get_view())
            text.set_size(16)
            text.set_position(pos_in_window.x, pos_in_window.y - 40)
            text.set_color(COLOR_BLACK)
            text.set_text(f"Speed: ({box.speed.x:.2f}, {box.speed.y:.2f})\nPos: ({box.pos.x:.2f}, {box.pos.y:.2f})")
            window.draw(text)

    def deleteing(self):
        mp = MouseInterface.get_position_in_window(window)
        mp = window.convert_window_coords_to_view_coords(*mp.xy, cm.get_view())
        for box in self.__static_boxes:
            if (mp.x > box.pos.x and mp.x < box.pos.x + box.size.x and mp.y > box.pos.y and mp.y < box.pos.y + box.size.y):
                if MouseInterface.get_click('right'):
                    self.__static_boxes.remove(box)

        for box in self.__dynamic_boxes:
            if (mp.x > box.pos.x and mp.x < box.pos.x + box.size.x and mp.y > box.pos.y and mp.y < box.pos.y + box.size.y):
                if MouseInterface.get_click('right'):
                    self.__static_boxes.remove(box)
        

    def update(self, dt: float):

        for box in self.__dynamic_boxes:
            # Integrate gravity
            box.speed += GRAVITY * dt

            # Save previous position for motion direction checks
            prev_pos = box.pos.copy()

            grounded = False
            # Move vertically and resolve vertical collisions (separate axis resolution)
            box.pos.y += box.speed.y * dt

            # find minimal vertical penetration among colliders
            min_penetration_y = None
            collider_y = None
            for static_box in self.__static_boxes:
                # compute AABB overlap
                left_a = box.pos.x
                right_a = box.pos.x + box.size.x
                top_a = box.pos.y
                bottom_a = box.pos.y + box.size.y

                left_b = static_box.pos.x
                right_b = static_box.pos.x + static_box.size.x
                top_b = static_box.pos.y
                bottom_b = static_box.pos.y + static_box.size.y

                overlap_x = min(right_a, right_b) - max(left_a, left_b)
                overlap_y = min(bottom_a, bottom_b) - max(top_a, top_b)

                if overlap_x > 0 and overlap_y > 0:
                    # positive penetration
                    if min_penetration_y is None or abs(overlap_y) < abs(min_penetration_y):
                        min_penetration_y = overlap_y
                        collider_y = static_box

            if min_penetration_y is not None and collider_y is not None:
                # If we moved downwards (positive y), push up; if moved upwards, push down
                if box.pos.y > prev_pos.y:
                    # moving down
                    box.pos.y -= min_penetration_y
                    grounded = True
                else:
                    # moving up
                    box.pos.y += min_penetration_y

                # simple bounce / damping
                box.speed.y *= -0.3
                # stop very small velocities to prevent jitter
                if abs(box.speed.y) < 0.01:
                    box.speed.y = 0

            # Move horizontally and resolve horizontal collisions
            prev_pos_x = box.pos.x
            box.pos.x += box.speed.x * dt

            min_penetration_x = None
            collider_x = None
            for static_box in self.__static_boxes:
                left_a = box.pos.x
                right_a = box.pos.x + box.size.x
                top_a = box.pos.y
                bottom_a = box.pos.y + box.size.y

                left_b = static_box.pos.x
                right_b = static_box.pos.x + static_box.size.x
                top_b = static_box.pos.y
                bottom_b = static_box.pos.y + static_box.size.y

                overlap_x = min(right_a, right_b) - max(left_a, left_b)
                overlap_y = min(bottom_a, bottom_b) - max(top_a, top_b)

                if overlap_x > 0 and overlap_y > 0:
                    if min_penetration_x is None or abs(overlap_x) < abs(min_penetration_x):
                        min_penetration_x = overlap_x
                        collider_x = static_box

            if min_penetration_x is not None and collider_x is not None:
                if box.pos.x > prev_pos_x:
                    box.pos.x -= min_penetration_x
                else:
                    box.pos.x += min_penetration_x

                box.speed.x *= -0.3
                if abs(box.speed.x) < 0.01:
                    box.speed.x = 0

            # Apply ground friction when object is contacting the top of a static collider
            if grounded:
                box.speed.x *= FRICTION_GROUND
                if abs(box.speed.x) < 0.01:
                    box.speed.x = 0


ENGINE = Engine()



start_pos = None
start_pos_real = None
box_type = 0
def draw_box():
    global start_pos, start_pos_real, box_type
    if KeyBoardInterface.get_click("enter"):
        print(f"box_type: {box_type}")
        box_type = (box_type + 1) % 2
    if start_pos is None and MouseInterface.get_click('left'):
        start_pos_real = MouseInterface.get_position_in_window(window)
        start_pos = window.convert_window_coords_to_view_coords(*start_pos_real.xy, cm.get_view())
    if MouseInterface.get_press('right') and start_pos is not None:
        start_pos = None
    if start_pos is not None and MouseInterface.get_click('left'):
        end_pos_real = MouseInterface.get_position_in_window(window)
        end_pos = window.convert_window_coords_to_view_coords(*end_pos_real.xy, cm.get_view())

        size = end_pos - start_pos
        if size.x < 0:
            start_pos.x += size.x
        if size.y < 0:
            start_pos.y += size.y
        
        box = Box(start_pos, abs(size), BoxTypes(box_type))
        ENGINE.add_box(box)
        start_pos = None

    

    if start_pos is not None:
        BoxRect.set_outline_color(COLOR_DARK_GREEN)
        
        end_pos_real = MouseInterface.get_position_in_window(window)
        end_pos = window.convert_window_coords_to_view_coords(*end_pos_real.xy, cm.get_view())

        size = end_pos - start_pos
        if size.x < 0:
            start_pos.x += size.x
        if size.y < 0:
            start_pos.y += size.y
        BoxRect.set_position(start_pos)
        BoxRect.set_size(abs(size))
        cm.apply(window)
        window.draw(BoxRect)
        cm.reapply(window)


while window.update(window_events):
    window.clear()

    if window_events.get_type() == WindowEvents.Type.MouseWheelMoved:
        cm_zoom += window_events.get_mouse_wheel() * 0.1 * cm.get_zoom()
        cm.set_target_zoom(cm_zoom)

    cm.update()

    if window.get_resized():
        cm.set_size(*window.get_size().xy)

    if KeyBoardInterface.get_press('w'):
        cm.move(0, -5 * cm.get_zoom())
    if KeyBoardInterface.get_press('s'):
        cm.move(0, 5 * cm.get_zoom())
    if KeyBoardInterface.get_press('a'):
        cm.move(-5 * cm.get_zoom(), 0)
    if KeyBoardInterface.get_press('d'):
        cm.move(5 * cm.get_zoom(), 0)

    draw_box()

    cm.apply(window)

    ENGINE.render()

    if KeyBoardInterface.get_click("space"): SIM = not SIM
    if KeyBoardInterface.get_click("e"): ENGINE.clear_dynamic_boxes()
    if KeyBoardInterface.get_click("r"): ENGINE.clear_static_boxes(); ENGINE.clear_dynamic_boxes()
    if KeyBoardInterface.get_click("l"): SLOUMO = not SLOUMO
    if KeyBoardInterface.get_click("t"): DEBUG = not DEBUG
    if SIM: ENGINE.update(window.get_delta() / (1 if SLOUMO else 10))
    if KeyBoardInterface.get_press("m"):
        ENGINE.add_box(Box(window.convert_window_coords_to_view_coords(*MouseInterface.get_position_in_window(window).xy, cm.get_view()), 
                           Vector2f(20, 20), BoxTypes.DYNAMIC).set_speed(Vector2f.random() * 20))
    
    cm.reapply(window)
    if DEBUG: ENGINE.render_debug()
    ENGINE.deleteing()
    text.set_position(0, window.get_size().y - 35)
    text.set_size(24)
    text.set_text(f"Simulation {"started" if SIM else "stopped"}")
    text.set_color(COLOR_ORANGE if SIM else COLOR_GRAY)
    window.draw(text)

    window.view_info()
    window.display()
