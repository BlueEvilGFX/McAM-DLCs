import bpy, os, shutil

from bpy.props import IntProperty, BoolProperty, FloatProperty, StringProperty
from random import random
from ....utils import utils

class PRESET_HELPER_PRESET_OPEN(bpy.types.Operator):
    bl_idname = "presethelper.preset_open"
    bl_label = "open"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        #   get basica dlc / addon data
        dlc_name = os.path.basename(os.path.dirname(__file__))              #   get dlc name
        addon = bpy.context.preferences.addons.get("MC_Assets_Manager")
        if addon:
            addonPropAccess = eval(f'addon.preferences.{dlc_name}_propGroup')

        preset = addonPropAccess.presetsWipEnum

        if preset == '0':
            self.report({'WARNING'}, "please select a valid preset")
            return{'CANCELLED'}
        else:
            addonPath = utils.AddonPathManagement.getDlcDirPath()
            dlcName = os.path.basename(os.path.dirname(__file__))
            file = os.path.join(addonPath, dlcName, "preset_wip", preset+".blend")
            bpy.ops.wm.open_mainfile(filepath=file)
            return{'FINISHED'}

class PRESET_HELPER_PRESET_NEW(bpy.types.Operator):
    bl_idname = "presethelper.preset_new"
    bl_label = "new"
    bl_options = {'REGISTER', 'UNDO'}

    name : StringProperty()

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        self.layout.prop(self, "name")

    def execute(self, context):
        addonPath = utils.AddonPathManagement.getDlcDirPath()
        dlcName = os.path.basename(os.path.dirname(__file__))
        file = os.path.join(addonPath, dlcName, "preset_wip", self.name+".blend")
        bpy.ops.wm.save_as_mainfile(filepath=file)
        return{'FINISHED'}

class PRESET_HELPER_PRESET_REMOVE(bpy.types.Operator):
    bl_idname = "presethelper.preset_remove"
    bl_label = "remove"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        #   get basica dlc / addon data
        dlc_name = os.path.basename(os.path.dirname(__file__))              #   get dlc name
        addon = bpy.context.preferences.addons.get("MC_Assets_Manager")
        if addon:
            addonPropAccess = eval(f'addon.preferences.{dlc_name}_propGroup')

        preset = addonPropAccess.presetsWipEnum

        if preset == '0':
            self.report({'WARNING'}, "please select a valid preset")
            return{'CANCELLED'}
        else:
            addonPath = utils.AddonPathManagement.getDlcDirPath()
            dlcName = os.path.basename(os.path.dirname(__file__))
            file = os.path.join(addonPath, dlcName, "preset_wip", preset+".blend")
            if os.path.exists(file):
                os.remove(file)
                if os.path.exists(file+"1"):
                    os.remove(file+"1")
            return{'FINISHED'}

class PRESET_HELPER_PRESET_FINISH(bpy.types.Operator):
    bl_idname = "presethelper.preset_finish"
    bl_label = "finish"
    bl_options = {'REGISTER', 'UNDO'}
    
    def checkNewName(self, preset, presetX, preDirPath, x):
        #   check name if it already exists --> if yes, increment additional number by one
        path_to_create = os.path.join(preDirPath, presetX)
        path_exists = os.path.exists(path_to_create)
        if path_exists:
            x += 1
            presetX = os.path.splitext(preset)[0] + "_" + str(x) + ".blend"
            return self.checkNewName(preset, presetX, preDirPath, x)
        else:
            return presetX

    def add_file(self, file, context):
            preset_names = utils.AddonPathManagement.getOwnPresets()
            name = os.path.splitext(os.path.basename(file))[0]
            presets_path = utils.AddonPathManagement.getOwnPresetsDirPath()
            destination = os.path.join(presets_path, name+".blend")
            preset = name + ".blend"

            # iterate over all own presets if preset name already exists
            if name+".blend" in preset_names:
                x = 0                                                               #   start by number 0
                presetX = preset                                                    #   reference presetX as preset
                presetX = self.checkNewName(preset, presetX, presets_path, x)       #   check if name already exists
                oldName = os.path.join(presets_path, preset)                    
                newName = os.path.join(presets_path, presetX)
                os.rename(oldName,newName)                                          #   rename blend file which already exists with the new name with number
            shutil.move(file, destination)                                          #   copy preset file with its "normal" name
            utils.AddonReloadManagement.reloadPresetList()
            self.report({'INFO'}, "preset successully added")

    def execute(self, context):
        try:
            bpy.ops.file.pack_all()
        except:
            self.report({'ERROR'}, "images could not be packed correctly")
            return{'CANCELED'}

        #   get basica dlc / addon data
        dlc_name = os.path.basename(os.path.dirname(__file__))              #   get dlc name
        addon = bpy.context.preferences.addons.get("MC_Assets_Manager")
        if addon:
            addonPropAccess = eval(f'addon.preferences.{dlc_name}_propGroup')

        preset = addonPropAccess.presetsWipEnum

        if preset == '0':
            self.report({'WARNING'}, "please select a valid preset")
            return{'FINISHED'}
        else:
            path = utils.AddonPathManagement.getDlcDirPath()
            dlcName = os.path.basename(os.path.dirname(__file__))
            file = os.path.join(path, dlcName, "preset_wip", preset+".blend")
            if os.path.exists(file):
                if os.path.exists(file+"1"):
                    os.remove(file+"1")
                self.add_file(file, context)

            return{'FINISHED'}

