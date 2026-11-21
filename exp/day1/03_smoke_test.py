"""03 · 交互式冒烟测试：逐项小幅验证各执行器 API（每步回车确认才动作）。

顺序: 夹爪 → 腰身 → 头部 → 机械臂(单关节小角度) → 底盘(相对模式直线往返)。
目的: 核对 API 语义（单位、方向、正负号、限位），不是调参数。
安全: 全程专人守急停；机械臂动作前请助教确认姿态安全；底盘动作前清空周边。

用法: python 03_smoke_test.py --server 192.168.10.1:50051
"""
import argparse
import time

from common import ask, connect_robot, enter_sdk_mode

# X1 六轴限位（弧度，与官方 arm_control.py 一致）
JOINT_LOWER = [-2.792, 0.0, -3.14, -1.57, -1.4, -1.745]
JOINT_UPPER = [2.792, 3.44, 0.0, 1.57, 1.4, 1.745]


def step(msg: str) -> bool:
    print()
    print("=" * 62)
    print("下一步:", msg)
    if not ask("确认执行？"):
        print("已跳过")
        return False
    return True


def clip_joints(q):
    return [
        max(lo, min(hi, v)) for v, lo, hi in zip(q, JOINT_LOWER, JOINT_UPPER)
    ]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--server", default="192.168.10.1:50051")
    args = ap.parse_args()

    robot = connect_robot(args.server)
    enter_sdk_mode(robot)

    from x2robot.sdk import (
        ChassisControlMode,
        ChassisControlModeParam,
        ChassisPosition,
        GripperPosition,
        HeadPose,
        JointPositions,
        LiftPosition,
    )

    # 1. 夹爪（行程 0~4.5）
    if step("左夹爪: 开到 2.0 → 关到 1.0 → 回到 2.0（小开合）"):
        for pos in (2.0, 1.0, 2.0):
            robot.left_gripper.set_position(GripperPosition(position=pos))
            time.sleep(1.0)
        print("左夹爪当前:", robot.left_gripper.get_position())

    # 2. 腰身（行程 0~0.78 m）
    if step("腰身: 从当前位置 +5cm，再回原位"):
        cur = robot.lift.get_lift_position().position
        print(f"当前腰身: {cur:.3f} m")
        robot.lift.set_lift_position(LiftPosition(position=cur + 0.05))
        time.sleep(2)
        robot.lift.set_lift_position(LiftPosition(position=cur))
        time.sleep(2)

    # 3. 头部云台（俯仰 ±30°、偏航 ±90°，接口单位是度）
    if step("头部: 俯仰 +10° 回正；偏航 ±15° 回正"):
        robot.head.set_pose(HeadPose(pitch=10.0, yaw=0.0))
        time.sleep(1)
        robot.head.reset()
        time.sleep(1)
        robot.head.set_pose(HeadPose(pitch=0.0, yaw=15.0))
        time.sleep(1)
        robot.head.set_pose(HeadPose(pitch=0.0, yaw=-15.0))
        time.sleep(1)
        robot.head.reset()

    # 4. 机械臂：单关节小角度往返（只动 J1，其余保持）
    if step("左臂: J1 关节 ±0.15 rad 往返，其余关节不动"):
        js = robot.left_arm.get_joint_states()
        q = list(js.position)
        print("当前关节角(rad):", [f"{v:.3f}" for v in q])
        for delta in (0.15, -0.30, 0.15):
            q[0] += delta
            cmd = JointPositions(positions=clip_joints(q))
            robot.left_arm.set_joint_positions(cmd)
            time.sleep(2)
        js2 = robot.left_arm.get_joint_states()
        print("动作后关节角(rad):", [f"{v:.3f}" for v in js2.position])

    # 5. 底盘：相对坐标模式，直线往返（先设虚拟零点）
    if step("底盘: 相对模式前进 0.2 m 再退回（动作慢，各等 5 秒）"):
        robot.chassis.set_control_mode(
            ChassisControlModeParam(mode=ChassisControlMode.RELATIVE)
        )
        robot.chassis.set_virtual_zero_point(ChassisPosition(x=0.0, y=0.0, yaw=0.0))
        time.sleep(0.5)
        robot.chassis.move_to_relative_position(ChassisPosition(x=0.2, y=0.0, yaw=0.0))
        time.sleep(5)
        robot.chassis.move_to_relative_position(ChassisPosition(x=0.0, y=0.0, yaw=0.0))
        time.sleep(5)

    print()
    print("冒烟测试完成 ✓ 各接口行为已现场验证，回去更新集成组笔记")


if __name__ == "__main__":
    main()
