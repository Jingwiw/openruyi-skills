---
name: runtime-consumer-selection
description: "Choose real consumers, meaningful operations and rejection cases for a library upgrade."
metadata:
  kind: method
---

# 库升级的消费者测试

反向包依赖只是候选列表。通过 ELF 动态依赖、符号及实际调用路径确认消费者会到达变更代码；不在宿主执行不可信二进制探测。

| 消费者 | 有意义的操作 | 常见误判 |
| --- | --- | --- |
| PAM 调用程序 | 实际会话及失败路径 | root 切换用户通常不能证明密码认证 |
| 消息总线 | 私有实例的一次请求与拒绝请求 | broker 的 `--version` 不是服务测试 |
| 解析库 | 代表性有效输入和畸形输入 | 仅链接成功不能证明解析行为 |

固定消费者版本、配置和 fixture，仅替换旧库/候选库。确认实际加载的库身份，避免系统副本掩盖候选问题；服务用就绪条件而非固定 sleep 同步。

用私有实例和临时数据，不改系统服务；列出消费者、调用关系、具体输入、预期及未覆盖路径。Docker 覆盖判断可使用 `container-validation-boundaries`。
