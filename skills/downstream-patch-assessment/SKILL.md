---
name: downstream-patch-assessment
description: "Decide whether a downstream patch is still needed or superseded by upstream code or a build option."
metadata:
  kind: method
---

# 下游补丁评估

检查目标发布源码中的实现和测试，不以补丁能否应用判断修复是否存在：能应用可能重复修复，不能应用可能只是上下文变化。

| 发现 | 后续检查 |
| --- | --- |
| 上游已有相似提交 | 比较语义与原问题输入；提交哈希不同不代表修复不同 |
| 其他发行版有补丁 | 对齐版本、架构、构建选项，再复现问题 |
| 上游提供相关配置开关 | 同一源码、工具链、依赖和测试输入下只切换该选项；先验证再决定是否 backport |
| 准备删除补丁 | 同时检查 SPEC 的 Patch 声明、应用位置和原问题回归测试 |

保留补丁时记录上游出处、目标版本差异和许可证来源。逐个给出保留、调整、删除或待确认的结论；缺少复现或语义证据时不能判定已解决。
