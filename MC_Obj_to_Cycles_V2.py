import bpy

# Some usful stuff:

mats = bpy.data.materials
template = mats['Template'] # Our template material.

images = bpy.data.images

objects_mc = bpy.data.groups['Minecraft'].objects
print([ob.name for ob in objects_mc])

for ob in objects_mc:
    # Our input has provided us with a bunch of objects
    # All with the same name as the texture they use for their one material.
    # Originally this is just a basic BI material, we need to convert it to cycles and add textures.
    
    # Gather Info For Material Setup
    image_name = ob.name + ".png"

    try:
        image = images[image_name]
    except KeyError:
        print("No image found for object: {0}".format(ob.name))
        continue # Skips to the next object if the corrresponding image is not found.

    # Create a copy of the template material and aassign it to the object.
    viewport_colour = ob.material_slots[0].material.diffuse_color # Store the materials original diffuse colour for use in the viewport as it's helpful for navigation.
    ob.material_slots[0].material = template.copy()
    mat = ob.material_slots[0].material

    # Rename the material helpfully
    mat.name = "MC_" + ob.name # Adding "MC_ at the building will group all of our objects together when viewing them in a list."
    
    # Re-apply the viewport colour.
    mat.diffuse_color = viewport_colour

    # Now modify the image node from the Template material to use the correct image.
    nodes = mat.node_tree.nodes
    image_node = nodes['MC_Image']

    image_node.image = image # Assigns the image based on the objects name to the material.

    

    

    