class PRESET_HELPER_SUBDIVISION_ADD(bpy.types.Operator):
    bl_idname = "presethelper.subdivision_add"
    bl_label = "add"
    bl_options = {'REGISTER', 'UNDO'}

    subLevelsView : IntProperty(min=0, max=6, default=2)
    subLevelsRender : IntProperty(min=1, max=6, default=3)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "subLevelsView", slider = True)
        layout.prop(self, "subLevelsRender", slider = True)

    def execute(self, context):
        for item in bpy.context.selected_objects:
            for modifier in item.modifiers:
                if modifier.type == "SUBSURF":
                    modifier.levels = self.subLevelsView
                    modifier.render_levels = self.subLevelsRender
                    return{'FINISHED'}

            item.modifiers.new(name = "subdivision", type = "SUBSURF")
            item.modifiers['subdivision'].levels = self.subLevelsView
            item.modifiers['subdivision'].render_levels = self.subLevelsRender
                
        return{'FINISHED'}

class PRESET_HELPER_SUBDIVISION_REMOVE(bpy.types.Operator):
    bl_idname = "presethelper.subdivision_remove"
    bl_label = "remove"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for item in bpy.context.selected_objects:
            for modifier in item.modifiers:
                if modifier.type == "SUBSURF":
                    item.modifiers.remove(modifier)
                
        return{'FINISHED'}

class PRESET_HELPER_SOLIDIFY_ADD(bpy.types.Operator):
    bl_idname = "presethelper.solidify_add"
    bl_label = "add"
    bl_options = {'REGISTER', 'UNDO'}

    thickness : FloatProperty(step = 0.1)
    evenOffSet : BoolProperty()
    offset : FloatProperty(min = -1, max = 1, default = 1)

    random : BoolProperty(default = True)
    randomInfluence : FloatProperty(subtype="PERCENTAGE", min = 0, max = 1, default = 1)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "thickness")
        layout.prop(self, "offset", slider = True)

        row = layout.row(align = True)       
        row.prop(self, "evenOffSet", toggle = True)
        row.prop(self, "random", toggle = True)
        if self.random is True:
            layout.prop(self, "randomInfluence", slider = True)

    def execute(self, context):
        for item in bpy.context.selected_objects:
            randomPercentge = random()
            thickness = self.thickness*((randomPercentge*self.randomInfluence+0.5) if self.random is True else 1)

            for modifier in item.modifiers:
                if modifier.type == "SOLIDIFY":
                    modifier.thickness = thickness
                    modifier.offset = self.offset
                    modifier.use_even_offset = self.evenOffSet
                    return{'FINISHED'}

            item.modifiers.new(name = "solidify", type = "SOLIDIFY")
            item.modifiers['solidify'].thickness = thickness
            item.modifiers['solidify'].offset = self.offset
            item.modifiers['solidify'].use_even_offset = self.evenOffSet
                
        return{'FINISHED'}

class PRESET_HELPER_SOLIDIFY_REMOVE(bpy.types.Operator):
    bl_idname = "presethelper.solidify_remove"
    bl_label = "remove"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for item in bpy.context.selected_objects:
            for modifier in item.modifiers:
                if modifier.type == "SOLIDIFY":
                    item.modifiers.remove(modifier)
                
        return{'FINISHED'}


classes = (
            PRESET_HELPER_PRESET_OPEN,
            PRESET_HELPER_PRESET_NEW,
            PRESET_HELPER_PRESET_REMOVE,
            PRESET_HELPER_PRESET_FINISH,
            PRESET_HELPER_SUBDIVISION_ADD,
            PRESET_HELPER_SUBDIVISION_REMOVE,
            PRESET_HELPER_SOLIDIFY_ADD,
            PRESET_HELPER_SOLIDIFY_REMOVE
          )
          
def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
  
def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)