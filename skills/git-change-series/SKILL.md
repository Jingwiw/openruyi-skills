---
name: git-change-series
description: "Stage, commit, amend or safely push Git changes using confirmed commit boundaries."
metadata:
  kind: operation
---

# Git 提交序列维护

读取仓库、分支、工作树/暂存区、remote 和当前 head，保护无关工作。接收已确认的修改边界、标题风格、作者和操作授权；缺少时先展示候选，不从“检查 diff”推导提交权限。

- 只暂存目标路径或片段，重新查看 staged diff；检查运行后产生的新修改不能未经检查混入提交。
- 使用仓库实际 subject 和适用 sign-off；不全局修改用户 Git 配置。测试结论绑定被提交的内容。
- 修订未发布提交和改写已发布分支是不同操作。只有明确授权才重写远端主题分支；确认分支不共享且保留旧 tip。
- 重写时使用带预期远端旧 SHA 的 `--force-with-lease=refs/heads/BRANCH:OLD_SHA`；远端漂移则停止，不退回裸 force。
- 仅改 message 也改变 commit SHA。说明树是否相同，不把旧 SHA 的构建记录伪装成新 SHA 的构建。
- 推送后读回远端 ref；失败或网络中断先核对是否已生效，不盲目重复写。

交付提交 SHA、对应边界、远端确认和未执行操作。分组判断可组合 `change-boundaries`，openRuyi 文案可组合 `openruyi-contribution-style`。
