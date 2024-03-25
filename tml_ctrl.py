# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_timeline_controllers

class TimeLineControls:

    se_left_controller = None
    se_right_controller = None
    de_left_controller = None
    de_right_controller = None

    @classmethod
    def update_controllers_color(cls, prefs, context):
        # update controllers color
        if cls.se_left_controller:
            cls.se_left_controller.color = prefs.controllers_color[:3]
            cls.se_left_controller.color_highlight = cls.se_left_controller.color
        if cls.se_right_controller:
            cls.se_right_controller.color = prefs.controllers_color[:3]
            cls.se_right_controller.color_highlight = cls.se_right_controller.color
        if cls.de_left_controller:
            cls.de_left_controller.color = prefs.controllers_color[:3]
            cls.de_left_controller.color_highlight = cls.de_left_controller.color
        if cls.de_right_controller:
            cls.de_right_controller.color = prefs.controllers_color[:3]
            cls.de_right_controller.color_highlight = cls.de_right_controller.color

    @staticmethod
    def controllers_color(context):
        # get controllers color from preferences
        return context.preferences.addons[__package__].preferences.controllers_color[:3]
