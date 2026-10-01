---
name: reproducible-evidence
description: "Determine which inputs, results and reconstruction conditions to preserve for reproduction after cleanup."
metadata:
  kind: method
---

# 事实保留与环境重建

环境是可丢弃的执行工具，记录是复核依据。在环境外保存下一次重建真正需要的信息：源码提交与字节校验值、镜像 digest、包 NEVRA/校验值、仓库与公钥身份、工具版本、fixture、命令、字面输出及退出码。

- 若上游地址可能被覆盖或删除，按许可和保留策略保存必要输入；URL 和哈希只能识别字节，不能保证将来还能下载。
- 不保存密码、token 或完整认证配置。用认证来源类型和公开 key fingerprint 记录身份；公开日志前单独审查敏感内容。
- 资源清单记录本任务容器、进程、overlay 的精确身份、用途与保留期限，供执行者清理。
- 重建若无法获得原版本，应记录替代和环境漂移，不称为逐字节复现。
- 检查点保存最后完成的事件和仍运行的作业身份，使后续执行者能从已知事实恢复。

输出可以很小：输入清单、结果位置、已清理资源、仍运行的任务及理由。如何启动或移除资源交给相应操作能力。
