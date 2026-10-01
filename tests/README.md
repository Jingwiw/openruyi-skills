# 测试

```sh
python -m unittest discover -s tests -v
```

- `test_skills.py`：格式、引用、单技能复制与目录一致性。
- `test_docker_runner.py`：执行脚本的成功、失败、超时与清理路径，使用模拟 Docker 响应。
- `scenarios.json`：人工或 agent 行为检查的请求与验收条件。使用独立临时输入，检查实际交付；结果保存在仓库外。

自动检查不调用模型或真实 Docker。行为检查优先验收结果和安全边界，再比较耗时与真实 token 用量；必要的输入确认不计作返工。
