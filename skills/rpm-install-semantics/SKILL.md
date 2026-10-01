---
name: rpm-install-semantics
description: "Diagnose mismatches between RPM path macros, installed files and subpackage ownership."
metadata:
  kind: knowledge
---

# RPM 文件归属诊断

按 `SPEC 表达式 → 目标环境宏展开 → BUILDROOT 安装位置 → 子包归属` 核对，四者不能互相替代。

- 在目标 RPM 环境执行 `rpm --eval '%{_bindir} %{_sbindir} %{_libexecdir}'`。merged-usr 下不同宏可能同值，两个 glob 可能重复收录。
- 以安装日志和 BUILDROOT 为准；configure 的 libexecdir 不会重定位所有程序，Autotools 的 sbin_PROGRAMS 与 libexec_PROGRAMS 是不同声明。
- `File not found`：检查上游是否生成、安装阶段是否删除、路径是否改变，再修正 glob 或安装行为。
- `Installed but unpackaged`：确定文件用途和所属子包，不靠删除功能文件或扩大为整个目录消除报错。
- 开发链接、头文件、pkg-config 与运行库分别判断；man 页按接口消费者分包，不能仅凭文件存在决定归属。
- `rpmspec --parse` 只证明当前宏环境可解析，且宏可能执行命令；不在宿主解析不可信 SPEC。

参考 [RPM 文档](https://rpm.org/docs/)。
