# CS2971 Bottle Pouring

CS2971（2026-2027 Fall）具身智能课程大作业 · **轮式双臂赛道**（量子一号 Pro / Quantum X1 Pro）。

任务：**取瓶量液** —— 根据指令选取指定颜色的瓶子，向量筒中倒入指定体积的液体。
评分、测试流程与提交要求见 [assignment.md](assignment.md)。

## 目录结构

```
.
├── assignment.md                  # 赛道大作业要求（原《轮式双臂大作业：取瓶量液》）
├── arena/
│   └── arena.jpg                  # 任务场地照片
├── docs/
│   ├── course-overview.md         # 课程总 README（赛道总览、时间线、评分说明）
│   └── quantum-x1-pro-manual.pdf  # 量子一号 Pro 产品说明手册
└── wall-x/                        # wall-x 开源全链路框架（git submodule）
```

## 协作约定

- 每人只在个人分支上工作（命名 `<名字缩写>/<主题>`），**禁止直接提交到 `main`**。
- `main` 由 [sword-k-w](https://github.com/sword-k-w) 统一管理：从个人分支提 Pull Request 合并。
- AI 编码助手（Claude Code 等）在本仓库工作时，请遵循 [CLAUDE.md](CLAUDE.md)（[AGENTS.md](AGENTS.md) 同样指向它）。
- 模型权重、视频、数据集等大文件不入库，放网盘并在仓库内注明下载位置。

## wall-x 子模块

wall-x（Apache-2.0）是量子一号配套的开源软件栈，覆盖数据采集、遥操作、VLA 后训练与微调、真机部署、SDK、建图导航与仿真评测：

```bash
git submodule update --init wall-x
```

官方开发者文档：https://x2robot.com/docs/quantax1pro/v1/model-development/wall-oss/model-introduction

## 时间线

| 时间 | 事项 |
| --- | --- |
| W10 周四 23:59:59 前 | 中期报告（≤4 页） |
| W16 周二 23:59:59 前 | 最终真机测试 + Canvas 提交全部材料 |
| W16 | 答辩展示（视频 Demo 20% + presentation 10%） |

机器人实验室：学生中心 D313。
