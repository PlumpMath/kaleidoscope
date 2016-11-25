# Spectrum Palette Node
import bpy
import bpy.utils.previews
import json, os
import urllib.request
from bpy.types import Node
from mathutils import Color
import random

PaletteHistory = []
Palette_idHistory = [0, 0, 0]
palette = {}
palette_export = {}
online_check = True
for i in range(1, 16):
    PaletteHistory.append(Color())

class SpectrumTreeNode:
    @classmethod
    def poll(cls, ntree):
        b = False
        if ntree.bl_idname == 'ShaderNodeTree':
            b = True
        return b

class SpectrumProperties(bpy.types.PropertyGroup):
    def update_color_1(self, context):
        for world in bpy.data.worlds:
            if world.node_tree is not None:
                for node in world.node_tree.nodes:
                    if node.name.startswith("Spectrum Palette"):
                        node.outputs["Color 1"].default_value = bpy.context.scene.prism_spectrum_props.color1
                        update_caller(self, input_name="Color 1")
        for mat in bpy.data.materials:
            if mat.node_tree is not None:
                for node in mat.node_tree.nodes:
                    if node.name.startswith("Spectrum Palette"):
                        node.outputs["Color 1"].default_value = bpy.context.scene.prism_spectrum_props.color1
                        update_caller(self, input_name="Color 1")
        return None

    def update_color_2(self, context):
        for world in bpy.data.worlds:
            if world.node_tree is not None:
                for node in world.node_tree.nodes:
                    if node.name.startswith("Spectrum Palette"):
                        node.outputs["Color 2"].default_value = bpy.context.scene.prism_spectrum_props.color2
                        update_caller(self, input_name="Color 2")
        for mat in bpy.data.materials:
            if mat.node_tree is not None:
                for node in mat.node_tree.nodes:
                    if node.name.startswith("Spectrum Palette"):
                        node.outputs["Color 2"].default_value = bpy.context.scene.prism_spectrum_props.color2
                        update_caller(self, input_name="Color 2")
        return None

    def update_color_3(self, context):
        for world in bpy.data.worlds:
            if world.node_tree is not None:
                for node in world.node_tree.nodes:
                    if node.name.startswith("Spectrum Palette"):
                        node.outputs["Color 3"].default_value = bpy.context.scene.prism_spectrum_props.color3
                        update_caller(self, input_name="Color 3")
        for mat in bpy.data.materials:
            if mat.node_tree is not None:
                for node in mat.node_tree.nodes:
                    if node.name.startswith("Spectrum Palette"):
                        node.outputs["Color 3"].default_value = bpy.context.scene.prism_spectrum_props.color3
                        update_caller(self, input_name="Color 3")
        return None
    def update_color_4(self, context):
        for world in bpy.data.worlds:
            if world.node_tree is not None:
                for node in world.node_tree.nodes:
                    if node.name.startswith("Spectrum Palette"):
                        node.outputs["Color 4"].default_value = bpy.context.scene.prism_spectrum_props.color4
                        update_caller(self, input_name="Color 4")
        for mat in bpy.data.materials:
            if mat.node_tree is not None:
                for node in mat.node_tree.nodes:
                    if node.name.startswith("Spectrum Palette"):
                        node.outputs["Color 4"].default_value = bpy.context.scene.prism_spectrum_props.color4
                        update_caller(self, input_name="Color 4")
        return None

    def update_color_5(self, context):
        for world in bpy.data.worlds:
            if world.node_tree is not None:
                for node in world.node_tree.nodes:
                    if node.name.startswith("Spectrum Palette"):
                        node.outputs["Color 5"].default_value = bpy.context.scene.prism_spectrum_props.color5
                        update_caller(self, input_name="Color 5")
        for mat in bpy.data.materials:
            if mat.node_tree is not None:
                for node in mat.node_tree.nodes:
                    if node.name.startswith("Spectrum Palette"):
                        node.outputs["Color 5"].default_value = bpy.context.scene.prism_spectrum_props.color5
                        update_caller(self, input_name="Color 5")
        return None
    def set_type(self, context):
        prism_spectrum_props = bpy.context.scene.prism_spectrum_props
        prism_spectrum_props.random_int = int(prism_spectrum_props.gen_type)
        prism_spectrum_props.random_custom_int = int(prism_spectrum_props.custom_gen_type)
        return None
    def set_global_settings(self, context):
        prism_spectrum_props = bpy.context.scene.prism_spectrum_props
        c = Color()
        for i in range(0,5):
            if prism_spectrum_props.history_count == 0:
                exec("c.r = PaletteHistory[1"+str(i)+"].r")
                exec("c.g = PaletteHistory[1"+str(i)+"].g")
                exec("c.b = PaletteHistory[1"+str(i)+"].b")
            elif prism_spectrum_props.history_count == 1:
                exec("c.r = PaletteHistory["+str(i+5)+"].r")
                exec("c.g = PaletteHistory["+str(i+5)+"].g")
                exec("c.b = PaletteHistory["+str(i+5)+"].b")
            elif prism_spectrum_props.history_count == 2:
                exec("c.r = PaletteHistory["+str(i)+"].r")
                exec("c.g = PaletteHistory["+str(i)+"].g")
                exec("c.b = PaletteHistory["+str(i)+"].b")
            c.v = c.v+prism_spectrum_props.value_slider
            c.s = c.s+prism_spectrum_props.saturation_slider
            c.h = c.h+prism_spectrum_props.hue_slider
            exec("prism_spectrum_props.color"+str(i+1)+" = c.r, c.g, c.b, 1.0")
            exec("prism_spectrum_props.color"+str(i+1)+" = c.r, c.g, c.b, 1.0")
            exec("prism_spectrum_props.color"+str(i+1)+" = c.r, c.g, c.b, 1.0")
        return None
    def get_saved_palettes(self, context):
        saved_palettes_list = []
        global_palette = []
        local_palette = []
        synced_palette = []

        check = False
        val = None
        try:
            f = open(os.path.join(os.path.dirname(__file__), "sync_directory.txt"), 'r')
            line = f.readlines()
            val = line[0]
            f.close()
            check = True
        except:
            check = False

        #if check == True:
        for sub in os.listdir(val):
            if os.path.isfile(os.path.join(val, str(sub))):
                name = str(sub)
                if name.endswith('.json'):
                    name = name[:-5]
                    name = name.title()
                    name = name.replace('_', ' ')
                    global_palette.append(name)

        i=0
        for sub in os.listdir(os.path.dirname(__file__)):
            if os.path.isfile(os.path.join(os.path.dirname(__file__), str(sub))):
                name = str(sub)
                if name.endswith('.json'):
                    name = name[:-5]
                    name = name.title()
                    name = name.replace('_', ' ')
                    if name in global_palette:
                        saved_palettes_list.append((name, name, "", "URL", i))
                        synced_palette.append(name)
                    else:
                        saved_palettes_list.append((name, name, "", "FILE", i))
                        local_palette.append(name)
            i=i+1

        if check == True:
            i=0
            for sub in os.listdir(val):
                if os.path.isfile(os.path.join(val, str(sub))):
                    name = str(sub)
                    if name.endswith('.json'):
                        name = name[:-5]
                        name = name.title()
                        name = name.replace('_', ' ')
                        if name not in synced_palette and name not in local_palette:
                            saved_palettes_list.append((name, name, "", "WORLD", i))
                i=i+1

        return saved_palettes_list
    def import_saved_palette(self, context):
        prism_spectrum_props=bpy.context.scene.prism_spectrum_props
        name = prism_spectrum_props.saved_palettes
        name = name.lower()
        name = name.replace(' ', '_')
        name = name+".json"
        try:
            path = os.path.join(os.path.dirname(__file__), name)
            palette_file = open(path, 'r')
            self.palette = json.load(palette_file)
        except:
            if prism_spectrum_props.sync_path is not None:
                path = os.path.join(prism_spectrum_props.sync_path, name)
                palette_file = open(path, 'r')
                self.palette = json.load(palette_file)
        for i in range(1, 6):
            exec("prism_spectrum_props.color"+str(i)+" = hex_to_rgb(self.palette[prism_spectrum_props.saved_palettes]['color"+str(i)+"'])")
        palette_file.close()
        set_palettes_list(self, context)
        return None

    def set_ramp(self, context):
        set_color_ramp(self)
        return None

    value_slider = bpy.props.FloatProperty(name="Global Brightness", description="Control the Overall Brightness of the Palette", min=-0.5, max=0.5, default=0.0, update=set_global_settings)
    saturation_slider = bpy.props.FloatProperty(name="Global Saturation", description="Control the Overall Saturation of the Palette", min=-0.5, max=0.5, default=0.0, update=set_global_settings)
    hue_slider = bpy.props.FloatProperty(name="Global Hue", description="Control the Overall Hue of the Palette", min=-0.5, max=0.5, default=0, update=set_global_settings)
    color1 = bpy.props.FloatVectorProperty(name="Color1", description="Set Color 1 for the Palette", subtype="COLOR", size=4, max=1.0, min=0.0, update=update_color_1)
    color2 = bpy.props.FloatVectorProperty(name="Color2", description="Set Color 2 for the Palette", subtype="COLOR", size=4, max=1.0, min=0.0, update=update_color_2)
    color3 = bpy.props.FloatVectorProperty(name="Color3", description="Set Color 3 for the Palette", subtype="COLOR", size=4, max=1.0, min=0.0, update=update_color_3)
    color4 = bpy.props.FloatVectorProperty(name="Color4", description="Set Color 4 for the Palette", subtype="COLOR", size=4, max=1.0, min=0.0, update=update_color_4)
    color5 = bpy.props.FloatVectorProperty(name="Color5", description="Set Color 5 for the Palette", subtype="COLOR", size=4, max=1.0, min=0.0, update=update_color_5)

    hue = bpy.props.FloatVectorProperty(name="Hue", description="Set the Color for the Base Color to be used in Palette Generation", subtype="COLOR", size=4, max=1.0, min=0.0, default=(random.random(), random.random(), random.random(), 1.0))
    gen_type = bpy.props.EnumProperty(name="Type of Palette", description="Select the Rule for the Color Palette Generation", items=(('0','Monochromatic','Use Monochromatic Rule for Palette'),('1','Analogous','Use Analogous Rule for Palette'),('2','Complementary','Use Complementary Rule for Palette'),('3','Triadic','Use Triadic Rule for Palette'),('4','Custom','Use Custom Rule for Palette')), update=set_type, default="0")
    custom_gen_type = bpy.props.EnumProperty(name="Type of Custom Rule", description="Select the Custom rule for Custom Palette Generation", items=(('0', 'Vibrant', 'Uses Two Vibrant Colors, along with shades of black and white'), ('1', 'Gradient', 'Use Color with same hue, but gradual change in Saturation and Value'), ('2', 'Pop out', 'Pop out effect uses one color in combination with shades of black and white'), ('4', 'Online', 'Get Color Palettes from Internet'), ('3', 'Random Rule', 'Use any Rule or color Effect to generate the palette'), ('5', 'Random', 'Randomly Generated Color scheme, not following any rule!')), update=set_type, default="0")
    saved_palettes = bpy.props.EnumProperty(name="Saved Palettes", description="Stores the Saved Palettes", items=get_saved_palettes, update=import_saved_palette)

    use_custom = bpy.props.BoolProperty(name="Use Custom", description="Use Custom Values for Base Color", default=False)
    use_global = bpy.props.BoolProperty(name="Use Global Controls", description="Use Global Settings to control the overall Color of the Palette", default=False)
    use_internet_libs = bpy.props.BoolProperty(name="Internet Library Checker", description="Checks if the palette generated is from Internet library", default=False)
    use_organize = bpy.props.BoolProperty(name="Organize the Color Palette", description="Organize the Color palette generated", default=False)
    view_help = bpy.props.BoolProperty(name="Color Rule Help", description="Get some knowledge about this color rule", default=False)
    assign_colorramp_world = bpy.props.BoolProperty(name="Assign ColorRamp World", description="Assign the Colors from Spectrum to ColorRamp in the World Material", default=False, update=set_ramp)
    sync_help = bpy.props.BoolProperty(name="Syncing Information", description="View/Hide Information on how to setup Syncing of Saved Palettes", default=False)

    random_int = bpy.props.IntProperty(name="Random Integer", description="Used to use Random color rules and effects", default=0)
    random_custom_int = bpy.props.IntProperty(name="Random Custom Integer", description="Used to use Random color rules and effects", default=0)
    new_file = bpy.props.IntProperty(name="File Count",description="", default=1)
    online_palette_index = bpy.props.IntProperty(name="Palette Index", description="Stores the Index of the Online Palette")

    history_count = bpy.props.IntProperty(name="History Counter", description="Value to Count the Current History Value", default=0)

    save_palette_name = bpy.props.StringProperty(name="Save Palette Name", description="Name to be used to save this palette", default="My Palette")
    colorramp_world_name = bpy.props.StringProperty(name="ColorRamp name World", description="Select the ColorRamp in the World Material to assign the Colors", default="", update=set_ramp)

    check = False
    val = None
    try:
        f = open(os.path.join(os.path.dirname(__file__), "sync_directory.txt"), 'r')
        line = f.readlines()
        val = line[0]
        f.close()
        check = True
    except:
        check = False
    if check == True:
        sync_path = bpy.props.StringProperty(name="Sync Path", description="Select the Directory to Sync the Saved Palettes", subtype='DIR_PATH', default=val)
    else:
        sync_path = bpy.props.StringProperty(name="Sync Path", description="Select the Directory to Sync the Saved Palettes", subtype='DIR_PATH', default="")

