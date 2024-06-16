bl_info = {
        "name": "ModiFlex",
        "description": "Simplifies object management by clearing vertex groups, modifiers, and shapekeys with ease.",
        "author": "Darber",
        "version": (1, 1),
        "blender": (4, 1, 0),
        "location": "3D View > Properties > Tool > ModiFlex",
        "warning": "", # used for warning icon and text in add-ons panel
        "tracker_url": "https://github.com/GiggySauce/ModiFlex/issues",
        "support": "COMMUNITY",
        "category": "Tools"
        }

import bpy

class OBJECT_PT_ClearVertexGroupsPanel(bpy.types.Panel):
    bl_label = "Object Properties Assistant"
    bl_idname = "OBJECT_PT_clear_vertex_groups"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tools'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.clear_vertex_groups", text="Clear All Vertex Groups", icon='GROUP_VERTEX')
        layout.operator("object.clear_modifiers", text="Clear All Modifiers", icon='MODIFIER')
        layout.operator("object.clear_shapekeys", text="Clear All Shapekeys", icon='SHAPEKEY_DATA')


class ClearVertexGroupsOperator(bpy.types.Operator):
    """Clears all vertex groups from selected mesh objects"""
    bl_idname = "object.clear_vertex_groups"
    bl_label = "Clear All Vertex Groups"
    
    def execute(self, context):
        total_deleted = 0  # Inicializamos el contador
        
        # Obtener la lista de objetos seleccionados en la escena
        selected_objects = context.selected_objects
        
        # Iterar sobre cada objeto seleccionado
        for obj in selected_objects:
            # Verificar si el objeto tiene datos de malla (es un objeto de malla)
            if obj.type == 'MESH':
                # Obtener la cantidad de grupos de vértices antes de borrarlos
                num_groups_before = len(obj.vertex_groups)
                
                # Limpiar todos los grupos de vértices del objeto
                obj.vertex_groups.clear()
                
                # Incrementar el contador con la cantidad de grupos eliminados en este objeto
                total_deleted += num_groups_before
                
                self.report({'INFO'}, "All vertex groups deleted from object '{}'.".format(obj.name))
            else:
                self.report({'WARNING'}, "Skipping object '{}' as it is not a mesh.".format(obj.name))
        
        # Mostrar el mensaje con la cantidad total de grupos eliminados
        self.report({'INFO'}, "Total vertex groups deleted: {}.".format(total_deleted))
        
        return {'FINISHED'}


class ClearModifiersOperator(bpy.types.Operator):
    """Clears all modifiers from selected objects"""
    bl_idname = "object.clear_modifiers"
    bl_label = "Clear All Modifiers"
    
    def execute(self, context):
        total_deleted = 0  # Inicializamos el contador
        
        # Obtener la lista de objetos seleccionados en la escena
        selected_objects = context.selected_objects
        
        # Iterar sobre cada objeto seleccionado
        for obj in selected_objects:
            # Obtener la cantidad de modificadores antes de borrarlos
            num_modifiers_before = len(obj.modifiers)
            
            # Limpiar todos los modificadores del objeto
            obj.modifiers.clear()
            
            # Incrementar el contador con la cantidad de modificadores eliminados en este objeto
            total_deleted += num_modifiers_before
            
            self.report({'INFO'}, "All modifiers deleted from object '{}'.".format(obj.name))
        
        # Mostrar el mensaje con la cantidad total de modificadores eliminados
        self.report({'INFO'}, "Total modifiers deleted: {}.".format(total_deleted))
        
        return {'FINISHED'}


class ClearShapekeysOperator(bpy.types.Operator):
    """Clears all shapekeys from selected objects"""
    bl_idname = "object.clear_shapekeys"
    bl_label = "Clear All Shapekeys"
    
    def execute(self, context):
        total_deleted = 0  # Inicializamos el contador
        
        # Obtener la lista de objetos seleccionados en la escena
        selected_objects = context.selected_objects
        
        # Iterar sobre cada objeto seleccionado
        for obj in selected_objects:
            # Verificar si el objeto tiene shapekeys
            if obj.data.shape_keys:
                # Obtener la cantidad de shapekeys antes de borrarlos
                num_shapekeys_before = len(obj.data.shape_keys.key_blocks)
                
                # Borrar todos los shapekeys del objeto
                for key in obj.data.shape_keys.key_blocks:
                    obj.shape_key_remove(key)
                
                # Incrementar el contador con la cantidad de shapekeys eliminados en este objeto
                total_deleted += num_shapekeys_before
                
                self.report({'INFO'}, "All shapekeys deleted from object '{}'.".format(obj.name))
            else:
                self.report({'WARNING'}, "Skipping object '{}' as it does not have shapekeys.".format(obj.name))
        
        # Mostrar el mensaje con la cantidad total de shapekeys eliminados
        self.report({'INFO'}, "Total shapekeys deleted: {}.".format(total_deleted))
        
        return {'FINISHED'}


def register():
    bpy.utils.register_class(OBJECT_PT_ClearVertexGroupsPanel)
    bpy.utils.register_class(ClearVertexGroupsOperator)
    bpy.utils.register_class(ClearModifiersOperator)
    bpy.utils.register_class(ClearShapekeysOperator)


def unregister():
    bpy.utils.unregister_class(OBJECT_PT_ClearVertexGroupsPanel)
    bpy.utils.unregister_class(ClearVertexGroupsOperator)
    bpy.utils.unregister_class(ClearModifiersOperator)
    bpy.utils.unregister_class(ClearShapekeysOperator)


if __name__ == "__main__":
    register()
