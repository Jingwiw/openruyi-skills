---
name: obs-build-artifacts
description: "Read OBS build status or logs, or download RPMs from a specified build."
metadata:
  kind: operation
---

# OBS 构建观察与产物获取

接收项目、包、repository/architecture 对和预期来源身份；只执行调用者需要的观察、触发或下载操作。身份判断可组合 `obs-artifact-identity`，或使用调用者已经验证的来源清单。

- 查询 `/build/PROJECT/_result`。scheduled、building、依赖 blocked 是等待状态；保留现有 job，使用有期限的等待，不重复触发掩盖原失败。
- 日志接口为 `/build/PROJECT/REPOSITORY/ARCH/PACKAGE/_log`；依据实际错误定位服务、依赖、编译、测试或打包阶段。保存完整末尾及相关上下文。
- 安装验收时通过二进制列表获取 SRPM 和全部子包；只查来源时优先读取已有清单与日志。发布关闭时可使用认证 API。
- 下载后查询实际 NEVRA、架构和 SHA-256，保存对应源码身份、构建日志/buildinfo。预期来源无法确认的文件隔离，不交给验收当作新产物。
- 验证签名需要项目公开 key：读取 `_keyinfo` 并核对指纹，仅导入一次性验证环境。不要以关闭签名检查替代处理 key。
- 触发 rebuild 或 wipe 是另一个写操作，需要明确目标及授权；不因一项失败 wipe 整个项目。

交付构建状态/日志，或产物与来源清单。执行时读 [构建和产物接口](references/api.md)，按需选用日志、buildinfo、下载和签名身份查询。
