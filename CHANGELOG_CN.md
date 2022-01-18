# 升级日志

## [1.3.0](https://github.com/HXSecurity/DongTai-webapi/releases/tag/v1.3.0)-2021-1-15
* 功能
  * 增加了API自动测试的功能
* 改善
  * 改善了漏洞导出接口的查询速度
  * 改善了部分内容缺少提示的问题
* 修复
  * 修复了正则表达式验证中的re-dos问题
  * 修复了组件导出csv没有正确携带UTF-8 BOM的问题
  * 修复项目信息修改时提示信息不一致的问题
  * 修复了部分内容缺少i18n部分的问题
  * 修复了组件漏洞展示的问题


## [1.2.0](https://github.com/HXSecurity/DongTai-webapi/releases/tag/v1.2.0)-2021-12-18
* 功能
  * 增加了组件的license展示
  * 增加了一组通过id获取概况列表的接口
  * 增加了自定义规则批量处理接口
  * 增加组件导出功能
* 改善
  * 改善了组件概况接口的查询速度
* 修复
  * 修复了修改策略导致漏洞无法检出的bug
  * 修复了/api/v1/sensitive_info_rule/分页数据获取失败的bug
  * 修复正则校验与engine不一致的bug



## [1.1.4](https://github.com/HXSecurity/DongTai-webapi/releases/tag/v1.1.4)-2021-12-18
* 提升
  * 拆分和添加钩子以适应插件开发
* 
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
