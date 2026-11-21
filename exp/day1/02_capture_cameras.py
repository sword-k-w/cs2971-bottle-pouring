"""02 · 相机连拍：每个相机源拍 N 张，保存到 data/cameras/<时间戳>/。

彩色存 .jpg，深度存 .png（16bit）。画面里必须拍到真实场地（托盘/瓶子/量筒），
这组照片是感知组离线开发（颜色识别、刻度标定）的全部素材。

用法: python 02_capture_cameras.py --server 192.168.10.1:50051 --frames 5
"""
import argparse
import datetime
import pathlib
import time

from common import connect_robot, save_image


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--server", default="192.168.10.1:50051")
    ap.add_argument("--frames", type=int, default=5, help="每个相机拍几张")
    ap.add_argument("--interval", type=float, default=0.5, help="连拍间隔秒")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    robot = connect_robot(args.server)
    outdir = pathlib.Path(args.out or f"data/cameras/{datetime.datetime.now():%Y%m%d_%H%M%S}")
    outdir.mkdir(parents=True, exist_ok=True)

    # (名称, 取图函数)。双目/肘部相机不一定配齐，出错只跳过不中断。
    sources = [
        ("head_rgb", robot.head_camera.get_rgb_image),
        ("head_depth", robot.head_camera.get_depth_image),
        ("head_left_eye", robot.head_camera.get_left_eye_image),
        ("head_right_eye", robot.head_camera.get_right_eye_image),
        ("left_wrist", robot.left_arm_camera.get_raw_image),
        ("right_wrist", robot.right_arm_camera.get_raw_image),
        ("left_elbow", robot.left_arm_camera.get_elbow_image),
        ("right_elbow", robot.right_arm_camera.get_elbow_image),
    ]

    for name, fn in sources:
        print(f"[相机] {name}")
        try:
            for i in range(args.frames):
                save_image(fn(), str(outdir / f"{name}_{i:03d}"))
                if i < args.frames - 1:
                    time.sleep(args.interval)
        except Exception as e:
            print(f"  该相机不可用: {type(e).__name__}: {e}")

    print(f"全部保存至 {outdir}")
    print("提示: 拍的时候让场地保持最终布局（托盘 A 四个瓶子 + 托盘 B 量筒就位）")


if __name__ == "__main__":
    main()
