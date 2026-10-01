---
name: openruyi-packaging-policy
description: "Find current openRuyi rules and sources for a specific SPEC change."
metadata:
  kind: knowledge
---

# openRuyi 打包约定

先围绕本次字段或行为检索 openruyi.cn；站点迁移时确认官方跳转或文档入口，不把旧链接失效当成没有规范。当前入口是 [打包规范](https://dev.openruyi.cn/docs/guide/packaging-guidelines/)。记录采用的页面、查询日期和目标仓库提交。

## 需要补充的判断

- 区分 MUST、SHOULD 和历史惯例；具体领域的补充规范优先于通用规范。示例与正文冲突时指出冲突，不默默将示例提升为规范。
- 根据改动查相关补充文档，不每次把整个站点读一遍。关注声明式 BuildSystem、RemoteAsset、Patch、文件拆包和许可证。
- HTTP(S) 源码资源的 RemoteAsset 要带实际下载字节的 SHA-256；URL 未变而字节变化是待调查事实，不直接接受新校验值。[资源处理说明](https://dev.openruyi.cn/docs/guide/remoteassetify-usage-guide/)
- BuildOption 的阶段名、间距和参数拆行按当前规范处理；不把传统 RPM 的手写阶段机械搬入声明式构建。
- 仓库 hooks 是可执行检查，不是规范全文。检查通过只证明其覆盖范围；自动修复产生的新 diff 仍须检查。

输出只需本次适用的约束和出处；缺少正式约束时明确标为建议。RPM 路径推断另可使用 `rpm-install-semantics`，不是必需依赖。