class SpectrumMaterialProps(bpy.types.PropertyGroup):

    def set_ramp(self, context):
        set_color_ramp(self)
        return None

    colorramp_name = bpy.props.StringProperty(name="ColorRamp name", description="Select the ColorRamp to assign the Colors", default="", update=set_ramp)
    assign_colorramp = bpy.props.BoolProperty(name="Assign ColorRamp", description="Assign the Colors from Spectrum to ColorRamp in the Object Material", default=False, update=set_ramp)

# Derived from the Node base type.

class SavePalette(bpy.types.Operator):
    """Save the current Palette for future use"""
    bl_idname = "spectrum.save_palette"
    bl_label = "Save Spectrum Palette"

    def set_name(self, context):
        prism_spectrum_props=bpy.context.scene.prism_spectrum_props
        prism_spectrum_props.save_palette_name = self.name

        name = self.name
        name = name.lower()
        self.name = name.replace(' ', '_')
        return None

    name = bpy.props.StringProperty(name="Palette Name", description="Enter the Name for the Palette", default="My Palette", update=set_name)

    def execute(self, context):
        prism_spectrum_props=bpy.context.scene.prism_spectrum_props
        prism_spectrum_props.save_palette_name = self.name
        global palette_export
        name = prism_spectrum_props.save_palette_name
        name = name.title()
        name = name.replace('_', ' ')
        prism_spectrum_props.save_palette_name = name
        palette_export[prism_spectrum_props.save_palette_name] = {
            "palette_name": prism_spectrum_props.save_palette_name,
            "color1": rgb_to_hex(prism_spectrum_props.color1),
            "color2": rgb_to_hex(prism_spectrum_props.color2),
            "color3": rgb_to_hex(prism_spectrum_props.color3),
            "color4": rgb_to_hex(prism_spectrum_props.color4),
            "color5": rgb_to_hex(prism_spectrum_props.color5)
        }
        name = prism_spectrum_props.save_palette_name
        name = name.lower()
        prism_spectrum_props.save_palette_name = name.replace(' ', '_')
        path = os.path.join(os.path.dirname(__file__), prism_spectrum_props.save_palette_name+".json")
        s = json.dumps(palette_export)
        with open(path, "w") as f:
            f.write(s)

        if prism_spectrum_props.sync_path is not None:
            path = os.path.join(prism_spectrum_props.sync_path, prism_spectrum_props.save_palette_name+".json")
            s = json.dumps(palette_export)
            with open(path, 'w') as f:
                f.write(s)
        return{'FINISHED'}

    def invoke(self, context, event):
        prism_spectrum_props=bpy.context.scene.prism_spectrum_props
        self.name = prism_spectrum_props.save_palette_name
        return bpy.context.window_manager.invoke_props_dialog(self)

