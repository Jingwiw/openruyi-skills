# 独立仓库，还是与 SPECS 并列？

## 本轮决定

先在现有个人 `openruyi-skills` 仓库维护。保留已有提交，不创建同名新仓库，不直接修改 openRuyi main 或组织设置。活跃内容只在 `skills/<name>/`；保持可整目录迁移。

| 选择 | 适合 | 代价 |
| --- | --- | --- |
| 独立 skills 仓库 | 跨包、跨仓库复用，独立审阅和发布节奏 | 需要说明安装入口；项目规范变化要跟进 |
| openRuyi 根目录 `skills/`，与 `SPECS/` 并列 | 高度绑定该仓库的知识，规范和技能需要原子更新 | 增加主仓库职责；非本仓库消费者要获取局部目录 |

目前的技能包含通用 RPM、Git、Docker、实验方法，不只服务 SPECS，因此独立库更自然。是否迁入组织由维护者决定，不因为写了技能就替组织建立仓库。

迁移时只保留一个可编辑源：把选定技能目录迁入目标 `skills/`，移交相应校验和维护说明。不要两边各维护一份，也暂不引入 submodule、双向同步或依赖解析器。

`skills/` 目录是组织方式，不代表所有客户端都自动发现；客户端入口可在明确使用场景后增加适配，不能把某客户端的私有路径当作内容格式。

## 参考观察（2026-10-01）

- [Agent Skills 格式](https://agentskills.io/specification)：标准入口是 YAML frontmatter 的 SKILL.md，内容与参考资料渐进加载。采用格式，不额外强制闭环。
- [Anthropic skills](https://github.com/anthropics/skills)：单技能目录、自带资源，插件清单只是分发组合。借鉴内容与分发分离，不复制其技能文本或授权条款。
- [Sentry skills](https://github.com/getsentry/skills)：统一 skills 源目录；按作用范围区分技能库和项目内技能。借鉴单一维护源，不照搬额外 SPEC 文件和内部流程。
- [HashiCorp agent-skills](https://github.com/hashicorp/agent-skills)：同一组技能支持单项使用与产品组合。借鉴可组合分发，不为当前一个领域预建多层产品插件结构。

这些是活跃项目的管理实践，不是它们认可本仓库的设计，也不是已经验证本仓库在所有客户端兼容。

## 原导出内容

初始化提交 `abfc584a9e9d49cf4f5d2bdaccad9b3a7e6dd089` 是本次基线。旧技能、参考、脚本和清单位于 `legacy/`，内容保留，入口后缀调整以退出发现。Rust/backlog 等未在这次 audit 中验证的旧技能不冒充新体系已完成的能力。旧 exporter 不再运行，避免引入本机来源作为第二个真相源。
