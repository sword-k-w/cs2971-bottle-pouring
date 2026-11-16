# CLAUDE.md

CS2971 具身智能大作业「取瓶量液」仓库（轮式双臂赛道）。项目背景、目录结构与时间线见 [README.md](README.md)。

## 协作约定（协作者与 AI 助手都须遵守）

1. **分支隔离**：每人只在个人分支上工作，**禁止直接向 `main` 提交或推送**。分支命名 `<名字缩写>/<主题>`。
2. **`main` 由 owner（sword-k-w）统一管理**。合并进 `main` 必须从个人分支提 Pull Request，等 sword-k-w 审查合并。
3. **AI 助手不得自行写远端**：AI 助手（Claude Code 等）不得自行 commit、push（含 force-push）、创建或合并 PR；必须先展示改动与命令，经使用者明确同意后才能执行。
4. 提交信息用英文、动词开头、简明（如 `feat: add color-based bottle grasping`）。
5. 大文件（模型权重、视频、数据集）不入库，放网盘并在仓库内注明下载位置。
6. 课程资料（assignment.md、docs/）的改动同样走分支 + PR，不直接提交。

## 常用操作

```bash
# 首次克隆（含 wall-x 子模块）
git clone --recurse-submodules https://github.com/sword-k-w/cs2971-bottle-pouring.git
cd cs2971-bottle-pouring

# 开个人分支
git checkout -b <name>/<topic>

# 同步 main 的最新改动
git fetch origin && git merge origin/main

# 推送个人分支
git push -u origin <name>/<topic>
```

## 关键文件

- `assignment.md` — 赛道任务、测试流程与计分规则
- `docs/course-overview.md` — 课程时间线与评分构成
- `docs/quantum-x1-pro-manual.pdf` — 量子一号 Pro 硬件手册
- `wall-x/` — 官方开源全链路框架（git 子模块）。子模块内的改动不会被本仓库记录；如需改动 wall-x，fork 上游仓库，或在本仓库单独目录维护补丁/脚本
