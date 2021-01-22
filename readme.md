## IAST Agent Server
> 负责与agent相关的api服务，包括：接收agent注册信息、接收心跳信息、接收错误日志信息、接收组件信息、接收漏洞信息、接收权限变更信息、发送引擎控制命令、发送hook点策略、下载检测引擎；

### 接口
- [x] 下载agent
- [x] 自动化部署脚本下载
- [x] 检测引擎下载
- [x] agent注册接口
- [x] 查询检测引擎更新标志
- [x] 修改检测引擎更新标志
- [x] 加载HOOK策略
- [x] 加载agent配置
- [x] 上传报告
- [ ] 获取重放请求

### 检测相关jar包
- iast-agent.jar
- iast-inject.jar
- 高版本iast-core.jar
- 低版本iast-core.jar : 6d791d60368bf7b1899a6b252c278ac

jar包检测方法，计算jar包的SHA-1/MD5，与标准数据进行对比，检测下载的jar包是否正确

| JAR包名称 | 哈希算法 | 哈希值 |
| --- | ---- | --- |
| iast-agent | MD5 | fb120d4c59e60c0a3b3bc31ed595225f |
| iast-agent | SHA-1 | c6040c9797a9926553960ca9edf1f777142a63ba |
| iast-inject | MD5 | c41164a757400b40e9e10b5a3ca32218 |
| iast-inject | SHA-1 | 58102b2f34e16cc1c7da98421c4872efdbbe0d70 |
| 低版本iast-core | MD5 | ed40fe3ad49397bb8c9700bab4b40596 |
| 低版本iast-core | SHA-1 | b6c9607d608b4623defa50a5bf377bfe3bb1ab95 |
| 高版本iast-core | MD5 | 08d8c5b5d8ce8b93994fdb889d02d197 |
| 高版本iast-core | SHA-1 | b02980a245a633a90a8740d8dc7476e20b2ed123 |
