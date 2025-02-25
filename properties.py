import bpy
from bpy.types import Context


# ==============================================================================
# SECTION: Callbacks
# ==============================================================================
# Description: Callback functions to handle value changes of properties

def populate_classes(self, context: Context) -> list[tuple[str,str,str]]:
    '''
    Set items for "Current Class Enum" given the list of classes

    Args
        context: Current context

    Returns
        A list of items for the Current Class Enum
    '''
    
    enum_items = [] 

    for classification_class in context.scene.bat_properties.classification_classes:        
        name = classification_class.name
        item = (name, name, name)  # (ID, name, value)
        enum_items.append(item)
        
    return enum_items


def update_current_class_params(self, context: Context) -> None:
    '''
    Update values of current class params when the current class is changed

    Args
        context: Current context
    '''
    # Get the index of current class
    index = context.scene.bat_properties.classification_classes.find(context.scene.bat_properties.current_class)

    # Set current class params
    context.scene.bat_properties.current_class_color = context.scene.bat_properties.classification_classes[index].mask_color
    context.scene.bat_properties.current_class_objects = context.scene.bat_properties.classification_classes[index].objects
    context.scene.bat_properties.current_class_is_instances = context.scene.bat_properties.classification_classes[index].is_instances


def update_classification_class_color(self, context: Context) -> None:
    '''
    Update color of class in the list of classes if the color for the current class is changed

    Args
        context: Current context
    '''
    # Get the index of current class
    index = context.scene.bat_properties.classification_classes.find(context.scene.bat_properties.current_class)

    # Set color of current class
    context.scene.bat_properties.classification_classes[index].mask_color = context.scene.bat_properties.current_class_color


def update_classification_class_objects(self, context: Context) -> None:
    '''
    Update associated collection of class in the list of classes if the associated collection for the current class is changed

    Args
        context: Current context
    '''
    # Get the index of current class
    index = context.scene.bat_properties.classification_classes.find(context.scene.bat_properties.current_class)

    # Set collection for current class
    context.scene.bat_properties.classification_classes[index].objects = context.scene.bat_properties.current_class_objects


def update_classification_class_is_instances(self, context: Context) -> None:
    '''
    Update instance segmentation setup of class in the list of classes if the instance segmentation setup for the current class is changed

    Args
        context: Current context
    '''
    # Get the index of current class
    index = context.scene.bat_properties.classification_classes.find(context.scene.bat_properties.current_class)

    # Set instance segmentation on or off for current class
    context.scene.bat_properties.classification_classes[index].is_instances = context.scene.bat_properties.current_class_is_instances


def update_camera_calibration_file(self, context: Context) -> None:
    '''
    Update camera intrinsics and lens distortion parameters
    '''
    bpy.ops.bat.import_camera_data()
    

def get_sensor_width(self) -> float:
    '''
    Getter for Camera sensor_width
    '''
    if 'sensor_width' not in self:
        return bpy.data.cameras[bpy.context.scene.camera.data.name].sensor_width
    return self['sensor_width']

def set_sensor_width(self, value: float) -> None:
    '''
    Setter for Camera sensor_width
    '''
    scene = bpy.context.scene
    camera = bpy.data.cameras[bpy.context.scene.camera.data.name]
    camera.type = 'PERSP'
    camera.lens_unit = 'MILLIMETERS'
    camera.lens = (scene.bat_properties.camera.fx/scene.render.resolution_x)*value
    bpy.data.cameras[bpy.context.scene.camera.data.name].sensor_width = value
    self['sensor_width'] = value

def get_fx(self) -> float:
    '''
    Getter for Camera fx
    '''
    if 'fx' not in self:
        return (24/36)*bpy.context.scene.render.resolution_x  # Default focal length (mm) / sensor width (mm) * image width (pixel)
    return self['fx']

def set_fx(self, value: float) -> None:
    '''
    Setter for Camera fx
    '''
    scene = bpy.context.scene
    camera = bpy.data.cameras[bpy.context.scene.camera.data.name]
    camera.type = 'PERSP'
    camera.lens_unit = 'MILLIMETERS'
    camera.lens = (value/scene.render.resolution_x)*scene.bat_properties.camera.sensor_width
    self['fx'] = value


def get_fy(self) -> float:
    '''
    Getter for Camera fy
    '''
    if 'fy' not in self:
        return (24/36)*bpy.context.scene.render.resolution_x  # Same as fx (pixel aspect = 1)
    return self['fy']

def set_fy(self, value: float) -> None:
    '''
    Setter for Camera fy
    '''
    self['fy'] = value

def get_cx(self) -> float:
    '''
    Getter for Camera cx
    '''
    if 'cx' not in self:
        return bpy.context.scene.render.resolution_x/2
    return self['cx']

def set_cx(self, value: float) -> None:
    '''
    Setter for Camera cx
    '''
    self['cx'] = value

def get_cy(self) -> float:
    '''
    Getter for Camera cy
    '''
    if 'cy' not in self:
        return bpy.context.scene.render.resolution_y/2
    return self['cy']

def set_cy(self, value: float) -> None:
    '''
    Setter for Camera cy
    '''
    self['cy'] = value



