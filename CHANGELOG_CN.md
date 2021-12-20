# 升级日志

## [1.1.4](https://github.com/HXSecurity/DongTai-webapi/releases/tag/v1.1.4)-2021-12-18
* 提升
  * 拆分和添加钩子以适应插件开发
* 使固定
  * 修复了container为 None 时的 VulDetail ，NoneType导致的问题
  * 修复了 VulSummary 不适当的 sql 查询导致 API 超时的问题
  * 修复返回时缺失扫描策略名称的的问题
  * 修正/api/v1/vulns 局部变量'result' 赋值前引用的问题
  * 修正 /api/v1/sensitive_info_rule/ 字段 没有范围指示


## [1.1.3](https://github.com/HXSecurity/DongTai-webapi/releases/tag/v1.1.3) - 2021-12-03

* 功能
  * 项目现在根据获取组件和漏洞信息时间排序
  * 增加了扫描模板策略管理
  * 增加漏洞主动验证开关（包括全局与项目级）
* 改进
  * 组件信息现在增加了组件路径
  * 改进了原有的分页逻辑
  * 改进了原有的数据校验以适应边界值
  * 绑定探针时探针名现在优先显示别名
* 修复
  * 修复项目创建时agentid可能导致的错误
  * 修复了项目创建时非原子性错误
  * 修复删除数据时存在的权限错误
