---
name: container-validation-boundaries
description: "Determine what Docker or cross-architecture emulation can test and which claims require a target kernel."
metadata:
  kind: knowledge
---

# 容器验证边界

Docker 隔离文件系统和进程视图，但不是一台自带目标内核的完整机器。外架构 OCI 用户空间在模拟器下运行，不等于使用了该架构的内核。

| 观察 | 能支持的结论 | 不能直接支持的结论 |
| --- | --- | --- |
| RPM 安装、文件清单和依赖事务 | 该环境的安装行为 | 所有部署环境均可安装 |
| CLI/API、动态加载、合成输入 | 实际执行的用户空间路径 | 真实内核事件或硬件路径 |
| 私有服务完成一次请求 | 该服务的所测操作 | 系统级服务生命周期全部正确 |
| 缺 netlink、capability 或设备 | 当前环境无法覆盖该路径 | 功能通过，或必然是产品缺陷 |

先看日志，缺权限不能自动归因；区分配置错误与环境确实不具备能力。额外权限需要具体理由和授权，实验保持共享宿主的系统级安全规则不变。

内核行为确需覆盖时提出隔离的完整虚拟机方案；在用户选定的环境范围内记录覆盖缺口。写明 host/kernel/image/architecture/emulation 实际事实；Docker 后端由环境提供。

参考 [Docker 多平台说明](https://docs.docker.com/build/building/multi-platform/)。
