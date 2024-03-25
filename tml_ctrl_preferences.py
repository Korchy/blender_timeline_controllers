# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_timeline_controllers

from bpy.types import AddonPreferences
from bpy.props import FloatVectorProperty
from bpy.utils import register_class, unregister_class
from .tml_ctrl import TimeLineControls


class TML_CTRL_preferences(AddonPreferences):
    bl_idname = __package__

    controllers_color: FloatVectorProperty(
        name='Controllers Color',
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0,
        default=(0.0, 1.0, 1.0, 0.7),
        update=lambda self, context: TimeLineControls.update_controllers_color(prefs=self, context=context)

    )

    def draw(self, context):
        layout = self.layout
        layout.prop(
            data=self,
            property='controllers_color'
        )


def register():
    register_class(TML_CTRL_preferences)


def unregister():
    unregister_class(TML_CTRL_preferences)
