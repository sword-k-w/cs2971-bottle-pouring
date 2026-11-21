"""04 · 量筒刻度标定采图（引导式）。感知组离线标定的核心素材。

流程: 把量筒放上托盘 B → 加水到指定刻度 → 回车 → 从头部相机(彩色+深度)与双腕
相机各拍一张，同时记录当前底盘里程计（离线标定必须知道拍照时机器人站在哪）。

机器人位置全程不动；量筒每次摆放尽量一致（可用胶带在托盘上做标记）。

用法: python 04_cylinder_calib_capture.py --server 192.168.10.1:50051 --levels 0,25,50,75,100
"""
import argparse
import datetime
import pathlib
import time

from common import connect_robot, dump_json, save_image, to_dict_safe


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--server", default="192.168.10.1:50051")
    ap.add_argument(
        "--levels",
        default="0,25,50,75,100",
        help="液位档位(mL)，按量筒实际量程现场调整，逗号分隔",
    )
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    robot = connect_robot(args.server)
    outdir = pathlib.Path(
        args.out or f"data/cylinder_calib/{datetime.datetime.now():%Y%m%d_%H%M%S}"
    )
    outdir.mkdir(parents=True, exist_ok=True)

    cameras = [
        ("head_rgb", robot.head_camera.get_rgb_image),
        ("head_depth", robot.head_camera.get_depth_image),
        ("left_wrist", robot.left_arm_camera.get_raw_image),
        ("right_wrist", robot.right_arm_camera.get_raw_image),
    ]

    print("=== 量筒标定采图 ===")
    print("要求: 量筒立放在托盘 B 的标记位置；加水到指定刻度；")
    print("      回车后自动拍照并记录底盘位姿。机器人全程不要移动。\n")

    for level in [s.strip() for s in args.levels.split(",") if s.strip()]:
        lvdir = outdir / f"level_{level}mL"
        lvdir.mkdir(parents=True, exist_ok=True)
        input(f">>> 将量筒加水至 {level} mL，放回托盘 B 标记位置，然后回车…")
        for name, fn in cameras:
            try:
                save_image(fn(), str(lvdir / name))
            except Exception as e:
                print(f"  {name} 不可用: {type(e).__name__}: {e}")
        odom = to_dict_safe(robot.chassis.get_odometry())
        dump_json({"level_mL": level, "odometry": odom}, str(lvdir / "robot_pose.json"))
        print()

    print(f"标定采图完成 ✓ 全部保存在 {outdir}")
    print("回去后: 对 head_rgb 各液位照片检测凹液面下缘 → 拟合 像素行 ↔ 体积 关系；")
    print("        head_depth 可用于辅助液面/量筒定位；robot_pose.json 用于复现拍照位姿。")


if __name__ == "__main__":
    main()
