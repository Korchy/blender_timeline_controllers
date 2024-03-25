# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_timeline_controllers

from . import tml_ctrl_gizmoz
from . import tml_ctrl_ops
from . import tml_ctrl_preferences
from .addon import Addon


bl_info = {
    'name': 'TimeLine Controllers',
    'category': 'All',
    'author': 'Nikita Akimov',
    'version': (1, 0, 0),
    'blender': (4, 0, 0),
    'location': 'All areas with the timeline',
    'doc_url': 'https://b3d.interplanety.org/en/blender-add-on-timeline-controllers/',
    'tracker_url': 'https://b3d.interplanety.org/en/blender-add-on-timeline-controllers/',
    'description': 'Additional controllers for convenient change start and end frame numbers on the TimeLine'
}


def register():
    if not Addon.dev_mode():
        tml_ctrl_preferences.register()
        tml_ctrl_ops.register()
        tml_ctrl_gizmoz.register()
    else:
        print('It seems you are trying to use the dev version of the '
              + bl_info['name']
              + ' add-on. It may work not properly. Please download and use the release version')


def unregister():
    if not Addon.dev_mode():
        tml_ctrl_gizmoz.unregister()
        tml_ctrl_ops.unregister()
        tml_ctrl_preferences.unregister()


if __name__ == '__main__':
    register()
