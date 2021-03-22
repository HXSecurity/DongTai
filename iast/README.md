### IAST 服务端API接口文档
- API接口列表

#### API接口列表

| API接口 | 功能 | 访问权限 |
| ----  | ----  |  ----  |
| /iast/download/agent | 下载IAST AgentDownload | 火线用户 |
| /iast/token/create | 生成IAST UserToken | 火线用户 |
| /iast/deploy | 获取IAST Agent的部署方案 | 火线用户 |
| /iast/server | 获取服务器列表 | 火线用户 |
| /iast/app | 获取应用该程序列表 | 火线用户 |
| /iast/vul | 获取漏洞列表 | 火线用户 |
| /iast/detail | 获取漏洞详情 | 火线用户 |
| /iast/modify | 修改数据 | 火线用户 |
| /iast/download/core | Agent下载核心依赖包 | IAST UserToken |
| /iast/download/properties | Agent下载配置文件 | IAST UserToken |
| /iast/api/vul | Agent上传漏洞数据 | IAST UserToken |
| /iast/api/heartbeat | Agent上传心跳数据 | IAST UserToken |
| /iast/api/errorlog | Agent上传错误日志 | IAST UserToken |
| /iast/api/asset | Agent上传第三方组件信息 | IAST UserToken |


#### 下载IAST AgentDownload

接口编号：预留

接口描述：下载Agent.jar包

接口协议：GET

接口地址：/iast/download/agent

输入参数：无

输出数据：二进制，jar包

#### 生成IAST UserToken
接口编号：预留

接口描述：获取IAST UserToken，用于配置Agent.jar来下载核心jar包和上报漏洞

接口协议：GET

接口地址：/iast/token/create

输入参数：无

输出参数：

| 参数名 | 参数含义 | 数据类型 | 备注 |
| ----  | ----  |  ----  |  ----  |
| token  | IAST UserToken | Varchar  | IAST的Token，UUID |

输出数据示例：
```json
{
  "token":"xxxx-xxxxxx-xxxxxx-xxxx"
}
```

#### 获取IAST Agent的部署方案

接口编号：预留

接口描述：获取IAST Agent的部署文案

接口协议：GET

接口地址：/iast/deploy

输入参数：

| 参数名 | 参数含义 | 数据类型 | 是否必须 | 备注 |
| ---- | ----  |  ----  | ----  |  ----  |
| os | 操作系统 | varchar | 否 | 默认为linux |
| server | 服务器类型 | varchar  | 否 | 默认为tomcat |

输出数据：

| 参数名 | 参数含义 | 数据类型 | 备注 |
| ----  | ----  |  ----  |  ----  |
| status  | 接口的状态码 | int  | 200-正常，500-请求的数据不存在 |
| msg  | API接口返回的消息 | Varchar  | success、failure |
| desc  | 部署文案内容 | Varchar  | IAST的Token，UUID |

#### 获取服务器列表

接口编号：预留

接口描述：获取IAST UserToken，用于配置Agent.jar来下载核心jar包和上报漏洞

接口协议：GET

接口地址：/iast/server

输入参数：

| 参数名 | 参数含义 | 数据类型 | 是否必须 | 备注 |
| ---- | ----  |  ----  | ----  |  ----  |
| page | 当前页 | int | 否 | 默认为1 |
| page_size | 每页的数量 | int  | 否 | 默认为10 |

输出数据：

| 参数名 | 参数含义 | 数据类型 | 备注 |
| ----  | ----  |  ----  |  ----  |
| token  | IAST UserToken | Varchar  | IAST的Token，UUID |

### 依赖包的安装

#### 在mac下安装M2Crypto包
1.打开终端，切换至使用的python环境
2.安装依赖：
```
brew install openssl
brew install swig
```
3.配置环境变量（临时、永久都行）
```
export LDFLAGS="-L$(brew --prefix openssl)/lib"
export CFLAGS="-I$(brew --prefix openssl)/include"
export SWIG_FEATURES="-cpperraswarn -includeall -I$(brew --prefix openssl)/include"
```
4.安装m2crypto包
`pip install m2crypto`
