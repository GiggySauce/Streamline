bl_info = {
    "name": "Streamline",
    "blender": (4, 2, 0),
    "category": "Object",  
    "author": "Giggysauce",
    "description": "Tools to simplify certain tasks.",
    "version": (2, 0),
    "tracker_url": "https://github.com/GiggySauce/Streamline/issues",
    "doc_url": "https://github.com/GiggySauce/Streamline",
    "support": "COMMUNITY",
}

from . import cleanup
from . import rename
from . import camera_tools

def register():
    cleanup.register()
    rename.register()
    camera_tools.register()

def unregister():
    cleanup.unregister()
    rename.unregister()
    camera_tools.unregister()

if __name__ == "__main__":
    register()