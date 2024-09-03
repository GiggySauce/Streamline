import bpy

class CleanUpPanel(bpy.types.Panel):
    bl_label = "Clean Up"
    bl_idname = "CleanUp"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Streamline'

    def draw(self, context):
        layout = self.layout
        
        # VERTEX GROUPS
        layout.operator("object.clear_vertex_groups", text="Clear Vertex Groups", icon='GROUP_VERTEX')
        
        # MODIFIERS
        layout.operator("object.remove_modifiers", text="Remove Modifiers", icon='MODIFIER')
        
        # SHAPE KEYS
        layout.operator("object.remove_shape_keys", text="Remove Shape Keys", icon='SHAPEKEY_DATA')

class ClearVertexGroupsOperator(bpy.types.Operator):
    bl_idname = "object.clear_vertex_groups"
    bl_label = "Clear Vertex Groups"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type in {'MESH', 'ARMATURE'}:
                obj.vertex_groups.clear()
                self.report({'INFO'}, f"Cleared vertex groups of '{obj.name}'")
        return {'FINISHED'}

class RemoveModifiersOperator(bpy.types.Operator):
    bl_idname = "object.remove_modifiers"
    bl_label = "Remove Modifiers"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type in {'MESH', 'CURVE', 'SURFACE', 'META', 'FONT'}:
                obj.modifiers.clear()
                self.report({'INFO'}, f"Removed modifiers of '{obj.name}'")
        return {'FINISHED'}

class RemoveShapeKeysOperator(bpy.types.Operator):
    bl_idname = "object.remove_shape_keys"
    bl_label = "Remove Shape Keys"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                shape_keys = obj.data.shape_keys
                if shape_keys and shape_keys.key_blocks:
                    # Eliminar shape keys
                    key_blocks = shape_keys.key_blocks[:]
                    for key_block in key_blocks:
                        bpy.ops.object.skp_shape_key_remove(type='DEFAULT')
                    self.report({'INFO'}, f"Removed shape keys of '{obj.name}'")
                else:
                    self.report({'WARNING'}, f"No shape keys found for '{obj.name}'")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(CleanUpPanel)
    bpy.utils.register_class(ClearVertexGroupsOperator)
    bpy.utils.register_class(RemoveModifiersOperator)
    bpy.utils.register_class(RemoveShapeKeysOperator)

def unregister():
    bpy.utils.unregister_class(CleanUpPanel)
    bpy.utils.unregister_class(ClearVertexGroupsOperator)
    bpy.utils.unregister_class(RemoveModifiersOperator)
    bpy.utils.unregister_class(RemoveShapeKeysOperator)

if __name__ == "__main__":
    register()
