---
name: docker-disposable-experiment
description: "Run a specified Docker experiment, save output and exit status, and clean up owned containers."
metadata:
  kind: operation
---

# 一次性 Docker 实验

使用 [执行脚本](scripts/run.py)：

```sh
python3 scripts/run.py --image IMAGE@sha256:DIGEST --platform PLATFORM \
  --input INPUT_DIR --output NEW_RESULT_DIR -- /bin/sh /input/test.sh
```

镜像须已存在。输入挂载到只读 `/input`，可写产物目录为 `/output`；脚本保存 stdout、stderr、退出状态及清理结果。默认断网，联网需显式指定 `--network`；不覆盖已有结果目录。

- 测 RPM 时安装指定文件，再查询最终 NEVRA：依赖求解可能装入同名发行版包。用核实过的项目公钥处理信任，保留签名检查。
- 比较旧包与候选时固定消费者版本、fixture 和配置；升级版本与切换编译选项分别做对照，否则无法归因。
- 在容器外保存镜像 digest、RPM 校验值、命令、输入和结果。URL 加哈希不能保证以后仍能下载；不可再获取的输入需按许可保留。
- 只清理本次创建的精确 container ID；失败也先保存输出。清理失败报告残留 ID，不使用 `system prune`，不删除共享镜像或 volume。
- 脚本不提供 privileged、额外 capability 或 Docker socket 挂载。需要这些能力时另行确认宿主影响和授权。

超时与程序退出码分别记录；非零结果按用例判断，不由执行器改写为成功。Docker 后端由环境提供。参考 [Docker run](https://docs.docker.com/reference/cli/docker/container/run/)。
