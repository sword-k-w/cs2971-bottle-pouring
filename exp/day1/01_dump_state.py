"""01 · 状态全量导出：关节角、末端位姿、夹爪、腰身、头部、底盘、IMU、系统信息。

用法: python 01_dump_state.py --server 192.168.10.1:50051 [--out data/state.json]
输出: 一个 JSON 文件，供集成组离线核对 API 字段语义（单位/坐标系/正负号）。
"""
import argparse
import datetime

from common import connect_robot, dump_json, to_dict_safe


def try_get(fn, *a, **kw):
    """单个接口读取出错不影响整体导出。"""
    try:
        return to_dict_safe(fn(*a, **kw))
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--server", default="192.168.10.1:50051")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    robot = connect_robot(args.server)
    out = {"model": robot.get_robot_model()}

    out["static_info"] = try_get(robot.system.get_static_info)
    out["dynamic_info"] = try_get(robot.system.get_dynamic_info)
    out["robot_status"] = try_get(robot.get_robot_status, fields=[])
    out["all_joint_states"] = try_get(robot.state.get_all_joint_states)

    for side in ("left", "right"):
        arm = getattr(robot, f"{side}_arm")
        out[f"{side}_arm"] = {
            "joint_states": try_get(arm.get_joint_states),
            "end_pose": try_get(arm.get_end_pose),
        }
        out[f"{side}_gripper"] = try_get(getattr(robot, f"{side}_gripper").get_position)

    out["lift"] = try_get(robot.lift.get_lift_position)
    out["head"] = try_get(robot.head.get_pose)
    out["chassis"] = {
        "odometry": try_get(robot.chassis.get_odometry),
        "global_position": try_get(robot.chassis.get_global_position),
        "relative_position": try_get(robot.chassis.get_relative_position),
        "control_mode": try_get(robot.chassis.get_control_mode),
    }
    out["imu"] = try_get(robot.imu.get_chassis_imu)

    path = args.out or f"data/state_dump_{datetime.datetime.now():%Y%m%d_%H%M%S}.json"
    dump_json(out, path)
    print("导出完成 ✓ 回去后与集成组核对各字段单位（rad/m/deg）")


if __name__ == "__main__":
    main()