# ==============================================================================
# SECTION: Camera Properties
# ==============================================================================
# Description: Properties for the BAT Camera

class BAT_Camera(bpy.types.PropertyGroup):
    '''
    Property group describing a camera
    '''

    calibration_file: bpy.props.StringProperty(
        name = 'calibration_file',
        description = 'Import camera calibration data',
        subtype = 'FILE_PATH',
        update = update_camera_calibration_file,
    )


    sensor_width: bpy.props.FloatProperty(
        name="sensor_width",
        description="Width of the CCD sensor in millimeters",
        min = 0,
        soft_min = 0,
        max = 500,
        soft_max = 500,
        get = get_sensor_width,
        set = set_sensor_width,
    )

    # Intrinsics
    fx: bpy.props.FloatProperty(
        name="fx",
        description="Focal length X (in pixel units)",
        min = 0,
        soft_min = 0,
        get = get_fx,
        set = set_fx,
    )
    fy: bpy.props.FloatProperty(
        name="fy",
        description="Focal length Y (in pixel units)",
        min = 0,
        soft_min = 0,
        get = get_fy,
        set = set_fy,
    )
    cx: bpy.props.FloatProperty(
        name="cx",
        description="Optical Center X (in pixel units)",
        get = get_cx,
        set = set_cx,
    )
    cy: bpy.props.FloatProperty(
        name="cy",
        description="Optical Center Y (in pixel units)",
        get = get_cy,
        set = set_cy,
    )

    # Lens distortion
    p1: bpy.props.FloatProperty(
        name="p1",
        description="Lens distortion p1 parameter",
    )
    p2: bpy.props.FloatProperty(
        name="p2",
        description="Lens distortion p2 parameter",
    )
    k1: bpy.props.FloatProperty(
        name="k1",
        description="Lens distortion k1 parameter",
    )
    k2: bpy.props.FloatProperty(
        name="k2",
        description="Lens distortion k2 parameter",
    )
    k3: bpy.props.FloatProperty(
        name="k3",
        description="Lens distortion k3 parameter",
    )
    k4: bpy.props.FloatProperty(
        name="k4",
        description="Lens distortion k4 parameter",
    )



# ==============================================================================
# SECTION: Class Properties
# ==============================================================================
# Description: Properties for a single class

class BAT_ClassificationClass(bpy.types.PropertyGroup):
    '''
    Property group describing a single classification class
    '''

    name: bpy.props.StringProperty(
        name="class_name",
        description="Identifier for the class"
    )
    mask_color: bpy.props.FloatVectorProperty(
        name="object_color",
        subtype='COLOR',
        size=4,
        default=(1.0, 1.0, 1.0, 1.0),
        min=0.0, max=1.0,
        description="Color used for representing the class on the annotated image"
    )
    objects: bpy.props.StringProperty(
        name="class_objects",
        description="Name of a collection containing objects belonging to this class"
    )
    is_instances: bpy.props.BoolProperty(
        name="is_instances",
        description="If true the objects in the associated collection will be handled as instances"
    )



# ==============================================================================
# SECTION: Visualization Properties
# ==============================================================================
# Description: Properties for visualization/user interaction (current/active class)

class BAT_Properties(bpy.types.PropertyGroup):
    '''
    Property group for visualizing/editing class params
    '''

    # Collection of all classes (list of classes)
    classification_classes: bpy.props.CollectionProperty(type=BAT_ClassificationClass)

    # The currently selected class
    current_class: bpy.props.EnumProperty(items=populate_classes, update=update_current_class_params)

    # Properties of currently selected class
    current_class_color: bpy.props.FloatVectorProperty(
        name="Mask color",
        subtype='COLOR',
        size=4,
        default=(0.0, 0.0, 0.0, 1.0),
        min=0.0, max=1.0,
        description="Color value of the current class for the segmentation mask",
        update=update_classification_class_color
    )
    current_class_objects: bpy.props.StringProperty(
        name="Objects' collection",
        description="Collection containing all objects belonging to the current class",
        update=update_classification_class_objects
    )
    current_class_is_instances: bpy.props.BoolProperty(
        name="Is instances?",
        description="Objects of this class are instances (instance segmentation)",
        default=False,
        update=update_classification_class_is_instances
    )

    # Data passes
    depth_map_generation: bpy.props.BoolProperty(
        name="generate depth map?",
        description="Generate the depth map",
        default=False
    )
    surface_normal_generation: bpy.props.BoolProperty(
        name="generate surface normal?",
        description="Generate the surface normals",
        default=False
    )
    optical_flow_generation: bpy.props.BoolProperty(
        name="generate optical flow?",
        description="Generate the optical flow",
        default=False
    )

    # Camera properties
    camera: bpy.props.PointerProperty(type=BAT_Camera)



# ==============================================================================
# SECTION: Register/Unregister
# ==============================================================================
# Description: Make defined classes available in Blender

classes = [BAT_Camera, BAT_ClassificationClass, BAT_Properties]

def register() -> None:
    '''
    Register properties
    '''
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.bat_properties = bpy.props.PointerProperty(type=BAT_Properties)

def unregister() -> None:
    '''
    Unregister properties
    '''
    del bpy.types.Scene.bat_properties
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
