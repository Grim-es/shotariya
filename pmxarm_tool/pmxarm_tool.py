# -*- coding: utf-8 -*-

bl_info = {
    'name': 'pmxarm_tool',
    'author': 'shotariya desu',
    'version': (0, 0, 8),
    'blender': (2, 79, 0),
    'description': 'Fix an armature of MMD models for Unity',
    'location': 'Space Menu',
    'warning': '',
    'wiki_url': '',
    'category': 'Object'
    }

import bpy


def main(self, context):
    bone_list = ['ControlNode', 'ParentNode', 'Center', 'CenterTip', 'Groove', 'Waist', 'LowerBody2', 'Eyes', 'EyesTip',
                 'LowerBodyTip', 'UpperBody2Tip', 'GrooveTip', 'NeckTip']
    bone_list_with = ['_shadow_', '_dummy_', 'Dummy_', 'WaistCancel', 'LegIKParent', 'LegIK', 'LegIKTip', 'ToeTipIK',
                      'ToeTipIKTip', 'ShoulderP_', 'EyeTip_', 'ThumbTip_', 'IndexFingerTip_', 'MiddleFingerTip_',
                      'RingFingerTip_', 'LittleFingerTip_', 'HandDummy_', 'ArmTwist', 'HandTwist', 'LegD', 'KneeD_L',
                      'AnkleD', 'LegTipEX', 'HandTip_', 'ShoulderC_', 'SleeveShoulderIK_']
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
        'Knee_L': 'Leg_L',
        'Knee_R': 'Leg_R',
        'AnkleD_L': 'Ankle_L',
        'AnkleD_R': 'Ankle_R',
        'Ankle_L': 'Knee_L',
        'Ankle_R': 'Knee_R',
        'LegTipEX_L': 'ToeTip_L',
        'LegTipEX_R': 'ToeTip_R',
        'ToeTip_L': 'Ankle_L',
        'ToeTip_R': 'Ankle_R'
    }
    bone_list_weight= {
        'LegD_L': 'Left leg',
        'LegD_R': 'Right leg',
        'KneeD_L': 'Left knee',
        'KneeD_R': 'Right knee',
        'AnkleD_L': 'Left ankle',
        'AnkleD_R': 'Right ankle',
        'LegTipEX_L': 'Left toe',
        'LegTipEX_R': 'Right toe',
        'Shoulder_L': 'ShoulderC_L',
        'Shoulder_R': 'ShoulderC_R',
        'Shoulder_L': 'SleeveShoulderIK_L',
        'Shoulder_R': 'SleeveShoulderIK_R',
        'ArmTwist_L': 'Left arm',
        'ArmTwist_R': 'Right arm',
        'ArmTwist1_L': 'Left arm',
        'ArmTwist1_R': 'Right arm',
        'ArmTwist2_L': 'Left arm',
        'ArmTwist2_R': 'Right arm',
        'ArmTwist3_L': 'Left arm',
        'ArmTwist3_R': 'Right arm',
        'HandTwist_L': 'Left elbow',
        'HandTwist_R': 'Right elbow',
        'HandTwist1_L': 'Left elbow',
        'HandTwist1_R': 'Right elbow',
        'HandTwist2_L': 'Left elbow',
        'HandTwist2_R': 'Right elbow',
        'HandTwist3_L': 'Left elbow',
        'HandTwist3_R': 'Right elbow'
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

    def delete_hierarchy(obj):
        names = {obj.name}

        def get_child_names(objz):
            for child in objz.children:
                names.add(child.name)
                if child.children:
                    get_child_names(child)

        get_child_names(obj)
        objects = bpy.data.objects
        [setattr(objects[n], 'select', True) for n in names]

        bpy.ops.object.delete()
        
    bpy.ops.object.hide_view_clear()
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

    for obj in bpy.data.objects:
        obj.select = False
        if obj.type == 'ARMATURE':
            bpy.context.scene.objects.active = obj
            obj.select = True

    armature = bpy.context.scene.objects.active

    if armature is not None:
        if armature.type != 'ARMATURE':
            self.report({'ERROR'}, 'Select Armature')
            return {'CANCELLED'}

    bpy.ops.object.mode_set(mode='EDIT')

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

    for bone in armature.data.edit_bones:
        if bone.name in bone_list or bone.name.startswith(tuple(bone_list_with)):
            armature.data.edit_bones.remove(bone)

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    
    for obj in bpy.data.objects:
        if obj.name == 'rigidbodies' or obj.name == 'joints':
            delete_hierarchy(obj)
            bpy.data.objects.remove(obj)
            
    for obj in bpy.data.objects:
        obj.select = False
        if obj.type == 'MESH':
            bpy.context.scene.objects.active = obj
            obj.select = True

    mesh = bpy.context.scene.objects.active
    
    for key, value in bone_list_weight.items():
        pb = mesh.vertex_groups.get(key)
        pb2 = mesh.vertex_groups.get(value)
        if pb is None or pb2 is None:
            continue
        bpy.ops.object.modifier_add(type='VERTEX_WEIGHT_MIX')
        bpy.context.object.modifiers['VertexWeightMix'].vertex_group_a = value
        bpy.context.object.modifiers['VertexWeightMix'].vertex_group_b = key
        bpy.context.object.modifiers['VertexWeightMix'].mix_mode = 'ADD'
        bpy.context.object.modifiers['VertexWeightMix'].mix_set = 'B'
        bpy.ops.object.modifier_apply(modifier='VertexWeightMix')
        mesh.vertex_groups.remove(pb)

    armature.data.pose_position = 'REST'
    bpy.ops.object.select_all(action='DESELECT')


class FixPMXArmature(bpy.types.Operator):
    bl_idname = 'pmxarm_tool.fix_an_armature'
    bl_label = 'Fix an armature'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(self, context)
        self.report({'INFO'}, 'Armature fixing has finished.')
        return {'FINISHED'}


class FixPMXHips(bpy.types.Operator):
    bl_idname = 'pmxarm_tool.fix_my_hips'
    bl_label = 'Fix my hips'

    def execute(self, context):
        self.report({'INFO'}, 'This feature has not yet been scripted.')
        return {'FINISHED'}


class PMXArmToolPpanel(bpy.types.Panel):
    bl_label = 'pmxarm_tool'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = 'objectmode'
    bl_category = 'pmxarm'
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def draw(self, context):
        layout = self.layout
        armature = context.active_object
        if armature is not None:
            layout.label(text = 'PMX Armature:')
            layout.operator('pmxarm_tool.fix_an_armature', icon = 'POSE_HLT',
                            text = 'Fix Armature')
            layout.operator('pmxarm_tool.fix_my_hips', icon = 'BONE_DATA',
                            text = 'Fix Hips')
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


if __name__ == '__main__':
    register()
