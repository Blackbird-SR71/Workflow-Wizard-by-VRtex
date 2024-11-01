import bpy
from bl_ui.generic_ui_list import draw_ui_list
import os

#Pannel Set up 
class MyPropGroup(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()

class Debug(bpy.types.Operator):
    bl_idname = "object.debug_operator"
    bl_label = "DEBUG"

    def execute(self, context):
        DebugButton(context)
        return {'FINISHED'}

class Posemode(bpy.types.Operator):
    bl_idname = "object.posemode_operator"
    bl_label = "Pose Mode"

    def execute(self, context):
        PoseModeExecute(context)
        return {'FINISHED'}
    
class Import(bpy.types.Operator):
    bl_idname = "object.import_operator"
    bl_label = "Import Model"

    def execute(self, context):
        ImportExecute(context)
        return {'FINISHED'}    
    
class Export(bpy.types.Operator):
    bl_idname = "object.export_operator"
    bl_label = "Export Model" 

    def execute(self, context):
        ExportExecute(context)
        return {'FINISHED'}   
    

class MyPanel(bpy.types.Panel):
    bl_label = "Workflow Wizard"
    bl_idname = "SCENE_WORKFLOW_WIZARD"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Workflow Wizard"

    def draw(self, context):
        layout = self.layout
        
        #button import
        row = layout.row()
        row.scale_y = 2.0
        row.operator("object.import_operator")
        #button export
        row.scale_y = 2.0
        row.operator("object.export_operator")
        
        layout.label(text=" Modeling tools:")
        #button pose mode
        row = layout.row()
        row.scale_y = 1.5
        row.operator("object.posemode_operator")  
        
        #debug
        row = layout.row()
        row.scale_y = 1.5
        row.operator("object.debug_operator")

tools = bpy.context.workspace.tools
    
classes = [
    MyPropGroup,
    Import,
    Export,
    Posemode,
    MyPanel,
    Debug,
]

class_register, class_unregister = bpy.utils.register_classes_factory(classes)

#Pannel Actions

#Current selected tool of the user
def CurrentActiveTool():
    previousTool = tools.from_space_view3d_mode(bpy.context.mode).idname
    return previousTool

#Pose mode
def PoseModeExecute(context):
    previousTool = 'builtin.selectbox'
    if bpy.context.mode != 'POSE':
        previousTool = CurrentActiveTool()
    bpy.ops.object.posemode_toggle()
    if bpy.context.mode == 'POSE':
        bpy.ops.wm.tool_set_by_id(name='builtin.rotate')
    else:
        bpy.ops.wm.tool_set_by_id(name=previousTool)

#Export FBX with custom import settings      
def ImportExecute(context):
    bpy.ops.import_scene.fbx('INVOKE_DEFAULT',
        automatic_bone_orientation=False,
        use_prepost_rot=False,
        use_anim=False,
        ignore_leaf_bones=True)

#Export FBX with custom export settings    
def ExportExecute(context):
    bpy.ops.export_scene.fbx('INVOKE_DEFAULT',
        object_types={'ARMATURE', 'MESH'},
        use_mesh_modifiers=False,
        add_leaf_bones=True,
        bake_anim=False,
        apply_scale_options='FBX_SCALE_ALL',
        path_mode='AUTO',
        embed_textures=True,
        mesh_smooth_type='OFF',
        use_selection=True)

#Debug Button   
def DebugButton(context):
    bpy.ops.wm.console_toggle()



#Register/Unregister
def register():
    class_register()
    bpy.types.Scene.my_list = bpy.props.CollectionProperty(type=MyPropGroup)
    bpy.types.Scene.my_list_active_index = bpy.props.IntProperty()
    

def unregister():
    class_unregister()
    del bpy.types.Scene.my_list
    del bpy.types.Scene.my_list_active_index
    
register()