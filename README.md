# openRuyi skills

面向 openRuyi 开发的技能库，提供打包知识、实验方法和贡献工具，按任务自由组合。

由个人维护，面向 openRuyi 社区贡献。打包和贡献要求以项目当前文档为准。

## 使用

选择与问题相关的 `skills/<name>/`，交给支持 Agent Skills 的客户端加载，或复制到该客户端文档指定的技能目录。每个目录包含自己的 `SKILL.md` 和所需参考资料；可单独携带，不依赖本仓库根目录。客户端的发现和安装机制不同，本仓库不假定 `skills/` 会自动生效。

分析问题时选用相关知识和方法，执行任务时加入操作技能。远端写入按用户授权范围进行。

例：`runtime-consumer-selection` + `container-validation-boundaries` 用来设计用例；加上 `docker-disposable-experiment` 才执行。更多例子见 [组合方式](docs/composition.md)。

## 技能目录

<!-- catalog:start -->
| Skill | 类型 | 用途 |
| --- | --- | --- |
| [change-boundaries](skills/change-boundaries/SKILL.md) | 判断方法 | Split diffs by intent and dependency and recommend reviewable commit boundaries. |
| [container-validation-boundaries](skills/container-validation-boundaries/SKILL.md) | 知识 | Determine what Docker or cross-architecture emulation can test and which claims require a target kernel. |
| [controlled-comparison](skills/controlled-comparison/SKILL.md) | 判断方法 | Design controlled comparisons for upgrades, options or fixes using matched inputs and controlled variables. |
| [docker-disposable-experiment](skills/docker-disposable-experiment/SKILL.md) | 操作 | Run a specified Docker experiment, save output and exit status, and clean up owned containers. |
| [downstream-patch-assessment](skills/downstream-patch-assessment/SKILL.md) | 判断方法 | Decide whether a downstream patch is still needed or superseded by upstream code or a build option. |
| [git-change-series](skills/git-change-series/SKILL.md) | 操作 | Stage, commit, amend or safely push Git changes using confirmed commit boundaries. |
| [github-contribution-operations](skills/github-contribution-operations/SKILL.md) | 操作 | Find, create or update a specified GitHub issue or PR and read it back to confirm the result. |
| [obs-artifact-identity](skills/obs-artifact-identity/SKILL.md) | 知识 | Determine whether OBS RPMs came from a given commit; identify stale artifacts and source drift. |
| [obs-build-artifacts](skills/obs-build-artifacts/SKILL.md) | 操作 | Read OBS build status or logs, or download RPMs from a specified build. |
| [obs-source-configuration](skills/obs-source-configuration/SKILL.md) | 操作 | Branch an OBS package in a specified project and configure its Git source and exact revision. |
| [openruyi-contribution-style](skills/openruyi-contribution-style/SKILL.md) | 知识 | Draft or shorten commit, issue and PR text using openRuyi history and templates. |
| [openruyi-packaging-policy](skills/openruyi-packaging-policy/SKILL.md) | 知识 | Find current openRuyi rules and sources for a specific SPEC change. |
| [reproducible-evidence](skills/reproducible-evidence/SKILL.md) | 判断方法 | Determine which inputs, results and reconstruction conditions to preserve for reproduction after cleanup. |
| [rpm-install-semantics](skills/rpm-install-semantics/SKILL.md) | 知识 | Diagnose mismatches between RPM path macros, installed files and subpackage ownership. |
| [runtime-consumer-selection](skills/runtime-consumer-selection/SKILL.md) | 判断方法 | Choose real consumers, meaningful operations and rejection cases for a library upgrade. |
| [validation-claims](skills/validation-claims/SKILL.md) | 判断方法 | Review test claims and distinguish passed, failed, unavailable and untested coverage. |
<!-- catalog:end -->

## 维护

`skills/` 是唯一可编辑技能源；目录表由 frontmatter 生成，不另外维护一套描述。`metadata.kind` 仅供浏览分类，不是运行时依赖或调用顺序。

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python tools/catalog.py --write
.venv/bin/python tools/validate.py .
.venv/bin/python -m unittest discover -s tests -v
```

校验覆盖格式、本地引用、单技能可携带性与执行脚本。冷启动任务评测的方法、评分顺序和研究来源见 [技能评测](docs/skill-evaluation.md)，实际用量与结论见 [首轮结果](docs/evaluation-results.md)。`tests/evals/` 保存中英文描述对照和具体任务，`tests/scenarios.json` 补充其他使用场景。

目录选择及开源参考见 [仓库布局](docs/repository-layout.md)。原初始化提交的内容保留在 `legacy/`，旧 `SKILL.md` 改名为 `SKILL.md.txt`，避免作为活跃技能被递归发现。历史导出脚本不再是本仓库维护入口，不运行它来覆盖人工维护内容。

原仓库没有明确的开源许可证，本次不替作者选择授权条款。公开可读不等于获得再分发许可；对外正式发行前需由所有者确认许可证。

本次技能重组与校验工具由 Codex 协助编写，供维护者审阅。验证包括结构检查、脚本测试和 18 次冷启动任务；具体覆盖范围见评测记录。
