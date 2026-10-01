---
name: openruyi-contribution-style
description: "Draft or shorten commit, issue and PR text using openRuyi history and templates."
metadata:
  kind: knowledge
---

# openRuyi 贡献文案

读取目标仓库当前模板、相关路径提交历史和同类已合并 PR；需要样本时看 [合并示例](references/examples.md)。历史风格不能覆盖当前模板。

- 软件包标题常见 `SPECS: <package>: <action>`；沿用实际历史，不强加 Conventional Commits。标题说清楚时省略正文，保留适用 sign-off。
- PR 写改动及必要原因。升级附发布链接；OBS 按架构附结果链接；Docker 测试列具体操作，不写空泛的 checks passed。
- 保留影响验收的失败和覆盖限制。lint 减少但仍非零不能写成 clean；详细计数和过程日志留在外部记录。
- 模板不编造关联 issue，不代替用户勾选行为准则承诺。按当前 [AI 贡献政策](https://dev.openruyi.cn/community/policy/ai-contribution-policy/) 披露实际可确认的协助工具。
- 个人 fork 的 branch→main 审阅与上游投稿是不同目标，明确 head/base 仓库。起草或润色不隐含发布。
