---
name: openruyi-packaging-policy
description: "Find current openRuyi rules and sources for a specific SPEC change."
metadata:
  kind: knowledge
---

# openRuyi 打包规范入口

按本次 SPEC 字段检索 [打包规范](https://dev.openruyi.cn/docs/guide/packaging-guidelines/)，相关补充规范优先于通用示例；区分 MUST、SHOULD 和历史惯例。

- HTTP(S) 源资源使用 RemoteAsset，并绑定实际下载字节的 SHA-256。URL 未变而字节变化需调查，不能直接接受新校验值。见 [资源处理说明](https://dev.openruyi.cn/docs/guide/remoteassetify-usage-guide/)。
- openRuyi 使用声明式 BuildSystem/BuildOption；按当前规范核对阶段名、间距和参数拆行，不机械移植传统 RPM 手写阶段。
- 按修改涉及的 Patch、文件拆包、许可证查补充规则；无需遍历整个站点。
- hooks 只覆盖部分规则；自动修复后的 diff 仍需检查。规范页面、查询日期和目标仓库提交一起保留，避免把历史格式当作当前要求。
