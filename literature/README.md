# 文献清单（取瓶量液 · 文献调研）

> 本目录为中期报告文献调研所下载的论文 PDF。文件名 `主题_简称.pdf`，后附 arXiv 编号与一句话要点。
> 全部来自 arXiv（开源预印本）。如需原始条目，访问 `https://arxiv.org/abs/<编号>`。

## 1. VLA（视觉-语言-动作大模型）

| 文件 | arXiv | 一句话要点 |
| --- | --- | --- |
| `VLA_RT-2.pdf` | 2307.15818 | RT-2：把 VLM 与机器人数据协同微调，把网络知识迁移到动作，端到端「图→动作」 |
| `VLA_OpenVLA.pdf` | 2406.09246 | OpenVLA：开源 7B VLA（Prismatic VLM + Llama-2），Open X-Embodiment 97 万条轨迹训练 |
| `VLA_pi0.pdf` | 2410.24164 | π0（Physical Intelligence）：flow-matching 连续动作 VLA，预训练 + pi0-FAST 后训练，跨 7 种机器人 |

## 2. WAM（世界-动作模型）

| 文件 | arXiv | 一句话要点 |
| --- | --- | --- |
| `WAM_World-Action-Models-Survey.pdf` | 2605.12090 | WAM 首个系统综述：联合预测未来世界状态 + 动作，视频预训练生成式主干，NVIDIA DreamZero 起名 |
| `WAM_DINO-WM.pdf` | 2411.04983 | DINO-WM：在预训练视觉特征上建世界模型，零样本规划（世界模型路线代表作） |
| `WAM_WALL-WM.pdf` | 2606.01955 | WALL-WM：自变量（XSquare）自家世界模型，与 wall-x 生态配套 |

## 3. Agent 路线（LLM/VLM 智能体）

| 文件 | arXiv | 一句话要点 |
| --- | --- | --- |
| `Agent_SayCan.pdf` | 2204.01691 | SayCan：LLM 高层规划 + 可负担性（affordance/value）接地，「Do As I Can, Not As I Say」 |
| `Agent_VoxPoser.pdf` | 2307.05973 | VoxPoser：LLM 写代码生成 3D 价值图/可负担性图，与 MPC 组合，零样本真机操作 |
| `Agent_Code-as-Policies.pdf` | 2209.07753 | Code-as-Policies：LLM 直接生成可执行代码（ROS），层次化、可组合 |

## 4. 移动双臂操作

| 文件 | arXiv | 一句话要点 |
| --- | --- | --- |
| `MobileDualArm_Mobile-ALOHA.pdf` | 2401.02117 | Mobile ALOHA：低成本全身遥操作 + 模仿学习，移动双臂整机策略 |
| `MobileDualArm_OK-Robot.pdf` | 2401.12202 | OK-Robot：真实家庭里开放词表「取放」（pick-and-drop），移动底盘 + 单臂 |
| `MobileDualArm_Dobb-E.pdf` | 2311.16098 | Dobb·E：iPhone 遥操作采数 + 家庭环境模仿学习 |

## 5. 液体倾倒

| 文件 | arXiv | 一句话要点 |
| --- | --- | --- |
| `Pouring_FluidLab.pdf` | 2303.02346 | FluidLab：可微分流体仿真基准（MLS-MPM），倒液/拉花等流体操纵任务 |
| `Pouring_SelfSupervised-Pouring.pdf` | 2011.10150 | 自监督精准倒液：跨容器泛化，GSSP 微调 |
| `Pouring_PourIt.pdf` | 2307.11299 | PourIt!（ICCV 2023）：弱监督单图液面感知 + 视觉闭环倒液（Franka，10 Hz） |

> 补充综述（未下 PDF，纯参考）：Reyes-Montiel et al., *Techniques Applied to Autonomous Liquid Pouring: A Scoping Review*, Math. Comput. Appl. 31(1):30 (2026), DOI `10.3390/mca31010030`。核心结论：经典控制（PID/PD）占主导（~30%），学习型方法（RL/IL）占比最低（~15%），**精确体积倾倒的闭环视觉伺服仍是研究缺口**。

## 6. wall-x 生态（自变量 / XSquare）

| 文件 | arXiv | 一句话要点 |
| --- | --- | --- |
| `WallX_Wall-OSS.pdf` | 2509.11766 | WALL-OSS：wall-x 的开源 VLA 训练/推理栈（Qwen2.5-VL-3B + MoT 双 FFN，flow-matching/FAST 两种动作分支） |
| `WallX_Wall-OSS-0.5.pdf` | 2605.30877 | Wall-OSS-0.5：4B VLA，20+ 形态预训练，未微调即可零样本部署，17 个真机任务验证 |

- 代码仓库：`https://github.com/X-Square-Robot/wall-x`（Apache-2.0，Python 包 `wall_x`）
- 官方文档：`https://x2robot.com/docs/quantax1pro/v1/model-development/wall-oss/model-introduction`
- 三条开发路径：① 直接验证预训练模型；② 用自有 LeRobot 数据微调；③ 适配第三方模型（文档以 π0.5 为例）
- 覆盖链路：数据采集/遥操作 → VLA 后训练微调（FSDP）→ 真机部署 → SDK（控制/感知/导航）→ 建图导航 → 仿真（LIBERO）
