import bpy

ob = bpy.context.active_object

mats = bpy.data.materials
images = bpy.data.images

#mat = mats['anvil_side']
copy = mats['Copy']

mats_to_do = [mat for mat in mats if mat.name != copy.name]

for mat in mats_to_do:
    mat.use_nodes = True

    # Create Dict of Nodes to Copy
    nodes_dict = {}
    for node in copy.node_tree.nodes:
       node_name = node.name
       node_label = node.bl_label
       node_type = node.bl_idname
       if node_type == 'ShaderNodeGroup':
           node_group = node.node_tree
           nodes_dict[node_name] = (node_type, node_label, node_group, node.location)
       else:
           nodes_dict[node_name] = (node_type, node_label, None, node.location)
       
          
    #Clear existing Nodes for material:
    mat.node_tree.nodes.clear()

    #Now add new nodes:
    for key in nodes_dict.keys():
        value = nodes_dict[key]
        mat.node_tree.nodes.new(type = value[0])
        mat.node_tree.nodes[value[1]].name = key
        node = mat.node_tree.nodes[key]
        node.location = value[3]   
        if  node.bl_idname == 'ShaderNodeGroup':
            mat.node_tree.nodes[key].node_tree = value[2]
        elif node.bl_idname == 'ShaderNodeTexImage':
            #Get image from shader name:
            try:
                image = bpy.data.images[mat.name + ".png"]
            except KeyError:
                image = None
            mat.node_tree.nodes[key].image = image
        
    #Now do links
    links_list = []
    for link in copy.node_tree.links:
        link_from_node = link.from_node.name
        link_from_socket = link.from_socket.name
        link_to_node = link.to_node.name
        link_to_socket = link.to_socket.name
        links_list.append((link_from_node,link_from_socket,link_to_node,link_to_socket))
        
    #Copy links to material:
    for link in links_list:
        input = mat.node_tree.nodes[link[2]].inputs[link[3]]
        output = mat.node_tree.nodes[link[0]].outputs[link[1]]
        mat.node_tree.links.new(input, output)
        