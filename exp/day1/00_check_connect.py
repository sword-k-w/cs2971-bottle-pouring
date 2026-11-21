"""00 · SDK 连通性检查：ping + 机型 + 基本信息。当天第一件事。

用法: python 00_check_connect.py --server 192.168.10.1:50051
预期: ping 响应 Pong to: Hello, X2Robot!，并打印电量。
"""
import argparse

from common import connect_robot


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--server", default="192.168.10.1:50051", help="机器人 IP:端口")
    args = ap.parse_args()

    robot = connect_robot(args.server)
    print(f"已连接，机型: {robot.get_robot_model()}")

    from x2robot.sdk import PingRequest

    resp = robot.benchmark.ping(PingRequest(payload="Hello, X2Robot!"))
    print(f"ping 响应: {resp.payload}")
    if resp.payload == "Pong to: Hello, X2Robot!":
        print("Connection to X2Robot SDK server successful ✓")
    else:
        print("!! 响应内容与预期不符，检查 SDK 版本是否匹配固件")

    info = robot.system.get_dynamic_info()
    try:
        p = info.power_status
        print(f"电量: {p.value}%, 充电中: {p.is_charging}")
    except Exception as e:
        print(f"读取电量失败: {e}")

    static = robot.system.get_static_info()
    print(f"静态信息: {static}")


if __name__ == "__main__":
    main()
