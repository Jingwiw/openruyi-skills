---
name: obs-artifact-identity
description: "Determine whether OBS RPMs came from a given commit; identify stale artifacts and source drift."
metadata:
  kind: knowledge
---

# OBS 产物来源

核对关联链：

`Git SHA → service revision → expanded sources/srcmd5 → repository/architecture build → RPM SHA-256`

- service 更新、取源完成、各架构构建完成是三个不同事件。读展开源码和 obsinfo，核对候选字节；绿色状态本身不标识输入。
- 新构建失败或排队时，二进制 API 可能仍返回旧包。相同文件名、版本乃至 NEVRA 都不能证明来自新提交，必须关联生成它的构建日志及源身份。
- 下载前后核对源身份；发生变化时隔离该批结果，避免拼接不同构建的子包。
- 保存 Git SHA、project/package/repository/architecture、srcmd5、构建日志，以及每个 RPM 的 NEVRA 和 SHA-256。缺链则来源待确认。
- 改提交消息也会改变 SHA；若源码树相同，记录等价依据，保留旧构建的原始身份。
- `succeeded` 只表示构建成功；禁用发布时可能同时出现 `unpublished`，不说明运行时功能。

参考 [OBS 文档](https://openbuildservice.org/help/manuals/obs-user-guide/)。
