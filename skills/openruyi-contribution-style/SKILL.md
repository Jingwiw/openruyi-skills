---
name: openruyi-contribution-style
description: "Draft or shorten commit, issue and PR text using openRuyi history and templates."
metadata:
  kind: knowledge
---

# openRuyi 贡献风格

读取目标仓库当前模板，并抽样同类、实际已合并的 PR；同时查看相关路径的提交历史。个人 fork 审阅和上游投稿的目标不同。历史简洁风格不能覆盖当前模板要求。

- commit 标题遵循仓库实际格式；软件包历史常见 `SPECS: <package>: <action>`。不强行改成 Conventional Commits。
- 标题能说清楚时，不附过程说明；保留适用的 Signed-off-by。不要把“我们如何尝试过”写成提交主体。
- PR 说明改了什么，必要时解释为什么；升级可附上游发布链接。测试只列重要实际操作，OBS 给对应架构的结果链接。Docker-based tests 后接具体行为，不写空泛的 checks passed。
- 模板字段只填真实内容；不编造关联 issue、不照抄空模板、不代替人勾选行为准则承诺。
- 详细证据保留在可追溯记录中，不默认把正文删掉的流水账搬进巨大评论。与验收有关的失败和覆盖限制不能借简洁之名隐去。
- 按当前 [AI 贡献政策](https://dev.openruyi.cn/community/policy/ai-contribution-policy/) 做适用披露，使用实际可确认的工具身份，不复制模板中的模型名。自然措辞不等于隐瞒协助。

需要风格样本时看 [已合并示例](references/examples.md)。给出改后的文字即可；是否发布由调用者决定。
