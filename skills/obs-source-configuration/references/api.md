# Source API 速查

使用调用者提供的 `OBS_URL` 和 `OBS_NETRC_FILE`；临时 netrc 权限设为 0600。下列路径中的 PROJECT/PACKAGE 等分别做 URL 编码，查询参数用 URL 编码函数构造。所有写请求先核对目标和授权；curl 加 `--fail-with-body --silent --show-error`，同时保留 HTTP 状态及响应。

| 操作 | 方法与路径 | 读回 |
| --- | --- | --- |
| 查看项目和源包 | GET `/source/PROJECT/_meta`；GET `/source/PROJECT/PACKAGE` | 原配置、linkinfo、serviceinfo |
| 原生分支 | POST `/source/SOURCE_PROJECT/SOURCE_PACKAGE?cmd=branch&target_project=TARGET_PROJECT&target_package=TARGET_PACKAGE&noservice=1` | status 的 target_project/target_package；目标 `_link` |
| 查看/上传 service | GET/PUT `/source/TARGET_PROJECT/TARGET_PACKAGE/_service` | 上传后 GET 比较参数 |
| 运行服务 | POST `/source/TARGET_PROJECT/TARGET_PACKAGE?cmd=runservice` | 源目录的 serviceinfo，等待终态 |
| 展开源目录 | GET `/source/TARGET_PROJECT/TARGET_PACKAGE?expand=1` | srcmd5、entry 与 link/service 信息 |
| 查看展开文件 | GET `/source/TARGET_PROJECT/TARGET_PACKAGE/FILENAME?expand=1` | SPEC 字节、生成的 obsinfo 中实际 revision |

branch 目标已存在时 inspect/reconcile，避免 `force=1` 覆盖；`noservice=1` 用于先配置再运行服务。继承的构建/发布设置也需读取并按本次目标调整，不能把 branch 当作仅本地操作。

service 编辑示例片段如下。保留现有无关 service 和 param；为插入的字符串做 XML 转义，不用未转义的 shell 字符串拼接用户输入。

```xml
<services>
  <service name="obs_scm" mode="trylocal">
    <param name="scm">git</param>
    <param name="url">FORK_URL</param>
    <param name="revision">FULL_GIT_SHA</param>
    <param name="exclude">*</param>
    <param name="extract">SPECS/PACKAGE/*</param>
  </service>
  <service name="download_assets" mode="trylocal" />
</services>
```

源目录报告服务成功后才关联新构建；上传成功、服务成功与编译成功是三个独立事件。接口适用性以目标实例响应为准。

依据：[OBS branch API 定义](https://github.com/openSUSE/open-build-service/blob/master/src/api/public/apidocs/paths/source_project_name_package_name_cmd_branch.yaml)、[Source Services](https://openbuildservice.org/help/manuals/obs-user-guide/cha-obs-source-services)。
