import bpy, os

#   creating all directories needed for the dlc
def setup():
    main_path = os.path.dirname(os.path.realpath(__file__))
    files_path = os.path.join(main_path, "preset_wip")
    if not os.path.exists(files_path):
        os.mkdir(files_path)
setup()

from bpy.types import PropertyGroup
from bpy.props import EnumProperty
from ....utils import utils

from . import operators

class PreferencesProperty(PropertyGroup):
    def dynamicPresetsWip(self, context):
        pathToAddon = utils.AddonPathManagement.getAddonPath()
        dlcName = os.path.basename(os.path.dirname(__file__))
        path = os.path.join(pathToAddon, "files", "DLCs", dlcName, "preset_wip")

        presets = [os.path.splitext(x)[0] for x  in os.listdir(path) if x.endswith(".blend")]
        enum = [('0', '', '')]

        for x  in presets:
            enum.append((x, x, ''))
        return enum

    presetsWipEnum : EnumProperty(items=dynamicPresetsWip, name="")

class CustomAddonPreferences():
    '''Creates a Panel in the User Preferences -> Addon Preferences'''

    def display(self, element=None):
        pass


class Panel():
    """Creates a Panel for the DLC in McAMUI"""
    def draw(self, context):
        layout = self.layout

        #   get basica dlc / addon data
        dlc_name = os.path.basename(os.path.dirname(__file__))              #   get dlc name
        addon = bpy.context.preferences.addons.get("MC_Assets_Manager")
        if addon:
            addonPropAccess = eval(f'addon.preferences.{dlc_name}_propGroup')

        colWip =  layout.box().column()
        colWip.label(text="Unfinished Presets:")
        colWip.prop(addonPropAccess, "presetsWipEnum")

        row = colWip.row()
        row.operator("presethelper.preset_open")
        row.operator("presethelper.preset_new")

        row = colWip.row()
        row.operator("presethelper.preset_finish")
        row.operator("presethelper.preset_remove")

        subs = layout.box()
        subs.label(text="Subdivisions", icon='MOD_SUBSURF')
        row = subs.row()
        row.operator("presethelper.subdivision_add")
        row.operator("presethelper.subdivision_remove")

        sldfy = layout.box()
        sldfy.label(text="Solidify", icon='MOD_SOLIDIFY')
        row = sldfy.row()
        row.operator("presethelper.solidify_add")
        row.operator("presethelper.solidify_remove")


def register():
    operators.register()

def unregister():
    operators.unregister()