---
name: obs-build-artifacts
description: "Read OBS build status or logs, or download RPMs from a specified build."
metadata:
  kind: operation
---

# OBS 构建与产物接口

输入：OBS 地址、project/package、repository/architecture、预期来源身份。按需读取 [API 速查](references/api.md)。

- `/build/PROJECT/_result`：scheduled、building、依赖 blocked 为等待状态，重复触发会破坏原失败的观察。
- `/build/PROJECT/REPOSITORY/ARCH/PACKAGE/_log`：保存错误上下文，区分取源、依赖、编译、测试和打包阶段。
- 安装验收下载二进制列表中的 SRPM 和全部子包；禁用发布的项目可走认证 API。查询下载文件的 NEVRA、架构、SHA-256，并关联日志、buildinfo 和源码身份。
- 签名验证使用 `_keyinfo` 中的项目公钥，核对指纹后导入一次性环境；不以禁用签名检查处理信任失败。
- rebuild 和 wipe 是写操作，需指定目标和授权；单包失败不应 wipe 整个项目。

来源判断可使用 `obs-artifact-identity`；已有可信来源清单时直接复用。
