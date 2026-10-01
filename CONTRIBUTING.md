# 贡献

围绕一个技能或一项改进提交小范围变更。

## 编写技能

- 在 `skills/<name>/SKILL.md` 维护唯一版本，frontmatter 提供 `name` 和 `description`。
- `description` 写清用途和触发条件。`metadata.kind` 使用 `knowledge`、`method` 或 `operation`，供目录分类。
- 参考资料、脚本与素材放在本技能目录，按需要读取；单独安装后仍可使用。
- 公共规范引用权威来源；账号、凭据、仓库、镜像和环境信息由调用者提供。
- 实验变体、运行日志和逐轮结果保存在仓库外。

## 检查

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python tools/catalog.py --write
.venv/bin/python tools/validate.py .
.venv/bin/python -m unittest discover -s tests -v
```

将修改后的技能安装到临时项目，实际调用一个相关任务，检查结果、输入缺失时的处理和操作授权边界。可复用 [行为用例](tests/README.md)，也可补充有区分力的新用例。检查结束后清理本次创建的环境。

PR 简述改动和实际验证结果；未执行的检查如实说明。静态检查通过不代表行为验证通过。
