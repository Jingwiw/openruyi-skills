# 构建和产物接口

参数为调用者的 OBS_URL、PROJECT、REPOSITORY、ARCH、PACKAGE；路径分量分别 URL 编码。认证沿用 `osc` 配置或权限受限的 netrc。只读调查不触发 rebuild。

| 信息 | GET 路径 | 关注内容 |
| --- | --- | --- |
| 项目构建状态 | `/build/PROJECT/_result` | result 的 repository/arch；包 status code |
| 构建日志 | `/build/PROJECT/REPOSITORY/ARCH/PACKAGE/_log?start=0` | 对应源码/包版本及实际失败阶段 |
| 构建输入 | `/build/PROJECT/REPOSITORY/ARCH/PACKAGE/_buildinfo` | srcmd5、依赖与环境信息 |
| 二进制列表 | `/build/PROJECT/REPOSITORY/ARCH/PACKAGE` | binary 的 filename、size、mtime |
| 下载一个文件 | `/build/PROJECT/REPOSITORY/ARCH/PACKAGE/FILENAME` | 返回的实际字节 |
| 项目签名身份 | `/source/PROJECT/_keyinfo` | keyid、fingerprint、userid |

`_buildinfo` 可能反映当前请求，并不自动证明列表中的旧二进制来自该请求。结合产生它的日志和源身份关联；关联不足时保留未知。

下载时先保存列表，再对 SRPM 和每个二进制 RPM 计算 SHA-256，在具备 RPM 的验证环境运行：

```sh
rpm -qp --qf '%{NAME} %{EPOCHNUM}:%{VERSION}-%{RELEASE}.%{ARCH}\n' PACKAGE.rpm
rpm -K PACKAGE.rpm
```

按需进行完整安装验收时下载全套子包；仅判断来源时优先使用已有完整清单和日志，避免无意义下载。公钥信息和公钥数据格式随接口/实例核对：确认返回的公开 key 与 `_keyinfo` 指纹相符，再导入隔离环境，保留签名检查。

依据：[二进制列表 API](https://github.com/openSUSE/open-build-service/blob/master/src/api/public/apidocs/paths/build_project_name_repository_name_architecture_name_package_name.yaml)、[keyinfo API](https://github.com/openSUSE/open-build-service/blob/master/src/api/public/apidocs/paths/source_project_name_keyinfo.yaml)。
