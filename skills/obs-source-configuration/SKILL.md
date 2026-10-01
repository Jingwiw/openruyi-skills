---
name: obs-source-configuration
description: "Branch an OBS package in a specified project and configure its Git source and exact revision."
metadata:
  kind: operation
---

# OBS 分支与 service

输入：OBS 地址及认证配置、主工程/包、个人验证项目、Git fork、精确 SHA、repository/architecture。使用 `osc` 或 [Source API](references/api.md)，认证信息不进入参数或日志。

1. 读取现有 `_meta`、包目录、`_link`、`_service`；已存在的验证包核对后复用。
2. 在授权的个人项目调用原生 branch，保留主工程关系；独立创建的包不等于 branch。API 参数与检查位置见速查。
3. 验证项目通常启用 build、禁用 publish；repository/architecture 从实例元数据发现。
4. 仅修改 obs_scm 的 fork URL、精确 revision 和包路径提取规则；openRuyi 保留适用的 download_assets 及其他服务。
5. 授权后运行 source service，再读回配置与展开源码。上传成功不代表取源完成，更不代表构建通过。
