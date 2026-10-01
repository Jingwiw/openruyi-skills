---
name: obs-source-configuration
description: "Branch an OBS package in a specified project and configure its Git source and exact revision."
metadata:
  kind: operation
---

# OBS 分支与 service 配置

接收 OBS 地址、认证来源、主工程/包、调用者验证项目、个人 Git fork、精确 SHA、目标仓库/架构。使用 `osc` 或 OBS HTTP API；从配置读取认证，不把秘密放到参数或日志。

1. 先读取现有项目 `_meta`、包目录、`_link` 和 `_service`。项目/包已存在时核对后复用，不默认重建。
2. 在授权的个人空间使用 OBS 原生 branch 操作，保留与主工程的关系。发现已有独立包时先明确是否需要迁移，不静默覆盖或假称已 fork。
3. 验证项目通常启用 build、禁用 publish；仅修改目标项目所需的配置。仓库和架构从实例实际元数据发现。
4. 修改 obs_scm 的 fork URL、精确 revision 和包路径提取规则；在 openRuyi 中保留适用的 download_assets。保留其他服务和无关设置。
5. 在授权范围内运行 source service，再读回配置与展开源码。失败时保留响应，区分服务配置、取源和权限问题；不无限重试。

交付实际 source 配置和已观察状态，不把“成功上传 service”写成“构建通过”。只需渲染配置时不触发服务。

执行时读 [Source API 速查](references/api.md)，包含 branch 参数、service XML 和展开源码读回位置。需要判断产物对应关系时可组合 `obs-artifact-identity`。
