# -*- coding: utf-8 -*-

bl_info = {
    "name": "pmxarm_tool",
    "author": "shotariya desu",
    "version": (0, 0, 7),
    "blender": (2, 79, 0),
    "description": "Fix an armature of MMD models for Unity",
    "location": "Space Menu",
    "warning": "",
    "wiki_url": "",
    "category": "Object"
    }

import bpy


def main(self, context):
    bone_list = ['ControlNode', 'ParentNode', 'Center', 'CenterTip', 'Groove', 'Waist', 'LowerBody2', 'Eyes', 'EyesTip']
    bone_list_with = ['_shadow_', '_dummy_', 'Dummy_', 'WaistCancel', 'LegIKParent', 'LegIK', 'LegIKTip', 'ToeTipIK',
                      'ToeTipIKTip', 'ShoulderP_']
    bone_list_parenting = {
        'UpperBody': 'LowerBody',
        'Shoulder_L': 'UpperBody2',
        'Shoulder_R': 'UpperBody2',
        'Arm_L': 'Shoulder_L',
        'Arm_R': 'Shoulder_R',
        'Elbow_L': 'Arm_L',
        'Elbow_R': 'Arm_R',
        'Wrist_L': 'Elbow_L',
        'Wrist_R': 'Elbow_R',
        'LegD_L': 'Leg_L',
        'LegD_R': 'Leg_R',
        'KneeD_L': 'Knee_L',
        'KneeD_R': 'Knee_R',
        'AnkleD_L': 'Ankle_L',
        'AnkleD_R': 'Ankle_R',
        'LegTipEX_L': 'ToeTip_L',
        'LegTipEX_R': 'ToeTip_R'
    }
    bone_list_translate = {
        'LowerBody': 'Hips',
        'Leg_L': 'Left leg',
        'Leg_R': 'Right leg',
        'Knee_L': 'Left knee',
        'Knee_R': 'Right knee',
        'Ankle_L': 'Left ankle',
        'Ankle_R': 'Right ankle',
        'ToeTip_L': 'Left toe',
        'ToeTip_R': 'Right toe',
        'UpperBody': 'Spine',
        'UpperBody2': 'Chest',
        'Shoulder_L': 'Left shoulder',
        'Shoulder_R': 'Right shoulder',
        'Arm_L': 'Left arm',
        'Arm_R': 'Right arm',
        'Elbow_L': 'Left elbow',
        'Elbow_R': 'Right elbow',
        'Wrist_L': 'Left wrist',
        'Wrist_R': 'Right wrist'
}

    armature = bpy.context.object
    if armature is not None:
        if armature.type != 'ARMATURE':
            self.report({'ERROR'}, 'Select Armature')
            return {'CANCELLED'}
    bpy.ops.object.mode_set(mode='EDIT')
    for bone in armature.data.edit_bones:
        if bone.name in bone_list or bone.name.startswith(tuple(bone_list_with)):
            armature.data.edit_bones.remove(bone)
    for key, value in bone_list_parenting.items():
        pb = armature.pose.bones.get(key)
        pb2 = armature.pose.bones.get(value)
        if pb is None or pb2 is None:
            continue
        armature.data.edit_bones[key].parent = armature.data.edit_bones[value]
    for key, value in bone_list_translate.items():
        pb = armature.pose.bones.get(key)
        if pb is None:
            continue
        pb.name = value
    bpy.ops.object.mode_set(mode='OBJECT')
    armature.data.pose_position = 'REST'


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
        armature = context.active_object
        if armature is not None:
            layout.label(text = 'PMX Armature:')
            if armature.type == 'ARMATURE':
                layout.operator('pmxarm_tool.fix_an_armature', icon = 'POSE_HLT',
                                text = 'Fix Armature')
                layout.operator('pmxarm_tool.fix_my_hips', icon = 'BONE_DATA',
                                text = 'Fix Hips')
            else:
                layout.operator('pmxarm_tool.fix_an_armature', icon = 'ERROR',
                                text = 'Select Armature')
                layout.operator('pmxarm_tool.fix_my_hips', icon = 'ERROR',
                                text = 'Select Armature')
        else:
            layout.label(text = 'Select a MMD model')


def register():
    bpy.utils.register_class(FixPMXArmature)
    bpy.utils.register_class(FixPMXHips)
    bpy.utils.register_class(PMXArmToolPpanel)


def unregister():
    bpy.utils.unregister_class(FixPMXArmature)
    bpy.utils.unregister_class(FixPMXHips)
    bpy.utils.unregister_class(PMXArmToolPpanel)


if __name__ == "__main__":
    register()
