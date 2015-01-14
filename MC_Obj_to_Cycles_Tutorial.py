import bpy

# Some useful variables.
images = bpy.data.images
mats = bpy.data.materials
template = mats['Template'] # This is our template material.
objects_mc = bpy.data.groups['Minecraft'].objects # This is the list of all the objects in our 'Minecraft' group.

for ob in objects_mc:
    # The code we add here inside the for loop will be run for each object ("ob") in the list.

    # First we get the required image for the object. We can work this out from it's name.
    image_name = ob.name + ".png"

    # This gives us a string to look for in images (bpy.data.images):
    try:
        block_image = images[image_name]
    except KeyError:
        print("No image found for object: {0}".format(ob.name))
        continue #Skips to the next object if the corresponding image is not found.

    # Next we create a copy of the template material and assign it to the object.
    viewport_colour = ob.material_slots[0].material.diffuse_color # Store the materials original diffuse colour for use in the viewport as it's helpful for navigation.
    ob.material_slots[0].material = template.copy()

    #We now have a copy of the template called "Template.001" or something similar. Lets rename the material helpfully.
    mat = ob.material_slots[0].material
    mat.name = "MC_" + ob.name #The "MC_" at the beginning will group our objects together and distinguish them from non-minecraft materials when looking through them later.
    mat.diffuse_color = viewport_colour

    # Now we modify the image node from the template material to use the correct image.
    nodes = mat.node_tree.nodes #This gives us access to the materials nodes.
    image_node = nodes['MC_Image']
    image_node.image = block_image #Set's the node to use that block's image.

