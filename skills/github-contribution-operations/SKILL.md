---
name: github-contribution-operations
description: "Find, create or update a specified GitHub issue or PR and read it back to confirm the result."
metadata:
  kind: operation
---

# GitHub issue / PR 操作

绑定目标仓库、issue/PR 编号，或 head 仓库/分支与 base 仓库/分支。明确个人 fork 的 branch→main 审阅和向上游投稿的区别；不要根据默认 remote 猜目标。

- 查找已有 issue/PR，避免重复发布。读取当前模板和适用规范；需要风格时组合项目文案技能，而不是在这里再定义一套表达规则。
- issue 适合可复现未解问题或需要决定的事项；不要为填 PR 的 Related Issue 临时制造无意义 issue。
- PR 使用明确的 head/base，先检查差异和授权范围。用 body-file 或结构化 API 传递文本，避免 shell 展开破坏内容。
- 更新前读回最新正文/评论，保留人类刚做的变更；编辑后再次读取并比较预期字段。更新 PR 文案不等于改源码或启动 CI 排障。
- 评论删除、分支推送、关闭 issue、合并 PR 各有独立影响；只做本次请求覆盖的动作。不将一般审阅授权扩展为 merge。
- 不代替用户确认其已阅读行为准则，也不编造身份和测试结果。故障后先读取远端确认是否已完成，避免重复创建。

交付链接和实际更新字段；只要求草稿时返回文字，不产生远端写操作。参考 [GitHub CLI](https://cli.github.com/manual/gh_pr) 和 [GitHub REST API](https://docs.github.com/en/rest)。
