---
name: docker-disposable-experiment
description: "Run a specified Docker experiment, save output and exit status, and clean up owned containers."
metadata:
  kind: operation
---

# 一次性 Docker 实验

输入为镜像 digest、目标架构、实验命令/fixture、需要安装的产物和环境外的结果目录。只有明确需要时才创建环境；已有匹配且属于本任务的容器可以复用。检查可用能力，不假设某种宿主 OS 或 Docker backend。

单命令实验可使用 [执行脚本](scripts/run.py)：`python3 scripts/run.py --image IMAGE@sha256:DIGEST --platform PLATFORM --input INPUT_DIR --output NEW_RESULT_DIR -- /bin/sh /input/test.sh`。镜像须已存在；脚本默认断网，输入只读，保存原始 stdout/stderr、容器退出状态及清理结果。需要联网时显式设置 `--network`。不覆盖已有结果目录。

## 执行约束

- 创建唯一名称，记录实际 container ID；源输入只读挂载、结果单独可写。不要挂载宿主 Docker socket 或整个用户目录。
- 在创建成功后立即建立退出/异常清理路径。即使测试失败也先导出已获得的输出，再删除精确 ID；清理失败要报告，不能宣称无残留。
- 按输入选择网络需求和权限，默认不 privileged。binfmt 注册、宿主配置更改和额外 capability 不是隐含授权。
- 若测试 RPM，安装指定本地文件并查询最终 NEVRA；依赖求解装上的同名发行版包不一定是候选。保持签名检查，用核实过的项目公开 key 解决信任问题。
- 每条实验记录 stdout、stderr、exit；包升级/回滚后确认身份。保留环境、工具和消费者版本。业务预期来自用例，不由执行器将非零输出改为通过。
- 长作业保留 job/进程身份和中间记录；包装器超时后先检查内部命令，避免重复工作。
- 完成后移除本任务容器、临时凭据和自有临时文件，查询精确资源不存在。不用 system prune，不删除共享镜像、volume 或无关容器，不为回溯创建一堆快照。

输出结果目录和实际清理状态。重建资料可组合 `reproducible-evidence`；结论边界可组合 `container-validation-boundaries`。这些不是自动加载的前置任务。

参考 [Docker run](https://docs.docker.com/reference/cli/docker/container/run/) 和 [Docker rm](https://docs.docker.com/reference/cli/docker/container/rm/)。