def set_color_ramp(self):
    prism_spectrum_props=bpy.context.scene.prism_spectrum_props
    ramp = None
    ramp_world = None
    spectrum_active = bpy.context.object.active_material.prism_spectrum_props
    if prism_spectrum_props.assign_colorramp_world == True:
        try:
            try:
                ramp_world = bpy.context.scene.world.node_tree.nodes[prism_spectrum_props.colorramp_world_name].color_ramp
            except:
                if prism_spectrum_props.assign_colorramp_world == True:
                    self.report({'WARNING'}, "There is Not a Valid ColorRamp Node in the World Material")
            if prism_spectrum_props.colorramp_world_name != "" and prism_spectrum_props.assign_colorramp_world == True:
                try:
                    for i in range(0, len(ramp_world.elements)):
                            if prism_spectrum_props.assign_colorramp_world == True:
                                exec("ramp_world.elements["+str(i)+"].color[0] = prism_spectrum_props.color"+str(i+1)+"[0]")
                                exec("ramp_world.elements["+str(i)+"].color[1] = prism_spectrum_props.color"+str(i+1)+"[1]")
                                exec("ramp_world.elements["+str(i)+"].color[2] = prism_spectrum_props.color"+str(i+1)+"[2]")
                                ramp_world.elements[0].color[3] = 1.0
                except:
                    pass
        except:
            pass

    for mat in bpy.data.materials:
        spectrum_active = mat.prism_spectrum_props
        if spectrum_active.assign_colorramp == True and spectrum_active.colorramp_name != "":
            try:
                ramp = mat.node_tree.nodes[spectrum_active.colorramp_name].color_ramp
            except:
                if spectrum_active.assign_colorramp == True:
                    self.report({'WARNING'}, "There is Not a Valid ColorRamp Node in '"+mat.name+"'")
            if spectrum_active.colorramp_name != "" and spectrum_active.assign_colorramp == True:
                try:
                    for i in range(0, len(ramp.elements)):
                            if spectrum_active.assign_colorramp == True:
                                exec("ramp.elements["+str(i)+"].color[0] = prism_spectrum_props.color"+str(i+1)+"[0]")
                                exec("ramp.elements["+str(i)+"].color[1] = prism_spectrum_props.color"+str(i+1)+"[1]")
                                exec("ramp.elements["+str(i)+"].color[2] = prism_spectrum_props.color"+str(i+1)+"[2]")
                                ramp.elements[0].color[3] = 1.0
                except:
                    pass

class SpectrumNode(Node, SpectrumTreeNode):
    '''Spectrum node'''
    bl_idname = 'spectrum_palette.node'
    bl_label = 'Spectrum Palette'
    bl_icon = 'INFO'

    def init(self, context):
        self.outputs.new('NodeSocketColor', "Color 1")
        self.outputs.new('NodeSocketColor', "Color 2")
        self.outputs.new('NodeSocketColor', "Color 3")
        self.outputs.new('NodeSocketColor', "Color 4")
        self.outputs.new('NodeSocketColor', "Color 5")
        self.outputs["Color 1"].default_value = bpy.context.scene.prism_spectrum_props.color1
        self.outputs["Color 2"].default_value = bpy.context.scene.prism_spectrum_props.color2
        self.outputs["Color 3"].default_value = bpy.context.scene.prism_spectrum_props.color3
        self.outputs["Color 4"].default_value = bpy.context.scene.prism_spectrum_props.color4
        self.outputs["Color 5"].default_value = bpy.context.scene.prism_spectrum_props.color5
        self.width = 226

    def update(self):
        out = ""
        try:
            for world in bpy.data.worlds:
                for node in world.node_tree.nodes:
                    if node.name.startswith("Spectrum Palette"):
                        for out in node.outputs:
                            if out.is_linked:
                                for o in out.links:
                                    if o.is_valid:
                                        o.to_socket.node.inputs[o.to_socket.name].default_value = out.default_value
        except:
            pass

        try:
            for mat in bpy.data.materials:
                for node in mat.node_tree.nodes:
                    if node.name.startswith("Spectrum Palette"):
                        for out in node.outputs:
                            if out.is_linked:
                                for o in out.links:
                                    if o.is_valid:
                                        o.to_socket.node.inputs[o.to_socket.name].default_value = out.default_value
        except:
            pass

    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        SpectrumPaletteUI(self, context, layout)

    #Node Label
    def draw_label(self):
        return "Spectrum Palette"

def SpectrumPaletteUI(self, context, layout):
    prism_spectrum_props = bpy.context.scene.prism_spectrum_props
    global icons_dict
    col = layout.column(align=True)
    row = col.row(align=True)
    split = row.split(percentage=0.8)
    col1 = split.column(align=True)
    col1.prop(prism_spectrum_props, "gen_type", text="Rule")
    if prism_spectrum_props.gen_type == "4":
        col1.prop(prism_spectrum_props, "custom_gen_type", "Type")
    col2 = split.column()
    row2 = col2.row(align=True)
    if prism_spectrum_props.gen_type != '4' or prism_spectrum_props.custom_gen_type == '3' or prism_spectrum_props.custom_gen_type == '0' or prism_spectrum_props.custom_gen_type == '2':
        if prism_spectrum_props.use_organize == False:
            row2.prop(prism_spectrum_props, "use_organize", toggle=True, text="", icon='SNAP_OFF', emboss=False)
        else:
            row2.prop(prism_spectrum_props, "use_organize", toggle=True, text="", icon='SNAP_ON', emboss=False)
    row2.prop(prism_spectrum_props, "view_help", toggle=True, text="", icon='INFO', emboss=False)
    if prism_spectrum_props.view_help == True:
        box = layout.box()
        col_box = box.column(align=True)
        if prism_spectrum_props.gen_type == "0":
            col_box.label("Monochromatic Scheme is the")
            col_box.label("most basic color rule. It has")
            col_box.label("colors of same hue, but with")
            col_box.label("varying saturation and")
            col_box.label("brightness. It is useful when")
            col_box.label("used in a proper way.")
        elif prism_spectrum_props.gen_type == "1":
            col_box.label("Analogous Scheme uses")
            col_box.label("colors of different hues. It")
            col_box.label("uses one color as base color")
            col_box.label("and uses colors near it in the")
            col_box.label("color wheel, with varying")
            col_box.label("saturation and brightness.")
        elif prism_spectrum_props.gen_type == "2":
            col_box.label("Complementary Scheme is")
            col_box.label("interesting rule where colors")
            col_box.label("opposite to each other in the")
            col_box.label("color wheel are used. This")
            col_box.label("scheme should be used")
            col_box.label("carefully because of contrasting")
            col_box.label("shades.")
        elif prism_spectrum_props.gen_type == "3":
            col_box.label("Triadic Scheme uses")
            col_box.label("one color as base color")
            col_box.label("and other two colors are")
            col_box.label("chosen from the color wheel")
            col_box.label("such that all three form an")
            col_box.label("equilateral triangle.")
        elif prism_spectrum_props.gen_type == "4":
            col_box.label("Custom schemes are some")
            col_box.label("simple rules exclusive to")
            col_box.label("this add-on")
            col_box.label()
            if prism_spectrum_props.custom_gen_type == "0":
                col_box.label("Vibrant scheme uses two")
                col_box.label("visually appealing color shades")
                col_box.label("and others are shades of black")
                col_box.label("and white")
            elif prism_spectrum_props.custom_gen_type == "1":
                col_box.label("Gradient scheme is similar")
                col_box.label("to Monochromatic scheme, and")
                col_box.label("it uses fixed hue with fixed")
                col_box.label("change and goes light to dark")
                col_box.label("from left to form gradient of")
                col_box.label("colors.")
            elif prism_spectrum_props.custom_gen_type == "2":
                col_box.label("Pop Out scheme is similar to")
                col_box.label("Vibrant scheme, but this uses")
                col_box.label("two same colors and other three")
                col_box.label("are shades of black and white.")
                col_box.label("Really Minimal Color Scheme.")
            elif prism_spectrum_props.custom_gen_type == "4":
                col_box.label("Online mode provides you with")
                col_box.label("some amazing color palettes")
                col_box.label("from the Internet.")
                col_box.label()
            elif prism_spectrum_props.custom_gen_type == "3":
                col_box.label("Random option allows you to")
                col_box.label("generate a palette from any rule")
                col_box.label("in a click. It is helpful when")
                col_box.label("you need want to find the best")
                col_box.label("palette of a base color.")
                col_box.label()
            elif prism_spectrum_props.custom_gen_type == "5":
                col_box.label("If you are really angry, and")
                col_box.label("want to try any color for your")
                col_box.label("scene, then use this option.")
                col_box.label("This option 'Randomly' generates")
                col_box.label("the colors for the palette.")
                if prism_spectrum_props.use_internet_libs == True:
                    col_box.label()
        if prism_spectrum_props.use_internet_libs == True:
            col_box.label("Palette ID: "+str(prism_spectrum_props.online_palette_index+1))
            row = col_box.row(align=True)
            row.scale_y = 1.1
            row.operator("wm.url_open", text="Problem?", icon="HELP").url="http://bit.ly/prismbugbs"
        if prism_spectrum_props.gen_type != '4' and prism_spectrum_props.custom_gen_type != '4':
            col_box.label()
        col_box.prop(prism_spectrum_props, "view_help", text="Close Help", icon='INFO')
    col = layout.column(align=True)
    if prism_spectrum_props.use_internet_libs != True:
        if prism_spectrum_props.use_custom == False:
            col.prop(prism_spectrum_props, "use_custom", text="Use Custom Base Color", toggle=True, icon="LAYER_USED")
        if prism_spectrum_props.use_custom == True:
            col.prop(prism_spectrum_props, "use_custom", text="Hide Custom Base Color", toggle=True, icon="LAYER_ACTIVE")
            col1 = layout.column()
            row = col1.row(align=True)
            row.label("Base Color:")
            row.prop(prism_spectrum_props, "hue", text="")

    col2 = layout.column(align=True)
    row = col2.row(align=True)
    row.prop(prism_spectrum_props, "color1", text="")
    row.prop(prism_spectrum_props, "color2", text="")
    row.prop(prism_spectrum_props, "color3", text="")
    row.prop(prism_spectrum_props, "color4", text="")
    row.prop(prism_spectrum_props, "color5", text="")
    row2 = col2.row(align=True)
    row2.scale_y = 1.2
    row2.operator(PaletteGenerate.bl_idname, text="Refresh Palette", icon="COLOR")
    col3 = layout.column(align=True)
    if online_check == False:
        col3.label("There was some problem,", icon='ERROR')
        col3.label("try again")
    if prism_spectrum_props.use_global == False:
        col3.prop(prism_spectrum_props, "use_global", text="View Global Controls", icon='LAYER_USED', toggle=True)
    else:
        col3.prop(prism_spectrum_props, "use_global", text="Hide Global Controls", icon='LAYER_ACTIVE', toggle=True)
        col4 = layout.column(align=True)
        row4 = col4.row(align=True)
        col4.prop(prism_spectrum_props, "hue_slider", text="Hue", slider=True)
        col4.prop(prism_spectrum_props, "saturation_slider", text="Saturation", slider=True)
        col4.prop(prism_spectrum_props, "value_slider", text="Value", slider=True)

    col4 = layout.column(align=True)
    col4.label()
    row4 = col4.row(align=True)
    if prism_spectrum_props.history_count != 2:
        row4.operator(PreviousPalette.bl_idname, text="", icon="TRIA_LEFT")
    row4.operator(PaletteShuffle.bl_idname, text="Shuffle", icon="ARROW_LEFTRIGHT")
    if prism_spectrum_props.history_count != 0:
        row4.operator(NextPalette.bl_idname, text="", icon="TRIA_RIGHT")
    col4.label()
    row5 = col4.row(align=True)
    if len(prism_spectrum_props.saved_palettes) !=0:
        row5.prop(prism_spectrum_props, "saved_palettes", text="")
    else:
        row5.label("No Saved Presets")
    row5.operator(SavePalette.bl_idname, text="", icon='ZOOMIN')
    row5.operator(DeletePalette.bl_idname, text="", icon='ZOOMOUT')
    col4.label()
    row6 = col4.row(align=True)
    if bpy.context.space_data.shader_type == 'WORLD':
        row6.prop_search(prism_spectrum_props,"colorramp_world_name", bpy.context.scene.world.node_tree, "nodes",text="Ramp", icon='NODETREE')
        row6.prop(prism_spectrum_props, "assign_colorramp_world", text="", icon='RESTRICT_COLOR_ON', toggle=True)
    elif bpy.context.space_data.shader_type == 'OBJECT':
        row6.prop_search(bpy.context.object.active_material.prism_spectrum_props,"colorramp_name", bpy.context.object.active_material.node_tree, "nodes",text="Ramp", icon='NODETREE')
        row6.prop(bpy.context.object.active_material.prism_spectrum_props, "assign_colorramp", text="", icon='RESTRICT_COLOR_ON', toggle=True)
    col4.label()
    row7 = col4.row(align=True)
    row7.operator('wm.url_open', text="", icon_value=icons_dict["blenderskool"].icon_id, emboss=False).url="http://www.blenderskool.cf"
    row7_1 = row7.row(align=True)
    row7_1.alignment = 'CENTER'
    row7_1.label("Akash Hamirwasia")
    row7.operator('wm.url_open', text="", icon_value=icons_dict["youtube"].icon_id, emboss=False).url="http://www.youtube.com/AkashHamirwasia1"

