---
name: controlled-comparison
description: "Design controlled comparisons for upgrades, options or fixes using matched inputs and controlled variables."
metadata:
  kind: method
---

# 最小变量对照

先写一句可证伪假设：“在固定条件下，改变 X 会使输入 Y 的结果从 A 变为 B。”然后选择能实际观测 B 的命令或 API。

- 固定源码字节、工具链、依赖、测试输入和可影响结果的配置；列出唯一计划改变的因素。
- 同时升级版本并修改选项无法证明选项的因果作用。拆成版本比较和同版本配置比较。
- baseline 与 candidate 使用相同输入和判定规则；增加无效输入的拒绝检查，以及不应改变的消费者或架构作为控制。
- 需要回滚证明时恢复原输入身份，再重复同一命令。源码回滚检查哈希，包回滚检查实际安装身份；不要只验证恢复命令退出成功。
- 复用缓存产物时确认其身份与比较条件相符，区别于重新编译。
- 条件不能固定时指出混杂因素，将结论限定为观察到的相关性。

设计给出假设、固定条件、变量、相同输入和预期；执行后将实际结果与预期比较，并说明混杂因素。
