#!/usr/bin/env bash
# 创建虚拟环境并安装 x2robot SDK。
#
# 运行位置：在你带去实验室的笔记本上跑（WSL/Ubuntu/Windows 均可），
# 不是机器人上——机器人自带 SDK 服务端，无需安装任何东西。
# 谁要跑 SDK 脚本，谁就在自己笔记本上装一份，一条命令的事。
#
# 用法: bash setup_env.sh <x2robot*.whl 路径> [python 版本，默认 3.12]
# 示例: bash setup_env.sh ~/Downloads/x2robot_sdk-2.0.0-cp310-cp310-manylinux_2_35_x86_64.whl
#
# 注意:
# - v1.1.2 固定 numpy==1.26.4，Python 最高 3.12；v2.0.0 支持 3.10~3.13。
#   默认 3.12 两个版本都兼容。
# - v2.0.0 是 manylinux wheel，仅 Linux；Windows 上只能装 v1.1.2（py3-none-any）。
# - 没有 uv 时自动退回 python3 -m venv + pip。
set -euo pipefail

WHEEL="${1:?用法: bash setup_env.sh <wheel 路径> [python 版本，默认 3.12]}"
PYVER="${2:-3.12}"

DEPS="grpcio grpcio-tools protobuf betterproto2 PyYAML numpy opencv-python typer av matplotlib toppra"

if command -v uv >/dev/null 2>&1; then
    echo "==> 使用 uv（若未安装: curl -LsSf https://astral.sh/uv/install.sh | sh）"
    uv venv .venv --python "$PYVER"
    uv pip install --python .venv $DEPS
    uv pip install --python .venv "$WHEEL"
    .venv/bin/python -c "from x2robot import connect; print('x2robot SDK 安装成功 ✓')"
else
    echo "==> 未找到 uv，退回 python3 -m venv + pip（建议装 uv，见上）"
    python3 -m venv .venv
    # shellcheck disable=SC1091
    source .venv/bin/activate
    pip install --upgrade pip
    # 国内网络慢可加: -i https://pypi.tuna.tsinghua.edu.cn/simple
    pip install $DEPS
    pip install "$WHEEL"
    python -c "from x2robot import connect; print('x2robot SDK 安装成功 ✓')"
fi

echo "下一步: .venv/bin/python 00_check_connect.py --help"
