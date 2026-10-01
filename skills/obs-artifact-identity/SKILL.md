---
name: obs-artifact-identity
description: "Determine whether OBS RPMs came from a given commit; identify stale artifacts and source drift."
metadata:
  kind: knowledge
---

# OBS 源码与产物身份

把下面的信息关联起来，而不是只读绿色状态：

`Git commit → service revision → expanded sources/srcmd5 → repository/architecture build → RPM bytes`

- branch 是可移动引用；service 使用精确提交。提交消息重写也改变 SHA，旧产物不会因此自动获得新身份。
- service 已更新不等于运行完成，运行完成不等于各架构已完成该版本构建。必要时读取展开源码和 obsinfo，对照本地候选字节。
- 新构建失败、排队或刚触发时，二进制 API 可能仍有旧包。NEVRA、来源记录和产生它的构建日志必须对应；只验文件名或版本不足。
- 获取产物前后检查源身份是否改变。若变化则隔离这批结果并重新核对，不把跨构建下载拼成一个清单。
- 保存 Git SHA、项目/包/仓库/架构、srcmd5、日志或构建身份、每个产物 NEVRA 和 SHA-256。缺少关联时写“尚未确认来源”，不猜测。
- `succeeded` 是构建结论；`unpublished` 与验证项目构建成功可同时出现，不能据此判断运行功能。

这是来源判断知识，不要求启动 OBS。操作能力可另选 `obs-build-artifacts`。参考 [OBS 文档](https://openbuildservice.org/help/manuals/obs-user-guide/)。