def update_caller(caller, input_name):
    prism_spectrum_props=bpy.context.scene.prism_spectrum_props
    for world in bpy.data.worlds:
        if world.node_tree is not None:
            for node in world.node_tree.nodes:
                if node.name.startswith("Spectrum Palette"):
                    if node.outputs[input_name].is_linked:
                        for o in node.outputs[input_name].links:
                            if o.is_valid:
                                o.to_socket.node.inputs[o.to_socket.name].default_value = node.outputs[input_name].default_value

    for mat in bpy.data.materials:
        if mat.node_tree is not None:
            for node in mat.node_tree.nodes:
                if node.name.startswith("Spectrum Palette"):
                    if node.outputs[input_name].is_linked:
                        for o in node.outputs[input_name].links:
                            if o.is_valid:
                                o.to_socket.node.inputs[o.to_socket.name].default_value = node.outputs[input_name].default_value

    for mat in bpy.data.materials:
        if mat.prism_spectrum_props.assign_colorramp == True or prism_spectrum_props.assign_colorramp_world == True:
            set_color_ramp(caller)
            break

def hex_to_rgb(value):
    gamma = 2.2
    value = value.lstrip('#')
    lv = len(value)
    fin = list(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    r = pow(fin[0] / 255, gamma)
    g = pow(fin[1] / 255, gamma)
    b = pow(fin[2] / 255, gamma)
    fin.clear()
    fin.append(r)
    fin.append(g)
    fin.append(b)
    fin.append(1.0)
    return tuple(fin)

def rgb_to_hex(rgb):
    gamma = 1/2.2
    fin = list(rgb)
    r = fin[0]*255
    g = fin[1]*255
    b = fin[2]*255
    r = int(255*pow(r / 255, gamma))
    g = int(255*pow(g / 255, gamma))
    b = int(255*pow(b / 255, gamma))
    fin.clear()
    fin.append(r)
    fin.append(g)
    fin.append(b)
    fin = tuple(fin)
    return '#%02x%02x%02x' % fin

def Spectrum_Engine(caller, context):
    prism_spectrum_props = bpy.context.scene.prism_spectrum_props
    prism_spectrum_props.hue_slider = 0.0
    prism_spectrum_props.saturation_slider = 0.0
    prism_spectrum_props.value_slider = 0.0

    c = Color()
    c.hsv = 1.0, 0.0, 1.0
    index = [1, 2, 3, 4, 5]
    random.shuffle(index)
    c.hsv = random.random(), random.random(), random.random()
    if random.randint(0, 3) /2 == 0:
        c.h = 0.0
    if c.v >= 0.95:
        c.v = c.v-0.1
    elif c.v <= 0.4:
        c.v = c.v+0.2

    if prism_spectrum_props.use_custom == True:
        if prism_spectrum_props.hue != (0.0, 0.0, 0.0, 1.0):
            c.r = random.uniform(prism_spectrum_props.hue[0]-0.1, prism_spectrum_props.hue[0]+0.05)
            c.g = random.uniform(prism_spectrum_props.hue[1]-0.1, prism_spectrum_props.hue[1]+0.05)
            c.b = random.uniform(prism_spectrum_props.hue[2]-0.1, prism_spectrum_props.hue[2]+0.05)

    #Monochromatic
    if prism_spectrum_props.gen_type == "0" or prism_spectrum_props.random_int == 0:
        Hue = c.h
        Saturation_less= 0.0
        if c.s <=0.1:
            Saturation_less = 0.0
        else:
            Saturation_less = random.uniform(0.1, c.s)

        if Saturation_less == c.s:
            Saturation_less = random.uniform(0.1, c.s)

        if Saturation_less < 0.25:
            Saturation_less = 0.4

        Saturation_more = random.uniform(c.s+0.1, c.s+0.2)

        Value_less = random.uniform(0.2, c.v)
        Value_more = random.uniform(c.v+0.1, c.v+0.3)

        if Value_less == 0.0:
            Value_less = 0.3
        elif Value_more == 0.0:
            Value_more = 0.7

        c1 = Color()
        c1.hsv = Hue, Saturation_more, Value_more

        if prism_spectrum_props.use_organize == False:
            exec("prism_spectrum_props.color"+str(index[0])+" = c1.r, c1.g, c1.b, 1.0")
        else:
            prism_spectrum_props.color1 = c1.r, c1.g, c1.b, 1.0

        c1.hsv = Hue, Saturation_more+0.1, Value_more
        if prism_spectrum_props.use_organize == False:
            exec("prism_spectrum_props.color"+str(index[1])+" = c1.r, c1.g, c1.b, 1.0")
        else:
            prism_spectrum_props.color2 = c1.r, c1.g, c1.b, 1.0

        c1.hsv = Hue, c.s, c.v
        if prism_spectrum_props.use_organize == False:
            exec("prism_spectrum_props.color"+str(index[2])+" = c1.r, c1.g, c1.b, 1.0")
        else:
            prism_spectrum_props.color3 = c1.r, c1.g, c1.b, 1.0

        c1.hsv = Hue, Saturation_more+0.1, Value_less-0.1
        if prism_spectrum_props.use_organize == False:
            exec("prism_spectrum_props.color"+str(index[3])+" = c1.r, c1.g, c1.b, 1.0")
        else:
            prism_spectrum_props.color4 = c1.r, c1.g, c1.b, 1.0

        c1.hsv = Hue, Saturation_less, Value_less-0.1
        if prism_spectrum_props.use_organize == False:
            exec("prism_spectrum_props.color"+str(index[4])+" = c1.r, c1.g, c1.b, 1.0")
        else:
            prism_spectrum_props.color5 = c1.r, c1.g, c1.b, 1.0
        prism_spectrum_props.use_internet_libs == False

    elif prism_spectrum_props.gen_type == "1" or prism_spectrum_props.random_int == 1:
        #Analogous
        Saturation = random.uniform(c.s, 1)
        if Saturation <= 0.4:
            Saturation = Saturation+0.35
        Value = c.v
        if (Value <= 1.0 or Value>1.0) and Value >= 0.8:
            Value = Value-0.1
        if Value <=0.3:
            Value = 0.7
        Value1 = random.uniform(Value+0.1, Value+0.25)
        if (Value1 <= 1.0 or Value1>1.0) and Value1 >= 0.8:
            Value1 = Value1-0.3
        if Value1 <=0.3:
            Value1 = 0.7
        Hue1 = random.uniform(c.h+0.2, c.h+0.3)
        Hue = random.uniform(c.h, c.h+0.2)
        if Hue1 == Hue:
            Hue1 = Hue1-0.1
        if Hue == 0:
            Hue1 = 0.1
        c2 = Color()
        c2.hsv = Hue1, Saturation-0.2, Value
        if prism_spectrum_props.use_organize == False:
            exec("prism_spectrum_props.color"+str(index[0])+" = c2.r, c2.g, c2.b, 1.0")
        else:
            prism_spectrum_props.color3 = c2.r, c2.g, c2.b, 1.0

        Hue1_2 = random.uniform(c.h-0.07, c.h-0.2)
        if Hue1_2 == Hue1:
            Hue1_2 = Hue1_2-0.1
        c2.hsv = Hue, Saturation+0.2, Value1
        if prism_spectrum_props.use_organize == False:
            exec("prism_spectrum_props.color"+str(index[1])+" = c2.r, c2.g, c2.b, 1.0")
            exec("prism_spectrum_props.color"+str(index[2])+" = c2.r, c2.g, c2.b, 1.0")
        else:
            prism_spectrum_props.color2 = c2.r, c2.g, c2.b, 1.0
            prism_spectrum_props.color1 = c2.r, c2.g, c2.b, 1.0

        Hue_1 = random.uniform(c.h, c.h-0.3)
        if Hue_1==0:
            Hue_1 = 0.9
        if Hue_1 == Hue:
            Hue_1 = Hue_1-0.08
        if c.h == 0.0:
            Hue_1 = 1-abs(Hue_1)
            Hue1_2 = 1-abs(Hue1_2)
        c2.hsv = Hue1_2, Saturation, Value1
        if prism_spectrum_props.use_organize == False:
            exec("prism_spectrum_props.color"+str(index[3])+" = c2.r, c2.g, c2.b, 1.0")
        else:
            prism_spectrum_props.color4 = c2.r, c2.g, c2.b, 1.0

        c2.hsv = Hue_1, Saturation, Value
        if prism_spectrum_props.use_organize == False:
            exec("prism_spectrum_props.color"+str(index[4])+" = c2.r, c2.g, c2.b, 1.0")
        else:
            prism_spectrum_props.color5 = c2.r, c2.g, c2.b, 1.0
        prism_spectrum_props.use_internet_libs = False

    elif prism_spectrum_props.gen_type == "2" or prism_spectrum_props.random_int == 2:
        #Complementary
        Hue = c.h
        Hue1 = 0.0
        if Hue>=0.5:
            Hue1=Hue-0.5
        else:
            Hue1=Hue+0.5
        Saturation = c.s
        if Saturation <=1.0 and Saturation >=0.95:
            Saturation = Saturation-0.1
        if Saturation <=0.3:
            Saturation = Saturation+0.25
        Saturation_more = random.uniform(Saturation+0.05, Saturation+0.2)
        Saturation_less = random.uniform(Saturation-0.2, Saturation-0.05)
        if Saturation_more <=1.0 and Saturation_more >=0.95:
            Saturation_more = Saturation_more-0.1
        if Saturation_more <=0.6:
            Saturation_more = Saturation_more+0.45

        if Saturation_less <=1.0 and Saturation_less >=0.95:
            Saturation_less = Saturation_less-0.15

        Value = c.v
        Value_more = random.uniform(Value+0.05, Value+0.2)
        Value_less = random.uniform(Value-0.2, Value-0.05)
        if Value_more >=0.0 and Value_more <0.1:
            Value_more = Value_more+0.35
        if Value_less >=0.0 and Value_less <0.1:
            Value_less = Value_less+0.3

        c2 = Color()
        c2.hsv = Hue, Saturation_more, Value_less
        if prism_spectrum_props.use_organize == False:
            exec("prism_spectrum_props.color"+str(index[0])+" = c2.r, c2.g, c2.b, 1.0")
        else:
            prism_spectrum_props.color1 = c2.r, c2.g, c2.b, 1.0

        c2.hsv = Hue, Saturation_less, Value_more
        if prism_spectrum_props.use_organize == False:
            exec("prism_spectrum_props.color"+str(index[1])+" = c2.r, c2.g, c2.b, 1.0")
        else:
            prism_spectrum_props.color2 = c2.r, c2.g, c2.b, 1.0

        c2.hsv = Hue, Saturation, Value
        if prism_spectrum_props.use_organize == False:
            exec("prism_spectrum_props.color"+str(index[2])+" = c2.r, c2.g, c2.b, 1.0")
        else:
            prism_spectrum_props.color3 = c2.r, c2.g, c2.b, 1.0

        c2.hsv = Hue1, Saturation_more, Value_less
        if prism_spectrum_props.use_organize == False:
            exec("prism_spectrum_props.color"+str(index[3])+" = c2.r, c2.g, c2.b, 1.0")
        else:
            prism_spectrum_props.color4 = c2.r, c2.g, c2.b, 1.0

        c2.hsv = Hue1, Saturation, Value
        if prism_spectrum_props.use_organize == False:
            exec("prism_spectrum_props.color"+str(index[4])+" = c2.r, c2.g, c2.b, 1.0")
        else:
            prism_spectrum_props.color5= c2.r, c2.g, c2.b, 1.0
        prism_spectrum_props.use_internet_libs = False

    elif prism_spectrum_props.gen_type == "3" or prism_spectrum_props.random_int == 3:
        #Triad
        Hue = c.h
        Hue2 = Hue+0.34
        Hue3 = Hue+0.34+0.34
        if Hue >0.34:
            if Hue > 0.66:
                Hue2 = Hue-0.34
                Hue3 = Hue-0.34-0.34
            Hue2 = Hue+0.34
            Hue3 = Hue-0.34

        Saturation = c.s
        if Saturation <=0.1:
            Saturation = 0.6
        elif Saturation <=0.6:
            Saturation = Saturation+0.45
        if Saturation >= 0.95:
            Saturation = Saturation-0.2
        Saturation_more = random.uniform(Saturation+0.07, Saturation+0.2)
        Saturation_less = random.uniform(Saturation-0.2, Saturation-0.07)
        Saturation_lesser = random.uniform(Saturation-0.1, Saturation-0.08)

        if Saturation_more <=1.0 and Saturation_more >=0.95:
            Saturation_more = Saturation_more-0.1
        if Saturation_more <=0.6:
            Saturation_more = Saturation_more+0.45

        if Saturation_lesser>=1.0 and Saturation_lesser >=0.85:
            Saturation_lesser = 0.7
        if Saturation_lesser <=0.6:
            Saturation_lesser = Saturation_lesser+0.35

        Value = c.v
        Value_less = 0
        if Value<=0.4:
            Value = 0.6
        Value_less = random.uniform(Value-0.2, Value-0.07)

        c2 = Color()
        c2.hsv = Hue, Saturation_more, Value_less
        if prism_spectrum_props.use_organize == False:
            exec("prism_spectrum_props.color"+str(index[0])+" = c2.r, c2.g, c2.b, 1.0")
        else:
            prism_spectrum_props.color1= c2.r, c2.g, c2.b, 1.0

        c2.hsv = Hue, Saturation, Value
        if prism_spectrum_props.use_organize == False:
            exec("prism_spectrum_props.color"+str(index[2])+" = c2.r, c2.g, c2.b, 1.0")
        else:
            prism_spectrum_props.color2= c2.r, c2.g, c2.b, 1.0

        c2.hsv = Hue3, Saturation_lesser, Value
        if prism_spectrum_props.use_organize == False:
            exec("prism_spectrum_props.color"+str(index[1])+" = c2.r, c2.g, c2.b, 1.0")
        else:
            prism_spectrum_props.color3= c2.r, c2.g, c2.b, 1.0

        c2.hsv = Hue2, Saturation_less-0.07, Value_less+0.1
        if prism_spectrum_props.use_organize == False:
            exec("prism_spectrum_props.color"+str(index[3])+" = c2.r, c2.g, c2.b, 1.0")
        else:
            prism_spectrum_props.color4= c2.r, c2.g, c2.b, 1.0

        c2.hsv = Hue2, Saturation_less+0.07, Value_less-0.2
        if prism_spectrum_props.use_organize == False:
            exec("prism_spectrum_props.color"+str(index[4])+" = c2.r, c2.g, c2.b, 1.0")
        else:
            prism_spectrum_props.color5= c2.r, c2.g, c2.b, 1.0
        prism_spectrum_props.use_internet_libs = False

    elif prism_spectrum_props.gen_type == "4" or prism_spectrum_props.random_int == 4:
        if prism_spectrum_props.custom_gen_type == "0" or prism_spectrum_props.random_custom_int == 0:
            #Vibrant
            Hue = c.h
            while True:
                if Hue <=0.1 and Hue>=0.0:
                    Hue = random.random()
                    if prism_spectrum_props.use_custom == True:
                        if prism_spectrum_props.hue != (0.0, 0.0, 0.0, 1.0):
                            c_rgb = Color()
                            c_rgb.r = prism_spectrum_props.hue[0]
                            c_rgb.g = prism_spectrum_props.hue[1]
                            c_rgb.b = prism_spectrum_props.hue[2]
                            Hue = random.uniform(c_rgb.h-0.1, c_rgb.h+0.1)
                else:
                    break
            Hue1 = 0.0
            if Hue > 0.7:
                Hue1 = Hue-random.random()
            else:
                Hue1 = Hue+random.random()

            Saturation = c.s
            if Saturation <= 0.7:
                Saturation = 0.8
            Value1 = c.v
            if Value1<0.5:
                Value1 = Value1+0.3
            Value = random.uniform(Value1-0.3, Value1-0.23)

            c2 = Color()
            c2.hsv = 0.0, 0.0, random.uniform(0.3, 0.7)
            if prism_spectrum_props.use_organize == False:
                exec("prism_spectrum_props.color"+str(index[0])+" = c2.r, c2.g, c2.b, 1.0")
            else:
                prism_spectrum_props.color4= c2.r, c2.g, c2.b, 1.0

            c2.hsv = 0.0, 0.0, random.uniform(0, 0.5)
            if prism_spectrum_props.use_organize == False:
                exec("prism_spectrum_props.color"+str(index[1])+" = c2.r, c2.g, c2.b, 1.0")
            else:
                prism_spectrum_props.color5= c2.r, c2.g, c2.b, 1.0

            c2.hsv = 0.0, 0.0, random.uniform(0.7, 1)
            if prism_spectrum_props.use_organize == False:
                exec("prism_spectrum_props.color"+str(index[2])+" = c2.r, c2.g, c2.b, 1.0")
            else:
                prism_spectrum_props.color3= c2.r, c2.g, c2.b, 1.0

            c2.hsv = Hue, Saturation, Value1
            if prism_spectrum_props.use_organize == False:
                exec("prism_spectrum_props.color"+str(index[3])+" = c2.r, c2.g, c2.b, 1.0")
            else:
                prism_spectrum_props.color2= c2.r, c2.g, c2.b, 1.0

            c2.hsv = Hue1, Saturation, Value
            if prism_spectrum_props.use_organize == False:
                exec("prism_spectrum_props.color"+str(index[4])+" = c2.r, c2.g, c2.b, 1.0")
            else:
                prism_spectrum_props.color1= c2.r, c2.g, c2.b, 1.0
            prism_spectrum_props.use_internet_libs = False
        elif prism_spectrum_props.custom_gen_type=="1" or prism_spectrum_props.random_custom_int == 1:
            #Gradient
            Hue = c.h
            Value = c.v
            Saturation = c.s+0.1

            c1 = Color()
            c1.hsv = Hue, 0.2, 0.9
            prism_spectrum_props.color1 = c1.r, c1.g, c1.b, 1.0

            c1.hsv = Hue, 0.3, 0.9-0.1
            prism_spectrum_props.color2 = c1.r, c1.g, c1.b, 1.0

            c1.hsv = Hue, Saturation, Value
            prism_spectrum_props.color3 = c1.r, c1.g, c1.b, 1.0

            c1.hsv = Hue, 0.9-0.1, 0.1+0.1
            prism_spectrum_props.color4 = c1.r, c1.g, c1.b, 1.0

            c1.hsv = Hue, 0.9, 0.1
            prism_spectrum_props.color5 = c1.r, c1.g, c1.b, 1.0
            prism_spectrum_props.use_internet_libs = False
        elif prism_spectrum_props.custom_gen_type == "2" or prism_spectrum_props.random_custom_int == 2:
            #Popout
            Hue = c.h
            Saturation = c.s
            if Saturation<0.9:
                Saturation = 0.95
            Value = c.v
            c2 = Color()
            c2.hsv = 0.0, 0.0, random.uniform(0.3, 0.7)
            if prism_spectrum_props.use_organize == False:
                exec("prism_spectrum_props.color"+str(index[0])+" = c2.r, c2.g, c2.b, 1.0")
            else:
                prism_spectrum_props.color4= c2.r, c2.g, c2.b, 1.0

            c2.hsv = Hue, Saturation, Value
            if prism_spectrum_props.use_organize == False:
                exec("prism_spectrum_props.color"+str(index[1])+" = c2.r, c2.g, c2.b, 1.0")
            else:
                prism_spectrum_props.color1= c2.r, c2.g, c2.b, 1.0

            c2.hsv = 0.0, 0.0, random.uniform(0, 0.2)
            if prism_spectrum_props.use_organize == False:
                exec("prism_spectrum_props.color"+str(index[2])+" = c2.r, c2.g, c2.b, 1.0")
            else:
                prism_spectrum_props.color5= c2.r, c2.g, c2.b, 1.0

            c2.hsv = Hue, Saturation-0.1, Value
            if prism_spectrum_props.use_organize == False:
                exec("prism_spectrum_props.color"+str(index[3])+" = c2.r, c2.g, c2.b, 1.0")
            else:
                prism_spectrum_props.color2= c2.r, c2.g, c2.b, 1.0

            c2.hsv = 0.0, 0.0, random.uniform(0.7, 1)
            if prism_spectrum_props.use_organize == False:
                exec("prism_spectrum_props.color"+str(index[4])+" = c2.r, c2.g, c2.b, 1.0")
            else:
                prism_spectrum_props.color3= c2.r, c2.g, c2.b, 1.0

            prism_spectrum_props.use_internet_libs = False
        elif prism_spectrum_props.custom_gen_type == "4" or prism_spectrum_props.random_custom_int == 3:
            global palette
            global online_check
            #Online
            try:
                if prism_spectrum_props.new_file != 0:
                    palette_file = str(urllib.request.urlopen("https://raw.githubusercontent.com/blenderskool/prism/master/palette.json").read(), 'UTF-8')
                    prism_spectrum_props.new_file = 0
                    palette = json.loads(palette_file)
                index = random.randint(0, len(palette)-1)
                for i in range(0, 20):
                    if prism_spectrum_props.online_palette_index == index or Palette_idHistory[1] == index or Palette_idHistory[0] == index:
                        index = random.randint(0, len(palette)-1)
                    else:
                        break
                prism_spectrum_props.online_palette_index = index
                online_check = True

                for i in range(1, 6):
                    exec("prism_spectrum_props.color"+str(i)+" = hex_to_rgb(palette[index]['color"+str(i)+"']['hex'])")
                prism_spectrum_props.use_internet_libs = True
            except:
                online_check = False
        elif prism_spectrum_props.custom_gen_type == "5" or prism_spectrum_props.random_custom_int == 4:
            #Random
            if prism_spectrum_props.use_custom == True:
                exec("prism_spectrum_props.color"+str(index[0])+" = prism_spectrum_props.hue[0], prism_spectrum_props.hue[1], prism_spectrum_props.hue[2], 1.0")
            else:
                exec("prism_spectrum_props.color"+str(index[0])+" = hex_to_rgb(''.join([random.choice('0123456789ABCDEF') for x in range(6)]))")
            exec("prism_spectrum_props.color"+str(index[1])+" = hex_to_rgb(''.join([random.choice('0123456789ABCDEF') for x in range(6)]))")
            exec("prism_spectrum_props.color"+str(index[2])+" = hex_to_rgb(''.join([random.choice('0123456789ABCDEF') for x in range(6)]))")
            exec("prism_spectrum_props.color"+str(index[3])+" = hex_to_rgb(''.join([random.choice('0123456789ABCDEF') for x in range(6)]))")
            exec("prism_spectrum_props.color"+str(index[4])+" = hex_to_rgb(''.join([random.choice('0123456789ABCDEF') for x in range(6)]))")
            prism_spectrum_props.use_internet_libs = False

def set_palettes_list(caller, context):
    prism_spectrum_props=bpy.context.scene.prism_spectrum_props
    #Palette History 1
    PaletteHistory[4].r = PaletteHistory[9].r
    PaletteHistory[4].g = PaletteHistory[9].g
    PaletteHistory[4].b = PaletteHistory[9].b

    PaletteHistory[3].r = PaletteHistory[8].r
    PaletteHistory[3].g = PaletteHistory[8].g
    PaletteHistory[3].b = PaletteHistory[8].b

    PaletteHistory[2].r = PaletteHistory[7].r
    PaletteHistory[2].g = PaletteHistory[7].g
    PaletteHistory[2].b = PaletteHistory[7].b

    PaletteHistory[1].r = PaletteHistory[6].r
    PaletteHistory[1].g = PaletteHistory[6].g
    PaletteHistory[1].b = PaletteHistory[6].b

    PaletteHistory[0].r = PaletteHistory[5].r
    PaletteHistory[0].g = PaletteHistory[5].g
    PaletteHistory[0].b = PaletteHistory[5].b
    Palette_idHistory[0] = Palette_idHistory[1]

    #Palette History 2
    PaletteHistory[9].r = PaletteHistory[14].r
    PaletteHistory[9].g = PaletteHistory[14].g
    PaletteHistory[9].b = PaletteHistory[14].b

    PaletteHistory[8].r = PaletteHistory[13].r
    PaletteHistory[8].g = PaletteHistory[13].g
    PaletteHistory[8].b = PaletteHistory[13].b

    PaletteHistory[7].r = PaletteHistory[12].r
    PaletteHistory[7].g = PaletteHistory[12].g
    PaletteHistory[7].b = PaletteHistory[12].b

    PaletteHistory[6].r = PaletteHistory[11].r
    PaletteHistory[6].g = PaletteHistory[11].g
    PaletteHistory[6].b = PaletteHistory[11].b

    PaletteHistory[5].r = PaletteHistory[10].r
    PaletteHistory[5].g = PaletteHistory[10].g
    PaletteHistory[5].b = PaletteHistory[10].b
    Palette_idHistory[1] = Palette_idHistory[2]

    #Palette History 3
    PaletteHistory[14].r = prism_spectrum_props.color5[0]
    PaletteHistory[14].g = prism_spectrum_props.color5[1]
    PaletteHistory[14].b = prism_spectrum_props.color5[2]

    PaletteHistory[13].r = prism_spectrum_props.color4[0]
    PaletteHistory[13].g = prism_spectrum_props.color4[1]
    PaletteHistory[13].b = prism_spectrum_props.color4[2]

    PaletteHistory[12].r = prism_spectrum_props.color3[0]
    PaletteHistory[12].g = prism_spectrum_props.color3[1]
    PaletteHistory[12].b = prism_spectrum_props.color3[2]

    PaletteHistory[11].r = prism_spectrum_props.color2[0]
    PaletteHistory[11].g = prism_spectrum_props.color2[1]
    PaletteHistory[11].b = prism_spectrum_props.color2[2]

    PaletteHistory[10].r = prism_spectrum_props.color1[0]
    PaletteHistory[10].g = prism_spectrum_props.color1[1]
    PaletteHistory[10].b = prism_spectrum_props.color1[2]
    Palette_idHistory[2] = prism_spectrum_props.online_palette_index

    prism_spectrum_props.history_count = 0

class PaletteGenerate(bpy.types.Operator):
    """Generate a new Color Palette"""
    bl_idname="spectrum_palette.palette_gen"
    bl_label="Refresh Palette"

    def execute(self, context):
        prism_spectrum_props = bpy.context.scene.prism_spectrum_props
        if prism_spectrum_props.custom_gen_type != "3":
            Spectrum_Engine(self, context)
        else:
            num = random.randint(0, 2)
            if num % 2 == 0:
                prism_spectrum_props.random_int = 4
            else:
                prism_spectrum_props.random_int = random.randint(0, 4)
            prism_spectrum_props.random_custom_int = random.randint(0, 4)
            Spectrum_Engine(self, context)
        set_palettes_list(self, context)
        for mat in bpy.data.materials:
            if mat.prism_spectrum_props.assign_colorramp == True or prism_spectrum_props.assign_colorramp_world == True:
                set_color_ramp(self)
                break
        return{'FINISHED'}

class PreviousPalette(bpy.types.Operator):
    """View the Previous Palette"""
    bl_idname="spectrum_palette.palette_previous"
    bl_label="Previous Palette"

    def execute(self, context):
        prism_spectrum_props = bpy.context.scene.prism_spectrum_props
        prism_spectrum_props.history_count = prism_spectrum_props.history_count+1
        if prism_spectrum_props.history_count == 2:
            for i in range(0, 5):
                exec("prism_spectrum_props.color"+str(i+1)+"[0] = PaletteHistory["+str(i)+"].r")
                exec("prism_spectrum_props.color"+str(i+1)+"[1] = PaletteHistory["+str(i)+"].g")
                exec("prism_spectrum_props.color"+str(i+1)+"[2] = PaletteHistory["+str(i)+"].b")

            prism_spectrum_props.online_palette_index = Palette_idHistory[0]

        elif prism_spectrum_props.history_count == 1:
            prism_spectrum_props.color1[0] = PaletteHistory[5].r
            prism_spectrum_props.color1[1] = PaletteHistory[5].g
            prism_spectrum_props.color1[2] = PaletteHistory[5].b

            prism_spectrum_props.color2[0] = PaletteHistory[6].r
            prism_spectrum_props.color2[1] = PaletteHistory[6].g
            prism_spectrum_props.color2[2] = PaletteHistory[6].b

            prism_spectrum_props.color3[0] = PaletteHistory[7].r
            prism_spectrum_props.color3[1] = PaletteHistory[7].g
            prism_spectrum_props.color3[2] = PaletteHistory[7].b

            prism_spectrum_props.color4[0] = PaletteHistory[8].r
            prism_spectrum_props.color4[1] = PaletteHistory[8].g
            prism_spectrum_props.color4[2] = PaletteHistory[8].b

            prism_spectrum_props.color5[0] = PaletteHistory[9].r
            prism_spectrum_props.color5[1] = PaletteHistory[9].g
            prism_spectrum_props.color5[2] = PaletteHistory[9].b

            prism_spectrum_props.online_palette_index = Palette_idHistory[1]

        elif prism_spectrum_props.history_count == 0:
            prism_spectrum_props.color1[0] = PaletteHistory[10].r
            prism_spectrum_props.color1[1] = PaletteHistory[10].g
            prism_spectrum_props.color1[2] = PaletteHistory[10].b

            prism_spectrum_props.color2[0] = PaletteHistory[11].r
            prism_spectrum_props.color2[1] = PaletteHistory[11].g
            prism_spectrum_props.color2[2] = PaletteHistory[11].b

            prism_spectrum_props.color3[0] = PaletteHistory[12].r
            prism_spectrum_props.color3[1] = PaletteHistory[12].g
            prism_spectrum_props.color3[2] = PaletteHistory[12].b

            prism_spectrum_props.color4[0] = PaletteHistory[13].r
            prism_spectrum_props.color4[1] = PaletteHistory[13].g
            prism_spectrum_props.color4[2] = PaletteHistory[13].b

            prism_spectrum_props.color5[0] = PaletteHistory[14].r
            prism_spectrum_props.color5[1] = PaletteHistory[14].g
            prism_spectrum_props.color5[2] = PaletteHistory[14].b

            prism_spectrum_props.online_palette_index[2] = Palette_idHistory[2]

        prism_spectrum_props.hue_slider = 0.0
        prism_spectrum_props.saturation_slider = 0.0
        prism_spectrum_props.value_slider = 0.0
        return{'FINISHED'}

class NextPalette(bpy.types.Operator):
    """View the Next Palette"""
    bl_idname="spectrum_palette.palette_next"
    bl_label="Next Palette"

    def execute(self, context):
        prism_spectrum_props = bpy.context.scene.prism_spectrum_props
        prism_spectrum_props.history_count = prism_spectrum_props.history_count-1
        if prism_spectrum_props.history_count == 1:
            prism_spectrum_props.color1[0] = PaletteHistory[5].r
            prism_spectrum_props.color1[1] = PaletteHistory[5].g
            prism_spectrum_props.color1[2] = PaletteHistory[5].b

            prism_spectrum_props.color2[0] = PaletteHistory[6].r
            prism_spectrum_props.color2[1] = PaletteHistory[6].g
            prism_spectrum_props.color2[2] = PaletteHistory[6].b

            prism_spectrum_props.color3[0] = PaletteHistory[7].r
            prism_spectrum_props.color3[1] = PaletteHistory[7].g
            prism_spectrum_props.color3[2] = PaletteHistory[7].b

            prism_spectrum_props.color4[0] = PaletteHistory[8].r
            prism_spectrum_props.color4[1] = PaletteHistory[8].g
            prism_spectrum_props.color4[2] = PaletteHistory[8].b

            prism_spectrum_props.color5[0] = PaletteHistory[9].r
            prism_spectrum_props.color5[1] = PaletteHistory[9].g
            prism_spectrum_props.color5[2] = PaletteHistory[9].b

            prism_spectrum_props.online_palette_index = Palette_idHistory[1]

        elif prism_spectrum_props.history_count == 0:
            prism_spectrum_props.color1[0] = PaletteHistory[10].r
            prism_spectrum_props.color1[1] = PaletteHistory[10].g
            prism_spectrum_props.color1[2] = PaletteHistory[10].b

            prism_spectrum_props.color2[0] = PaletteHistory[11].r
            prism_spectrum_props.color2[1] = PaletteHistory[11].g
            prism_spectrum_props.color2[2] = PaletteHistory[11].b

            prism_spectrum_props.color3[0] = PaletteHistory[12].r
            prism_spectrum_props.color3[1] = PaletteHistory[12].g
            prism_spectrum_props.color3[2] = PaletteHistory[12].b

            prism_spectrum_props.color4[0] = PaletteHistory[13].r
            prism_spectrum_props.color4[1] = PaletteHistory[13].g
            prism_spectrum_props.color4[2] = PaletteHistory[13].b

            prism_spectrum_props.color5[0] = PaletteHistory[14].r
            prism_spectrum_props.color5[1] = PaletteHistory[14].g
            prism_spectrum_props.color5[2] = PaletteHistory[14].b

            prism_spectrum_props.online_palette_index = Palette_idHistory[2]

        prism_spectrum_props.hue_slider = 0.0
        prism_spectrum_props.saturation_slider = 0.0
        prism_spectrum_props.value_slider = 0.0
        return{'FINISHED'}

class PaletteShuffle(bpy.types.Operator):
    """Shuffle the Order of colors in the Palette"""
    bl_idname="spectrum_palette.palette_shuffle"
    bl_label="Shufle Palette"

    def execute(self, context):
        prism_spectrum_props = bpy.context.scene.prism_spectrum_props

        col1 = Color()
        col2 = Color()
        col3 = Color()
        col4 = Color()
        col5 = Color()

        col1.r = prism_spectrum_props.color1[0]
        col1.g = prism_spectrum_props.color1[1]
        col1.b = prism_spectrum_props.color1[2]

        col2.r = prism_spectrum_props.color2[0]
        col2.g = prism_spectrum_props.color2[1]
        col2.b = prism_spectrum_props.color2[2]

        col3.r = prism_spectrum_props.color3[0]
        col3.g = prism_spectrum_props.color3[1]
        col3.b = prism_spectrum_props.color3[2]

        col4.r = prism_spectrum_props.color4[0]
        col4.g = prism_spectrum_props.color4[1]
        col4.b = prism_spectrum_props.color4[2]

        col5.r = prism_spectrum_props.color5[0]
        col5.g = prism_spectrum_props.color5[1]
        col5.b = prism_spectrum_props.color5[2]

        index = [1, 2, 3, 4, 5]
        random.shuffle(index)

        exec("prism_spectrum_props.color"+str(index[0])+" = col1.r, col1.g, col1.b, 1.0")
        exec("prism_spectrum_props.color"+str(index[1])+" = col2.r, col2.g, col2.b, 1.0")
        exec("prism_spectrum_props.color"+str(index[2])+" = col3.r, col3.g, col3.b, 1.0")
        exec("prism_spectrum_props.color"+str(index[3])+" = col4.r, col4.g, col4.b, 1.0")
        exec("prism_spectrum_props.color"+str(index[4])+" = col5.r, col5.g, col5.b, 1.0")

        prism_spectrum_props.history_count = 0.0

        PaletteHistory[14].r = prism_spectrum_props.color5[0]
        PaletteHistory[14].g = prism_spectrum_props.color5[1]
        PaletteHistory[14].b = prism_spectrum_props.color5[2]

        PaletteHistory[13].r = prism_spectrum_props.color4[0]
        PaletteHistory[13].g = prism_spectrum_props.color4[1]
        PaletteHistory[13].b = prism_spectrum_props.color4[2]

        PaletteHistory[12].r = prism_spectrum_props.color3[0]
        PaletteHistory[12].g = prism_spectrum_props.color3[1]
        PaletteHistory[12].b = prism_spectrum_props.color3[2]

        PaletteHistory[11].r = prism_spectrum_props.color2[0]
        PaletteHistory[11].g = prism_spectrum_props.color2[1]
        PaletteHistory[11].b = prism_spectrum_props.color2[2]

        PaletteHistory[10].r = prism_spectrum_props.color1[0]
        PaletteHistory[10].g = prism_spectrum_props.color1[1]
        PaletteHistory[10].b = prism_spectrum_props.color1[2]

        prism_spectrum_props.hue_slider = 0.0
        prism_spectrum_props.saturation_slider = 0.0
        prism_spectrum_props.value_slider = 0.0
        return{'FINISHED'}

class DeletePalette(bpy.types.Operator):
    """Delete the Current Selected Palette"""
    bl_idname = "spectrum.save_palette_remove"
    bl_label = "Delete"

    def execute(self, context):
        prism_spectrum_props=bpy.context.scene.prism_spectrum_props
        name = prism_spectrum_props.saved_palettes
        name = name.lower()
        name = name.replace(' ', '_')
        path = os.path.join(os.path.dirname(__file__), name+".json")
        try:
            os.remove(path)
        except:
            pass

        if prism_spectrum_props.sync_path is not None:
            try:
                path = os.path.join(prism_spectrum_props.sync_path, name+".json")
                os.remove(path)
            except:
                pass
        return{'FINISHED'}

def register():
    try:
        bpy.utils.register_module(__name__)
    except:
        pass
    global icons_dict
    icons_dict = bpy.utils.previews.new()
    icons_dir = os.path.join(os.path.dirname(__file__), "icons")
    icons_dict.load("blenderskool", os.path.join(icons_dir, "blenderskool_logo.png"), 'IMAGE')
    icons_dict.load("youtube", os.path.join(icons_dir, "youtube_icon.png"), 'IMAGE')
    bpy.types.Scene.prism_spectrum_props = bpy.props.PointerProperty(type=SpectrumProperties)
    bpy.types.Material.prism_spectrum_props = bpy.props.PointerProperty(type=SpectrumMaterialProps)
    bpy.app.handlers.frame_change_pre.append(pre_frame_change)

def unregister():
    global icons_dict
    bpy.utils.previews.remove(icons_dict)
    bpy.context.scene.prism_spectrum_props.new_file = 1
    del bpy.types.Scene.prism_spectrum_props
    del bpy.types.Material.prism_spectrum_props
    palette.clear()
    bpy.utils.unregister_module(__name__)

def pre_frame_change(scene):
    if scene.render.engine == 'CYCLES':
        for m in bpy.data.materials:
            if m.node_tree is not None:
                for n in m.node_tree.nodes:
                    if n.bl_idname == 'spectrum_palette.node':
                        v = n.color1
                        n.color1 = v

                        v = n.color2
                        n.color2 = v

                        v = n.color3
                        n.color3 = v

                        v = n.color4
                        n.color4 = v

                        v = n.color5
                        n.color5 = v