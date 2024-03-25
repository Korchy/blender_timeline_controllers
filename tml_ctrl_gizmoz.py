# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_timeline_controllers

from bpy.types import Gizmo, GizmoGroup
from bpy.utils import register_class, unregister_class
from mathutils import Vector
from .tml_ctrl import TimeLineControls


class TML_CTRL_GZ_Shape(Gizmo):

    def __init__(self):
        self.custom_shape = None

    def setup(self):
        self.custom_shape = self.new_custom_shape(
            type='TRIS',
            verts=((0, 0), (0, 1), (1, 1), (0, 0), (1, 1), (1, 0))
        )

    def draw(self, context):
        self.draw_custom_shape(self.custom_shape)

    def test_select(self, context, co):
        left_top_corner = self.matrix_world @ Vector((0, 1, 0, 1))
        right_bottom_corner = self.matrix_world @ Vector((1, 0, 0, 1))
        # for SEQUENCE_EDITOR needs to recalculate coordinate, for other - not
        if context.area.type == 'SEQUENCE_EDITOR':
            co = context.region.view2d.region_to_view(co[0], co[1])
        # check if co is inside gizmo shape (left_top and right_bottom coordinates)
        if ((left_top_corner[0] <= co[0] <= right_bottom_corner[0])
                and (right_bottom_corner[1] <= co[1] <= left_top_corner[1])):
            return 0
        else:
            return -1


class TIMELINE_GG_SE_Handlers(GizmoGroup):
    bl_label = 'Sequence Editor Gizmo Handles'
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'WINDOW'
    bl_options = {'PERSISTENT', 'SHOW_MODAL_ALL', 'SCALE'}

    def setup(self, context):
        # left gizmo control
        left_gizmo = self.gizmos.new('TML_CTRL_GZ_Shape')
        left_gizmo.color = TimeLineControls.controllers_color(context=context)
        left_gizmo.color_highlight = left_gizmo.color
        left_gizmo.alpha = 0.7
        left_gizmo.alpha_highlight = 0.9
        left_gizmo.use_draw_modal = True
        left_gizmo.use_draw_scale = False
        op = left_gizmo.target_set_operator('tml_ctrl.process_controllers')
        setattr(op, 'mode', 'START')
        TimeLineControls.se_left_controller = left_gizmo
        # right gizmo control
        right_gizmo = self.gizmos.new('TML_CTRL_GZ_Shape')
        right_gizmo.color = TimeLineControls.controllers_color(context=context)
        right_gizmo.color_highlight = right_gizmo.color
        right_gizmo.alpha = 0.7
        right_gizmo.alpha_highlight = 0.9
        right_gizmo.use_draw_modal = True
        right_gizmo.use_draw_scale = False
        op = right_gizmo.target_set_operator('tml_ctrl.process_controllers')
        setattr(op, 'mode', 'END')
        TimeLineControls.se_right_controller = right_gizmo

    def draw_prepare(self, context):
        # get area coordinates of frame_start and frame_end
        frame_start_co = context.region.view2d.region_to_view(context.scene.frame_start, 0.0)
        frame_start = context.region.view2d.view_to_region(frame_start_co[0], 0, clip=False)[0]
        frame_end_co = context.region.view2d.region_to_view(context.scene.frame_end, 0.0)
        frame_end = context.region.view2d.view_to_region(frame_end_co[0], 0, clip=False)[0]
        # correct size by UI
        width = 1 * context.preferences.system.ui_scale
        height = 2 * context.preferences.system.ui_scale
        # left gizmo
        TimeLineControls.se_left_controller.matrix_basis[0][3] = frame_start
        TimeLineControls.se_left_controller.matrix_basis[1][3] = 0
        TimeLineControls.se_left_controller.matrix_basis[0][0] = width
        TimeLineControls.se_left_controller.matrix_basis[1][1] = height
        # right gizmo
        TimeLineControls.se_right_controller.matrix_basis[0][3] = frame_end
        TimeLineControls.se_right_controller.matrix_basis[1][3] = 0
        TimeLineControls.se_right_controller.matrix_basis[0][0] = width
        TimeLineControls.se_right_controller.matrix_basis[1][1] = height


class TIMELINE_GG_DS_Handlers(GizmoGroup):
    bl_label = 'Dope Sheet Gizmo Handles'
    bl_space_type = 'DOPESHEET_EDITOR'
    bl_region_type = 'WINDOW'
    bl_options = {'PERSISTENT', 'SHOW_MODAL_ALL', 'SCALE'}

    def setup(self, context):
        # left gizmo control
        left_gizmo = self.gizmos.new('TML_CTRL_GZ_Shape')
        left_gizmo.color = TimeLineControls.controllers_color(context=context)
        left_gizmo.color_highlight = left_gizmo.color
        left_gizmo.alpha = 0.7
        left_gizmo.alpha_highlight = 0.9
        left_gizmo.use_draw_modal = True
        left_gizmo.use_draw_scale = False
        op = left_gizmo.target_set_operator('tml_ctrl.process_controllers')
        setattr(op, 'mode', 'START')
        TimeLineControls.de_left_controller = left_gizmo
        # right gizmo control
        right_gizmo = self.gizmos.new('TML_CTRL_GZ_Shape')
        right_gizmo.color = TimeLineControls.controllers_color(context=context)
        right_gizmo.color_highlight = right_gizmo.color
        right_gizmo.alpha = 0.7
        right_gizmo.alpha_highlight = 0.9
        right_gizmo.use_draw_modal = True
        right_gizmo.use_draw_scale = False
        op = right_gizmo.target_set_operator('tml_ctrl.process_controllers')
        setattr(op, 'mode', 'END')
        TimeLineControls.de_right_controller = right_gizmo

    def draw_prepare(self, context):
        # get area coordinates of frame_start and frame_end
        frame_start = context.region.view2d.view_to_region(context.scene.frame_start, 0, clip=False)[0]
        frame_end = context.region.view2d.view_to_region(context.scene.frame_end, 0, clip=False)[0]
        # correct size by UI
        width = 5 * context.preferences.system.ui_scale
        height = 35 * context.preferences.system.ui_scale
        # left gizmo
        TimeLineControls.de_left_controller.matrix_basis[0][3] = frame_start - 0.5 * width
        TimeLineControls.de_left_controller.matrix_basis[1][3] = 0
        TimeLineControls.de_left_controller.matrix_basis[0][0] = width
        TimeLineControls.de_left_controller.matrix_basis[1][1] = height
        # right gizmo
        TimeLineControls.de_right_controller.matrix_basis[0][3] = frame_end - 0.5 * width
        TimeLineControls.de_right_controller.matrix_basis[1][3] = 0
        TimeLineControls.de_right_controller.matrix_basis[0][0] = width
        TimeLineControls.de_right_controller.matrix_basis[1][1] = height


def register():
    register_class(TML_CTRL_GZ_Shape)
    register_class(TIMELINE_GG_SE_Handlers)
    register_class(TIMELINE_GG_DS_Handlers)


def unregister():
    unregister_class(TIMELINE_GG_DS_Handlers)
    unregister_class(TIMELINE_GG_SE_Handlers)
    unregister_class(TML_CTRL_GZ_Shape)
