---
name: rpm-install-semantics
description: "Diagnose mismatches between RPM path macros, installed files and subpackage ownership."
metadata:
  kind: knowledge
---

# RPM 安装语义

区分四种事实：SPEC 中的路径表达式、目标构建环境的宏展开、上游真实安装位置、RPM 最终归属。不能用其中一种替代另一种。

- 在目标 RPM 环境中查询 `%{_bindir}`、`%{_sbindir}`、`%{_libexecdir}` 等实际值。merged-usr 下不同宏可能指向同一路径；两个看似不同的 glob 可能重复收录。
- 从安装日志和 BUILDROOT 清单反推 `%files`；configure 的 libexecdir 不会自动重定位所有程序。Autotools 的 sbin_PROGRAMS 和 libexec_PROGRAMS 是不同安装声明。
- File not found：检查上游是否还生成该文件、安装步骤是否主动删除、路径是否变化，再决定修正 glob 或安装行为。
- Installed but unpackaged：先决定该文件是否应交付、由哪个子包负责；不为消除报错直接删除功能文件或扩大成全目录通配。
- 检查主包/devel 的边界：运行库、开发链接、头文件、pkg-config、man 页各有消费者。文件存在不代表依赖充分，程序启动也不代表 ABI 全部兼容。
- `rpmspec --parse` 只检验所用宏环境中的解析；构建、文件归属和真实安装仍是不同事实。处理不可信 SPEC 时考虑其宏执行能力。

给出“声明 → 展开 → 安装 → 归属”的最短证据链。参考 [RPM 官方文档](https://rpm.org/docs/)；发行版约束由调用者补充。
