import bpy

class RenameDataBlocksPanel(bpy.types.Panel):
    bl_label = "Rename Data-Blocks"
    bl_idname = "RenameDataBlocks"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Streamline'

    def draw(self, context):
        layout = self.layout
        
        # Crear una fila para el botón
        row = layout.row(align=True)
        
        # Crear una columna para el texto y el icono
        col = row.column()
        col.operator("object.rename_data_blocks", text="Rename Data Blocks", icon='FONT_DATA')

class RenameDataBlocksOperator(bpy.types.Operator):
    bl_idname = "object.rename_data_blocks"
    bl_label = "Rename Data Blocks"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Iterar sobre los objetos seleccionados
        for obj in context.selected_objects:
            if obj.type in {'MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'ARMATURE', 'LATTICE', 'POINT_CLOUD'}:
                # Renombrar el bloque de datos según el nombre del objeto
                obj.data.name = obj.name
                self.report({'INFO'}, f"Renamed data block of '{obj.name}'")
        
        return {'FINISHED'}

def register():
    bpy.utils.register_class(RenameDataBlocksPanel)
    bpy.utils.register_class(RenameDataBlocksOperator)

def unregister():
    bpy.utils.unregister_class(RenameDataBlocksPanel)
    bpy.utils.unregister_class(RenameDataBlocksOperator)

if __name__ == "__main__":
    register()
