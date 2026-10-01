# openRuyi skills

用于 openRuyi 打包、OBS 构建验证、Docker 实验和 GitHub 贡献的 Agent Skills。

## 安装

克隆技能仓库，在需要使用技能的项目中安装：

```sh
git clone https://github.com/Jingwiw/openruyi-skills.git

# 安装一个技能
npx skills add ./openruyi-skills --skill obs-artifact-identity

# 安装整组 openRuyi 技能
npx skills add ./openruyi-skills --skill '*'
```

按提示选择客户端，默认安装到当前项目。也可以将单个 `skills/<name>/` 目录复制到客户端的技能目录。安装选项见 [Skills CLI](https://github.com/vercel-labs/skills#options)。

## 使用

直接描述任务，或指定需要的技能，例如：

- “用 obs-artifact-identity 检查这些 RPM 是否对应候选提交。”
- “用 runtime-consumer-selection 和 container-validation-boundaries 设计 Docker 消费者测试。”
- “用 openruyi-contribution-style 精简这份 PR 草稿。”

执行设计好的实验时使用 `docker-disposable-experiment`。

## 技能目录

<!-- catalog:start -->
| Skill | 类型 | 用途 |
| --- | --- | --- |
| [container-validation-boundaries](skills/container-validation-boundaries/SKILL.md) | 知识 | Determine what Docker or cross-architecture emulation can test and which claims require a target kernel. |
| [docker-disposable-experiment](skills/docker-disposable-experiment/SKILL.md) | 操作 | Run a specified Docker experiment, save output and exit status, and clean up owned containers. |
| [downstream-patch-assessment](skills/downstream-patch-assessment/SKILL.md) | 判断方法 | Decide whether a downstream patch is still needed or superseded by upstream code or a build option. |
| [obs-artifact-identity](skills/obs-artifact-identity/SKILL.md) | 知识 | Determine whether OBS RPMs came from a given commit; identify stale artifacts and source drift. |
| [obs-build-artifacts](skills/obs-build-artifacts/SKILL.md) | 操作 | Read OBS build status or logs, or download RPMs from a specified build. |
| [obs-source-configuration](skills/obs-source-configuration/SKILL.md) | 操作 | Branch an OBS package in a specified project and configure its Git source and exact revision. |
| [openruyi-contribution-style](skills/openruyi-contribution-style/SKILL.md) | 知识 | Draft or shorten commit, issue and PR text using openRuyi history and templates. |
| [openruyi-packaging-policy](skills/openruyi-packaging-policy/SKILL.md) | 知识 | Find current openRuyi rules and sources for a specific SPEC change. |
| [rpm-install-semantics](skills/rpm-install-semantics/SKILL.md) | 知识 | Diagnose mismatches between RPM path macros, installed files and subpackage ownership. |
| [runtime-consumer-selection](skills/runtime-consumer-selection/SKILL.md) | 判断方法 | Choose real consumers, meaningful operations and rejection cases for a library upgrade. |
<!-- catalog:end -->

## 贡献

每个技能在 `skills/<name>/` 独立维护，包含 `SKILL.md` 和必要的 `references/`、`scripts/` 或 `assets/`。提交前运行检查，并在实际任务中验证行为和边界，详见 [贡献说明](CONTRIBUTING.md)。

## 许可证

许可证待仓库所有者确认。
