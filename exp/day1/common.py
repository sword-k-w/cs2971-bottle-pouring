"""真机实验共用工具。依赖 x2robot SDK（安装见 setup_env.sh）。

所有脚本都惰性导入 x2robot：没装 SDK 时 `--help` 依然可用。
"""
from __future__ import annotations

import json
import time
from dataclasses import is_dataclass


def connect_robot(server: str):
    """连接机器人 SDK 服务端。server 形如 "192.168.10.1:50051"。"""
    from x2robot import connect

    return connect(f"x2://{server}")


def enter_sdk_mode(robot) -> None:
    """切到 SDK 工作模式 + 机械臂关节位置控制模式（所有动作用的脚本第一步）。"""
    from x2robot.sdk import (
        ManipulatorControlMode,
        ManipulatorControlModeParam,
        RobotModeParam,
        RobotWorkMode,
    )

    r = robot.system.set_work_mode(RobotModeParam(mode=RobotWorkMode.SDK))
    print(f"[mode] set_work_mode(SDK): success={r.is_success}, msg={r.error_message}")
    r2 = robot.robot_control.set_manipulator_control_mode(
        ManipulatorControlModeParam(
            mode=ManipulatorControlMode.MANIPULATOR_JOINT_POSITIONS
        )
    )
    print(
        f"[mode] set_manipulator_control_mode(JOINT_POSITIONS): "
        f"success={r2.is_success}, msg={r2.error_message}"
    )


def decode_image(img):
    """解码 SDK 返回的 CompressedImage。

    彩色 → BGR 8bit ndarray；深度 → 16bit ndarray（深度流带 12 字节头，见官方 camera.py）。
    """
    import cv2
    import numpy as np

    if img is None or not getattr(img, "data", None):
        print("  警告: 收到空图像，跳过")
        return None
    data = bytes(img.data)
    is_depth = "depth" in (getattr(img, "format", "") or "").lower()
    if is_depth:
        data = data[12:]
    arr = np.frombuffer(data, np.uint8)
    frame = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED if is_depth else cv2.IMREAD_COLOR)
    return frame


def save_image(img, stem: str) -> None:
    """保存一张图像：8bit 存 .jpg，16bit（深度）存 .png。stem 不含扩展名。"""
    import cv2
    import numpy as np

    frame = decode_image(img)
    if frame is None:
        print(f"  警告: 解码失败，跳过 {stem}")
        return
    ext = ".jpg" if frame.dtype == np.uint8 else ".png"
    path = stem + ext
    ok = cv2.imwrite(path, frame)
    print(f"  已保存 {path}" + ("" if ok else "  <-- 保存失败!"))


def to_dict_safe(obj, depth: int = 0):
    """把 SDK 返回的消息对象转成可 json 序列化的结构（尽力而为，仅供导出查看）。"""
    if obj is None:
        return None
    if depth > 4:
        return str(obj)
    if hasattr(obj, "to_dict") and callable(obj.to_dict):
        try:
            return obj.to_dict()
        except Exception:
            pass
    if isinstance(obj, (int, float, str, bool)):
        return obj
    if isinstance(obj, (list, tuple)):
        return [to_dict_safe(x, depth + 1) for x in obj]
    if isinstance(obj, dict):
        return {str(k): to_dict_safe(v, depth + 1) for k, v in obj.items()}
    if is_dataclass(obj):
        return {k: to_dict_safe(v, depth + 1) for k, v in vars(obj).items()}
    return str(obj)


def dump_json(data, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)
    print(f"已保存 {path}")


def ask(prompt: str) -> bool:
    """等待确认：y/回车继续，其余跳过。"""
    ans = input(f"{prompt} [y/N] ").strip().lower()
    return ans in ("y", "yes")


def sleep(s: float) -> None:
    time.sleep(s)
