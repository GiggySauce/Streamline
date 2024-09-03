import bpy

# Define the PropertyGroup for camera composition
class CameraComposition(bpy.types.PropertyGroup):
    composition_guide: bpy.props.EnumProperty(
        name="Composition Guide",
        description="Select a composition guide",
        items=[
            ('NONE', 'None', 'No guide selected'),
            ('show_composition_thirds', 'Thirds', 'Thirds'),
            ('show_composition_center', 'Center', 'Center'),
            ('show_composition_golden', 'Golden Ratio', 'Golden Ratio'),
            ('show_composition_golden_tria_a', 'Triangle A', 'Triangle A'),
            ('show_composition_golden_tria_b', 'Triangle B', 'Triangle B'),
        ],
        default='NONE',
        update=lambda self, context: apply_composition_guide(self, context)  # Call the update function
    )

def apply_composition_guide(self, context):
    # Get the selected guide from the property
    guide = self.composition_guide
    
    # Get the active camera
    camera = context.scene.camera
    
    if camera and camera.data:
        # Reset all guides first
        camera.data.show_composition_thirds = False
        camera.data.show_composition_center = False
        camera.data.show_composition_golden = False
        camera.data.show_composition_golden_tria_a = False
        camera.data.show_composition_golden_tria_b = False

        # Apply the selected guide
        if guide == 'show_composition_thirds':
            camera.data.show_composition_thirds = True
        elif guide == 'show_composition_center':
            camera.data.show_composition_center = True
        elif guide == 'show_composition_golden':
            camera.data.show_composition_golden = True
        elif guide == 'show_composition_golden_tria_a':
            camera.data.show_composition_golden_tria_a = True
        elif guide == 'show_composition_golden_tria_b':
            camera.data.show_composition_golden_tria_b = True

# Define the panel to display camera tools
class CameraToolsPanel(bpy.types.Panel):
    bl_label = "Camera Tools"
    bl_idname = "CameraTools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Streamline'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        camera_data = scene.camera.data if scene.camera else None

        box = layout.box()
        box.label(text="Camera List", icon="GROUP")
        
        cameras = [obj for obj in bpy.data.objects if obj.type == 'CAMERA']

        for cam in cameras:
            row = box.row(align=True)
            if cam == scene.camera:
                row.prop(cam, "name", text="", icon='VIEW_CAMERA')
                row.operator("object.select_camera", text="Active", icon='RESTRICT_SELECT_OFF').camera_name = cam.name
            else:
                row.prop(cam, "name", text="", icon='VIEW_CAMERA_UNSELECTED')
                row.operator("object.select_camera", text="Select", icon='RESTRICT_SELECT_ON').camera_name = cam.name

        if camera_data:
            layout.separator()

            # Camera Type
            box = layout.box()
            box.label(text="Camera Type", icon="VIEW_CAMERA")
            box.prop(camera_data, "type", text="Type")

            # Passepartout
            box = layout.box()
            box.label(text="Passepartout", icon="MOD_MASK")
            row = box.row()
            row.prop(camera_data, "show_passepartout", text="Activate")
            row.prop(camera_data, "passepartout_alpha", text="Value")

            # Depth of Field
            box = layout.box()
            box.label(text="Depth of Field", icon="SETTINGS")
            row = box.row()
            row.prop(camera_data.dof, "use_dof", text="Activate")
            if camera_data and camera_data.dof:
                box.prop(camera_data.dof, "focus_object", text="Object")
                box.prop(camera_data.dof, "focus_distance", text="Distance", icon="DRIVER_DISTANCE")
                box.prop(camera_data.dof, "aperture_fstop", text="Aperture F-Stop")
                box.prop(camera_data.dof, "aperture_blades", text="Aperture Blades")
                box.prop(camera_data.dof, "aperture_rotation", text="Aperture Rotation")
                box.prop(camera_data.dof, "aperture_max", text="Aperture Max")
                box.prop(camera_data.dof, "aperture_min", text="Aperture Min")

            # Resolution and Aspect Ratio
            box = layout.box()
            box.label(text="Resolution & Aspect Ratio", icon="IMAGE_DATA")

            # Resolution Controls
            row = box.row()
            row.prop(scene.render, "resolution_x", text="Resolution X")
            row.prop(scene.render, "resolution_y", text="Resolution Y")
            box.prop(scene.render, "resolution_percentage", text="Scale (%)")

            # Flip Resolution Button
            row = box.row()
            row.operator("render.flip_resolution", text="Flip Resolution", icon="FILE_REFRESH")

            # Extras
            box = layout.box()
            box.label(text="Extras", icon="TOOL_SETTINGS")
            box.prop(camera_data, "show_limits", text="Show Limits")
            box.prop(camera_data, "lens", text="Focal Length")

            # Composition List
            if hasattr(scene, 'camera_data'):
                box.prop(scene.camera_data, "composition_guide", text="Guide", icon="MESH_GRID")

class SelectCameraOperator(bpy.types.Operator):
    bl_idname = "object.select_camera"
    bl_label = "Select Camera"
    bl_options = {'REGISTER', 'UNDO'}

    camera_name: bpy.props.StringProperty()

    def execute(self, context):
        camera = bpy.data.objects.get(self.camera_name)
        if camera and camera.type == 'CAMERA':
            context.scene.camera = camera
        return {'FINISHED'}

class FlipResolutionOperator(bpy.types.Operator):
    bl_idname = "render.flip_resolution"
    bl_label = "Flip Resolution"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        res_x = scene.render.resolution_x
        res_y = scene.render.resolution_y
        scene.render.resolution_x = res_y
        scene.render.resolution_y = res_x
        return {'FINISHED'}

def register():
    bpy.utils.register_class(CameraComposition)
    bpy.types.Scene.camera_data = bpy.props.PointerProperty(type=CameraComposition)
    bpy.utils.register_class(CameraToolsPanel)
    bpy.utils.register_class(SelectCameraOperator)
    bpy.utils.register_class(FlipResolutionOperator)

def unregister():
    bpy.utils.unregister_class(CameraToolsPanel)
    bpy.utils.unregister_class(SelectCameraOperator)
    bpy.utils.unregister_class(FlipResolutionOperator)
    bpy.utils.unregister_class(CameraComposition)
    del bpy.types.Scene.camera_data

if __name__ == "__main__":
    register()
