# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_timeline_controllers

from bpy.props import EnumProperty, IntProperty
from bpy.types import Operator
from bpy.utils import register_class, unregister_class


class TML_CTRL_OT_process_controllers(Operator):
    bl_idname = 'tml_ctrl.process_controllers'
    bl_label = 'Process Controllers'
    bl_description = 'Process Controllers'
    bl_options = {'GRAB_CURSOR_X', 'BLOCKING', 'UNDO'}

    offset: IntProperty(
        name='Offset',
        options={'SKIP_SAVE'},
    )

    mode: EnumProperty(
        name='Mode',
        items=(
            ('START', 'Start', 'Start frame'),
            ('END', 'End', 'End frame')
        ),
        default='START',
        options={'SKIP_SAVE'}
    )

    def __init__(self):
        self.frame_end = None
        self.frame_start = None
        self.start_mouse_co = None

    def invoke(self, context, event):
        region = context.region
        self.start_mouse_co = region.view2d.region_to_view(
            x=event.mouse_region_x,
            y=event.mouse_region_y
        )
        self.frame_start = context.scene.frame_start
        self.frame_end = context.scene.frame_end
        # run as modal
        context.window.cursor_modal_set('MOVE_X')
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        # Cancel
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            context.scene.frame_start = self.frame_start
            context.scene.frame_end = self.frame_end
            context.window.cursor_modal_restore()
            return {'CANCELLED'}
        # Finish
        if event.type in {'LEFTMOUSE'} and event.value in {'RELEASE'}:
            context.window.cursor_modal_restore()
            return {'FINISHED'}
        # Update
        if event.type in {'MOUSEMOVE'}:
            # Recalculate new offset
            region = context.region
            mouse_co = region.view2d.region_to_view(
                x=event.mouse_region_x,
                y=event.mouse_region_y
            )
            offset = int(mouse_co[0] - self.start_mouse_co[0])
            if offset != self.offset:
                self.offset = offset
                self.execute(context)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        if self.mode == 'START':
            context.scene.frame_start = min(self.frame_start + self.offset, self.frame_end)
        else:  # 'END'
            context.scene.frame_end = max(self.frame_end + self.offset, self.frame_start)
        return {'FINISHED'}


def register():
    register_class(TML_CTRL_OT_process_controllers)


def unregister():
    unregister_class(TML_CTRL_OT_process_controllers)
