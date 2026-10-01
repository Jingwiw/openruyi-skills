---
name: runtime-consumer-selection
description: "Choose real consumers, meaningful operations and rejection cases for a library upgrade."
metadata:
  kind: method
---

# 运行时消费者选取

先确定改变的是哪个库、接口或行为，再寻找实际使用它的程序。包名和反向依赖查询只是线索；结合已安装文件、ELF 动态依赖、符号和运行路径确认关系。不在宿主执行不可信二进制来做探测。

优先选一条会到达受影响代码的真实操作：身份切换的一次 PAM 会话、私有消息总线的一次调用、解析器的一份代表性输入。配一个应被拒绝的输入；避免只输出 `--version`。

- 控制消费者版本不变，分别使用旧库和候选库；否则把消费者升级当成库兼容性证据。
- 区分加载冒烟、具体操作、完整服务生命周期；跑版本命令的 broker 不能记为服务测试。
- 选择与声明对应的操作。例如 root 发起的用户切换覆盖会话路径，而密码认证需要实际经过认证的输入。
- 用私有实例和临时数据，避免修改系统服务或全局规则。若只能测低风险子路径，明确边界。

输出消费者、关系证据、具体输入、预期、拒绝输入和未覆盖路径。环境执行可另用 `docker-disposable-experiment`，知识边界可另用 `container-validation-boundaries`。
