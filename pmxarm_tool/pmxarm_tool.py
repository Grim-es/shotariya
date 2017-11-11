# Save as: pmxarm_tool.py
#
# How to instal:
# File > User Preferences > Add-ons > 
#     Install Add-on from File.. > Select this file
#     Save User Settings
#
#
# Author: shotariya
# Downloaded from: https://pastebin.com/raw/uSGRv1uv


bl_info = {
    "name": "pmxarm_tool",
    "author": "shotariya desu",
    "version": (0, 0, 6),
    "blender": (2, 79, 0),
    "description": "Fix an armature of MMD models for Unity",
    "location": "Space Menu",
    "warning": "",
    "wiki_url": "",
    "category": "Object"
    }

import bpy


def main(self, context):
    bone_list = ['ControlNode', 'ParentNode', 'Center', 'CenterTip', 'Groove', 'Waist',
                 'LegIKParent_L', 'LowerBody2', 'Eyes']
    bone_list_with = ['_shadow_', '_dummy_', 'LegIKParent', 'LegIK', 'LegIKTip', 'ToeTipIK',
                      'ToeTipIKTip', 'WaistCancel', 'Dummy_']
    bone_list_parenting = {'LowerBody': 'UpperBody', 'UpperBody2': 'Shoulder_L',
                           'UpperBody2': 'Shoulder_R', 'Shoulder_L': 'Arm_L', 'Shoulder_R': 'Arm_R',
                           'Arm_L': 'Elbow_L', 'Arm_R': 'Elbow_R', 'Elbow_L': 'Wrist_L',
                           'Elbow_R': 'Wrist_R', 'Leg_L': 'LegD_L', 'Knee_L': 'KneeD_L',
                           'Ankle_L': 'AnkleD_L', 'ToeTip_L': 'LegTipEX_L', 'Leg_R': 'LegD_R',
                           'Knee_R': 'KneeD_R', 'Ankle_R': 'AnkleD_R', 'ToeTip_R': 'LegTipEX_R'}
    bone_list_translate = {'LowerBody': 'Hips', 'Leg_L': 'Left leg', 'Knee_L': 'Left knee',
                            'Ankle_L': 'Left ankle', 'ToeTip_L': 'Left toe', 'Leg_R': 'Right leg',
                            'Knee_R': 'Right knee', 'Ankle_R': 'Right ankle', 'ToeTip_R': 'Right toe',
                            'UpperBody': 'Spine', 'UpperBody2': 'Chest',
                            'Shoulder_L': 'Left shoulder', 'Arm_L': 'Left arm',
                            'Elbow_L': 'Left elbow', 'Wrist_L': 'Left wrist',
                            'Shoulder_R': 'Right shoulder', 'Arm_R': 'Right arm',
                            'Elbow_R': 'Right elbow', 'Wrist_R': 'Right wrist'}

    armature = bpy.context.object
    if armature is not None:
        if armature.type == 'ARMATURE':
            armature_data = armature.data
        else:
            self.report({'ERROR'}, 'Select Armature')
            return {'CANCELLED'}
    bpy.ops.object.mode_set(mode='EDIT')
    for bone in armature_data.edit_bones:
        if bone.name in bone_list or bone.name.startswith(tuple(bone_list_with)):
            armature_data.edit_bones.remove(bone)
    for key, value in bone_list_parenting.items():
        pb = armature.pose.bones.get(key)
        pb2 = armature.pose.bones.get(value)
        if pb is None:
            continue
        if pb2 is None:
            continue
        armature_data.edit_bones[value].parent = armature.data.edit_bones[key]
    for key, value in bone_list_translate.items():
        pb = armature.pose.bones.get(key)
        if pb is None:
            continue
        pb.name = value
    bpy.ops.object.mode_set(mode='OBJECT')
    armature_data.pose_position = 'REST'


class FixPMXArmature(bpy.types.Operator):
    bl_idname = "pmxarm_tool.fix_an_armature"
    bl_label = "Fix an armature"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(self, context)
        self.report({'INFO'}, 'Armature fixing has finished.')
        return {'FINISHED'}


class FixPMXHips(bpy.types.Operator):
    bl_idname = "pmxarm_tool.fix_my_hips"
    bl_label = "Fix an armature"

    def execute(self, context):
        self.report({'INFO'}, 'This feature has not yet been scripted.')
        return {'FINISHED'}


class PMXArmToolPpanel(bpy.types.Panel):
    bl_label = 'pmxarm_tool'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = 'objectmode'
    bl_category = 'pmxarm'

    def draw(self, context):
        layout = self.layout
        layout.label(text = 'PMX Armature:')
        armature = context.active_object
        if armature.type == 'ARMATURE':
            layout.operator('pmxarm_tool.fix_an_armature', icon = 'POSE_HLT', 
                            text = 'Press to Fix')
            layout.operator('pmxarm_tool.fix_my_hips', icon = 'BONE_DATA', 
                            text = 'Fix Hips')
        else:
            layout.operator('pmxarm_tool.fix_an_armature', icon = 'ERROR', 
                            text = 'Select Armature')
            layout.operator('pmxarm_tool.fix_my_hips', icon = 'ERROR', 
                            text = 'Select Armature')


def register():
    bpy.utils.register_class(FixPMXArmature)
    bpy.utils.register_class(PMXArmToolPpanel)
    bpy.utils.register_class(FixPMXHips)


def unregister():
    bpy.utils.unregister_class(FixPMXArmature)
    bpy.utils.unregister_class(PMXArmToolPpanel)
    bpy.utils.unregister_class(FixPMXHips)


if __name__ == "__main__":
    register()
