# 中期报告（Midterm Report）

CS2971 轮式双臂赛道中期报告，LaTeX 编写，**不超过 4 页**，W10 周四 23:59:59 前提交（占总评 30%）。

要求内容：研究问题、任务目标与评价方式；相关工作；拟采用的模型、算法或系统方案；已完成的工作与初步实验结果；当前困难、后续计划及组内分工。

## 目录结构

```
midterm/
├── README.md           # 本文件：编译方法、分工与协作规则
├── main.tex            # 主文件（preamble + \input 各节），只由 owner 维护
└── sections/           # 每人只改自己负责的 .tex 文件，互不冲突
    ├── 01-intro.tex          # 研究问题、任务目标与评价方式
    ├── 02-related-work.tex   # 相关工作
    ├── 03-approach.tex       # 拟采用的模型/算法/系统方案
    └── 04-progress-plan.tex  # 已完成工作与初步实验、困难、计划与分工
```

## 编译

需要 TeX Live（含 ctex 宏包），用 XeLaTeX 编译：

```bash
cd report/midterm
xelatex main.tex    # 跑两遍，生成引用/页码
```

## 协作规则

- 每人**只编辑自己负责的 section 文件**，不要改动 `main.tex` 与他人的文件；
- `main.tex`、`README.md` 由 owner（sword-k-w）统一维护；
- 改动走个人分支，合入 `main` 须提 PR（见仓库根 [CLAUDE.md](../../CLAUDE.md)）；
- 提交前保证本地编译通过（无 Error，Overfull 警告尽量处理）；
- 总页数 ≤4 页，页数预算：01 ≈0.6 页、02 ≈1 页、03 ≈1 页、04 ≈1 页（含标题余量）。

## 分工

| 章节 | 文件 | 负责人 | 依赖 | 页数预算 |
| --- | --- | --- | --- | --- |
| 研究问题、任务目标与评价方式 | `sections/01-intro.tex` | TBD | 无 | ≈0.6 |
| 相关工作 | `sections/02-related-work.tex` | TBD | 无（与 01 完全并行） | ≈1 |
| 拟采用的模型/算法/系统方案 | `sections/03-approach.tex` | TBD | 轻：末尾引用 02 的调研结论 | ≈1 |
| 已完成工作与初步实验、困难、计划与分工 | `sections/04-progress-plan.tex` | sword-k-w（组长） | 最后写，汇总 01–03 的进展 | ≈1 |
