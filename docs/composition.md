# 按任务组合技能

选择原则：当前缺的是知识、判断，还是动作？调用者已经提供的事实不重新生产。没有对应操作需求就不要加载操作技能。

| 请求 | 最小组合 | 变化 |
| --- | --- | --- |
| OBS 显示成功，为什么拿到旧 RPM？ | obs-artifact-identity | 查远端加 obs-build-artifacts；审阅验证报告再加 validation-claims |
| 为库升级选择消费者测试 | runtime-consumer-selection | 设计对照加 controlled-comparison；判断 Docker 覆盖加 container-validation-boundaries；执行再加 docker-disposable-experiment |
| 只检查 SPEC 文件归属 | rpm-install-semantics | openRuyi 合规审阅再加 openruyi-packaging-policy |
| 判断旧补丁能否删除 | downstream-patch-assessment | 需要实验时加 controlled-comparison；不自动 backport |
| 清理实验环境但保留可回溯性 | reproducible-evidence + docker-disposable-experiment | 不重跑已完成测试，不保留无用快照 |
| 拆分提交但不要 commit | change-boundaries | 执行时加 git-change-series；风格按项目补充 |
| 只润色 PR | openruyi-contribution-style | 发布更新时加 github-contribution-operations；不重新打包 |
| 报告基础设施故障 | validation-claims + github-contribution-operations | issue 不要求先有源码修改或 PR |

## 知识归属

- 发行版规范：openruyi-packaging-policy；RPM 通用语义：rpm-install-semantics。
- OBS 来源对应关系：obs-artifact-identity；远端读写动作：两个 OBS operation skills。
- 环境能证明什么：container-validation-boundaries；如何解释检查结果：validation-claims。
- 留下什么以便重建：reproducible-evidence；如何操作容器：docker-disposable-experiment。
- 文案风格：openruyi-contribution-style；操作 GitHub：github-contribution-operations。

不存在机器自动解析的 skill 依赖图，也不要求遍历这些组合。可选名称用于发现；另一项 skill 未安装时，当前技能仍应提供其自身价值，需要外部事实则指出缺什么。

同一输入事实可被多个技能消费：候选 SHA、产物清单、测试记录、授权范围。按实际需要传递，不为了组合引入统一巨大 schema。
