---
name: container-validation-boundaries
description: "Determine what Docker or cross-architecture emulation can test and which claims require a target kernel."
metadata:
  kind: knowledge
---

# 容器验证边界

Docker 容器共享宿主内核；跨架构用户空间模拟不提供目标架构内核。

| 实验 | 可验证 | 不能据此验证 |
| --- | --- | --- |
| RPM 安装事务 | 当前仓库、依赖和宏环境中的安装 | 其他部署环境 |
| CLI/API、动态加载、合成输入 | 执行到的用户空间路径 | 真实内核事件、硬件路径 |
| 私有服务的一次请求 | 该操作及其依赖 | 系统服务启动、重启、关机生命周期 |
| netlink、capability 或设备不可用 | 当前环境的覆盖缺口 | 功能通过或产品必然有缺陷 |

缺权限时先区分配置错误和内核能力缺失；`--privileged` 不能补出另一种内核，还可能影响共享宿主。内核路径需要时使用隔离虚拟机；用户只要求 Docker 时保留覆盖缺口。

记录宿主内核、镜像 digest、目标架构及模拟方式；不要用镜像架构代替内核架构。参考 [Docker 多平台说明](https://docs.docker.com/build/building/multi-platform/)。
