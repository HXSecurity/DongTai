from collections import defaultdict

bc = defaultdict(
    lambda: "",
    {
        "CWE-843": "使用不兼容类型访问资源(类型混淆)",
        "CWE-710": "编程规范违背",
        "CWE-489": "遗留的调试代码",
        "CWE-334": "随机数的空间太小",
        "CWE-401": "在移除最后引用时对内存的释放不恰当(内存泄露)",
        "CWE-212": "敏感数据的不恰当跨边界移除",
        "CWE-1285": "Improper Validation of Specified Index, Position, or Offset in Input",
        "CWE-502": "不可信数据的反序列化",
        "CWE-193": "Off-by-one错误",
        "CWE-789": "未经控制的内存分配",
        "CWE-114": "流程控制",
        "CWE-697": "不充分的比较",
        "CWE-250": "带着不必要的权限执行",
        "CWE-348": "使用不可信的源",
        "CWE-183": "宽松定义的白名单",
        "CWE-428": "未经引用的搜索路径或元素",
        "CWE-754": "对因果或异常条件的不恰当检查",
        "CWE-342": "从先前值可预测准确值",
        "CWE-172": "编码错误",
        "CWE-786": "在缓冲区起始位置之前访问内存",
        "CWE-862": "授权机制缺失",
        "CWE-330": "使用不充分的随机数",
        "CWE-184": "不完整的黑名单",
        "CWE-444": "HTTP请求的解释不一致性(HTTP请求私运)",
        "CWE-799": "交互频率的控制不恰当",
        "CWE-130": "长度参数不一致性处理不恰当",
        "CWE-317": "在GUI中的明文存储",
        "CWE-917": "表达式语言语句中使用的特殊元素转义处理不恰当(表达式语言注入)",
        "CWE-426": "不可信的搜索路径",
        "CWE-98": "PHP程序中Include/Require语句包含文件控制不恰当(PHP远程文件包含)",
        "CWE-200": "信息暴露",
        "CWE-346": "源验证错误",
        "CWE-214": "通过处理环境导致的信息暴露",
        "CWE-271": "特权放弃/降低错误",
        "CWE-838": "输出上下文语义编码不恰当",
        "CWE-118": "对可索引资源的访问不恰当(越界错误)",
        "CWE-276": "缺省权限不正确",
        "CWE-829": "从非可信控制范围包含功能例程",
        "CWE-189": "数值错误",
        "CWE-681": "数值类型间的不正确转换",
        "CWE-326": "不充分的加密强度",
        "CWE-202": "通过数据查询的敏感数据暴露",
        "CWE-252": "未加检查的返回值",
        "CWE-617": "可达断言",
        "CWE-354": "完整性检查值验证不恰当",
        "CWE-270": "特权上下文切换错误",
        "CWE-674": "未经控制的递归",
        "CWE-611": "XML外部实体引用的不恰当限制(XXE)",
        "CWE-915": "动态确定对象属性修改的控制不恰当",
        "CWE-280": "不充分权限或特权的处理不恰当",
        "NVD-CWE-Other": "",
        "CWE-194": "未预期的符号扩展",
        "CWE-552": "对外部实体的文件或目录可访问",
        "CWE-760": "使用可预测Salt的单向哈希算法",
        "CWE-694": "使用多个具有重复标识的资源",
        "CWE-77": "在命令中使用的特殊元素转义处理不恰当(命令注入)",
        "CWE-1021": "不当限制渲染UI层或帧",
        "CWE-311": "敏感数据加密缺失",
        "CWE-170": "不恰当的空终结符",
        "CWE-598": "通过GET请求中的查询字符串导致的信息暴露",
        "CWE-653": "不充分的划分",
        "CWE-441": "未有动机的代理或中间人(混淆代理)",
        "CWE-20": "输入验证不恰当",
        "CWE-601": "指向未可信站点的URL重定向(开放重定向)",
        "CWE-203": "通过差异性导致的信息暴露",
        "CWE-1284": "Improper Validation of Specified Quantity in Input",
        "CWE-61": "UNIX符号链接跟随",
        "CWE-822": "非可信指针解引用",
        "CWE-620": "未经验证的口令修改",
        "CWE-268": "特权链锁",
        "CWE-1188": "不安全的默认资源初始化",
        "CWE-242": "使用内在危险函数",
        "CWE-112": "XML验证缺失",
        "CWE-299": "证书撤销验证不恰当",
        "CWE-113": "HTTP头部中CRLF序列转义处理不恰当(HTTP响应分割)",
        "CWE-79": "在Web页面生成时对输入的转义处理不恰当(跨站脚本)",
        "CWE-345": "对数据真实性的验证不充分",
        "CWE-191": "整数下溢(超界折返)",
        "CWE-1278": "Missing Protection Against Hardware Reverse Engineering Using Integrated Circuit (IC) Imaging Techniques",
        "CWE-349": "在可信数据中接受外来的不可信数据",
        "CWE-435": "交互错误",
        "CWE-119": "内存缓冲区边界内操作的限制不恰当",
        "CWE-1333": "Inefficient Regular Expression Complexity",
        "CWE-369": "除零错误",
        "CWE-26": "路径遍历:'dir/../filename'",
        "CWE-353": "缺失完整性检查支持",
        "CWE-470": "使用外部可控制的输入来选择类或代码(不安全的反射)",
        "CWE-404": "不恰当的资源关闭或释放",
        "CWE-696": "不正确的行为次序",
        "CWE-197": "数值截断错误",
        "CWE-774": "不加限制或调节进行文件描述符或句柄的分配",
        "CWE-125": "跨界内存读",
        "CWE-693": "保护机制失效",
        "CWE-277": "不安全的继承权限",
        "CWE-909": "资源初始化缺失",
        "CWE-923": "通信信道对预期端点的不适当限制",
        "CWE-539": "通过持久性Cookie导致的信息暴露",
        "CWE-590": "释放并不在堆上的内存",
        "CWE-208": "通过时间差异性导致的信息暴露",
        "CWE-302": "使用假设不可变数据进行的认证绕过",
        "CWE-532": "通过日志文件的信息暴露",
        "CWE-335": "PRNG种子错误",
        "CWE-340": "可预测问题",
        "CWE-185": "不正确的正则表达式",
        "CWE-332": "PRNG中信息熵不充分",
        "CWE-94": "对生成代码的控制不恰当(代码注入)",
        "CWE-347": "密码学签名的验证不恰当",
        "CWE-772": "对已超过有效生命周期的资源丧失索引",
        "CWE-834": "过度迭代",
        "CWE-610": "资源在另一范围的外部可控制索引",
        "CWE-924": "通信信道中传输过程中消息完整性的不正确执行",
        "CWE-1187": "使用未初始化的资源",
        "CWE-305": "使用基本弱点进行的认证绕过",
        "CWE-327": "使用已被攻破或存在风险的密码学算法",
        "CWE-613": "不充分的会话过期机制",
        "CWE-665": "初始化不恰当",
        "CWE-331": "信息熵不充分",
        "CWE-204": "响应差异性信息暴露",
        "CWE-126": "缓冲区上溢读取",
        "CWE-1286": "Improper Validation of Syntactic Correctness of Input",
        "CWE-755": "对异常条件的处理不恰当",
        "CWE-641": "文件和其他资源名称限制不恰当",
        "CWE-96": "静态存储代码中指令转义处理不恰当(静态代码注入)",
        "CWE-297": "对宿主不匹配的证书验证不恰当",
        "CWE-35": "路径遍历:'.../...//'",
        "CWE-313": "在文件或磁盘上的明文存储",
        "CWE-778": "不充分的日志记录",
        "CWE-798": "使用硬编码的凭证",
        "CWE-88": "参数注入或修改",
        "CWE-59": "在文件访问前对链接解析不恰当(链接跟随)",
        "CWE-667": "加锁机制不恰当",
        "CWE-75": "特殊命令到另一不同平面时的净化处理不恰当(特殊命令注入)",
        "CWE-328": "可逆的单向哈希",
        "CWE-823": "使用越界的指针偏移",
        "CWE-241": "非预期数据类型处理不恰当",
        "CWE-640": "忘记口令恢复机制弱",
        "CWE-91": "XML注入(XPath盲注)",
        "CWE-283": "未经验证的属主",
        "CWE-201": "通过发送数据的信息暴露",
        "CWE-115": "输入的错误解释",
        "CWE-920": "功耗限制不当",
        "CWE-190": "整数溢出或超界折返",
        "CWE-248": "未捕获的异常",
        "CWE-507": "特洛伊木马",
        "CWE-89": "SQL命令中使用的特殊元素转义处理不恰当(SQL注入)",
        "CWE-73": "文件名或路径的外部可控制",
        "CWE-358": "不恰当实现的标准安全检查",
        "CWE-93": "对CRLF序列的转义处理不恰当(CRLF注入)",
        "CWE-99": "对资源描述符的控制不恰当(资源注入)",
        "CWE-565": "在信任Cookie未进行验证与完整性检查",
        "CWE-943": "数据查询逻辑中特殊元素的不当中和",
        "CWE-87": "替代XSS语法转义处理不恰当",
        "CWE-379": "在具有不安全权限的目录中创建临时文件",
        "CWE-471": "对假设不可变数据的修改(MAID)",
        "CWE-706": "使用不正确的解析名称或索引",
        "CWE-290": "使用欺骗进行的认证绕过",
        "CWE-362": "使用共享资源的并发执行不恰当同步问题(竞争条件)",
        "CWE-400": "未加控制的资源消耗(资源穷尽)",
        "CWE-359": "侵犯隐私",
        "CWE-788": "在缓冲区结束位置之后访问内存",
        "CWE-15": "系统设置或配置在外部可控制",
        "CWE-24": "路径遍历:'../filedir'",
        "CWE-295": "证书验证不恰当",
        "CWE-662": "不恰当的同步机制",
        "CWE-267": "特权定义了不安全动作",
        "CWE-364": "信号处理例程中的竞争条件",
        "CWE-228": "语法无效结构处理不恰当",
        "CWE-824": "使用未经初始化的指针",
        "CWE-776": "DTD中递归实体索引的不恰当限制(XML实体扩展)",
        "CWE-688": "使用不正确变量或索引作为参数的函数调用",
        "CWE-912": "隐藏功能",
        "CWE-1336": "Improper Neutralization of Special Elements Used in a Template Engine",
        "CWE-922": "敏感信息的不安全存储",
        "CWE-916": "使用具有不充分计算复杂性的口令哈希",
        "CWE-257": "以可恢复格式存储口令",
        "CWE-506": "内嵌的恶意代码",
        "CWE-451": "关键信息的UI错误表达",
        "CWE-134": "使用外部控制的格式字符串",
        "CWE-704": "不正确的类型转换",
        "CWE-1236": "Improper Neutralization of Formula Elements in a CSV File",
        "CWE-664": "在生命周期中对资源的控制不恰当",
        "CWE-391": "未经检查的错误条件",
        "CWE-407": "算法复杂性",
        "CWE-522": "不充分的凭证保护机制",
        "CWE-90": "LDAP查询中使用的特殊元素转义处理不恰当(LDAP注入)",
        "CWE-457": "使用未经初始化的变量",
        "CWE-240": "对不一致结构体元素处理不恰当",
        "CWE-540": "通过源代码导致的信息暴露",
        "CWE-603": "使用客户端的认证机制",
        "CWE-323": "在加密中重用Nonce与密钥对",
        "CWE-216": "容器错误",
        "CWE-23": "相对路径遍历",
        "CWE-497": "将系统数据暴露到未授权控制的范围",
        "CWE-427": "对搜索路径元素未加控制",
        "CWE-259": "使用硬编码的口令",
        "CWE-256": "明文存储口令",
        "CWE-402": "将私有的资源传输到一个新的空间(资源泄露)",
        "CWE-42": "路径等价:'filename.' (尾部点号)",
        "CWE-573": "调用者对规范的不恰当使用",
        "CWE-338": "使用具有密码学弱点缺陷的PRNG",
        "CWE-415": "双重释放",
        "CWE-116": "对输出编码和转义不恰当",
        "CWE-178": "大小写敏感处理不恰当",
        "CWE-80": "Web页面中脚本相关HTML标签转义处理不恰当(基本跨站脚本)",
        "CWE-304": "认证中关键步骤缺失",
        "CWE-300": "通道可被非端点访问(中间人攻击)",
        "CWE-680": "整数溢出导致缓冲区溢出",
        "CWE-476": "空指针解引用",
        "CWE-682": "数值计算不正确",
        "CWE-670": "控制流实现总是不正确",
        "CWE-350": "不恰当地信任反向DNS",
        "CWE-279": "不安全的运行时授予权限",
        "CWE-775": "缺失文件描述符或句柄在有效生命周期之后的释放处理",
        "NVD-CWE-noinfo": "",
        "CWE-307": "过多认证尝试的限制不恰当",
        "CWE-672": "在过期或释放后对资源进行操作",
        "CWE-472": "对假设不可变Web参数的外部可控制",
        "CWE-770": "不加限制或调节的资源分配",
        "CWE-551": "不正确的行为次序:在解析与净化处理之前进行授权",
        "CWE-567": "在多现场上下文中未能对共享数据进行同步访问",
        "CWE-440": "预期行为违背",
        "CWE-129": "对数组索引的验证不恰当",
        "CWE-321": "使用硬编码的密码学密钥",
        "CWE-316": "在内存中的明文存储",
        "CWE-399": "资源管理错误",
        "CWE-707": "对消息或数据结构的处理不恰当",
        "CWE-627": "动态变量执行",
        "CWE-548": "通过目录枚举导致的信息暴露",
        "CWE-121": "栈缓冲区溢出",
        "CWE-294": "使用捕获-重放进行的认证绕过",
        "CWE-757": "在会话协商时选择低安全性的算法(算法降级)",
        "CWE-273": "对于放弃特权的检查不恰当",
        "CWE-763": "对无效指针或索引的释放",
        "CWE-285": "授权机制不恰当",
        "CWE-122": "堆缓冲区溢出",
        "CWE-123": "任意地址可写任意内容条件",
        "CWE-649": "依赖于未经完整性检查的安全相关输入的混淆或加密",
        "CWE-1076": "对预期协议的遵守不足",
        "CWE-416": "释放后使用",
        "CWE-523": "凭证传输未经安全保护",
        "CWE-669": "在范围间的资源转移不正确",
        "CWE-266": "特权授予不正确",
        "CWE-639": "通过用户控制密钥绕过授权机制",
        "CWE-749": "暴露危险的方法或函数",
        "CWE-303": "认证算法的不正确实现",
        "CWE-792": "对一个或多个特殊元素实例的过滤不完全",
        "CWE-209": "通过错误消息导致的信息暴露",
        "CWE-36": "绝对路径遍历",
        "CWE-281": "权限预留不恰当",
        "CWE-494": "下载代码缺少完整性检查",
        "CWE-1004": "没有'HttpOnly'标志的敏感Cookie",
        "CWE-390": "未有动作错误条件的检测",
        "CWE-78": "OS命令中使用的特殊元素转义处理不恰当(OS命令注入)",
        "CWE-918": "服务端请求伪造(SSRF)",
        "CWE-74": "输出中的特殊元素转义处理不恰当(注入)",
        "CWE-807": "在安全决策中依赖未经信任的输入",
        "CWE-599": "缺失对OpenSSL证书的验证",
        "CWE-312": "敏感数据的明文存储",
        "CWE-120": "未进行输入大小检查的缓冲区拷贝(传统缓冲区溢出)",
        "CWE-525": "通过浏览器缓存导致的信息暴露",
        "CWE-124": "缓冲区下溢",
        "CWE-1287": "Improper Validation of Specified Type of Input",
        "CWE-1295": "Debug Messages Revealing Unnecessary Information",
        "CWE-117": "日志输出的转义处理不恰当",
        "CWE-261": "口令使用弱密码学算法",
        "CWE-642": "对关键状态数据的外部可控制",
        "CWE-425": "直接请求(强制性浏览)",
        "CWE-377": "不安全的临时文件",
        "CWE-436": "解释冲突",
        "CWE-527": "将CVS仓库暴露给非授权控制范围",
        "CWE-284": "访问控制不恰当",
        "CWE-22": "对路径名的限制不恰当(路径遍历)",
        "CWE-732": "关键资源的不正确权限授予",
        "CWE-657": "违背安全设计原则",
        "CWE-378": "创建拥有不安全权限的临时文件",
        "CWE-64": "Windows快捷方式跟随(.LNK)",
        "CWE-684": "特定函数功能的不正确供给",
        "CWE-269": "特权管理不恰当",
        "CWE-521": "弱口令要求",
        "CWE-131": "缓冲区大小计算不正确",
        "CWE-325": "缺少必要的密码学步骤",
        "CWE-668": "将资源暴露给错误范围",
        "CWE-790": "特殊元素过滤不恰当",
        "CWE-459": "清理环节不完整",
        "CWE-708": "不正确的属主授予",
        "CWE-434": "危险类型文件的不加限制上传",
        "CWE-1321": "Improperly Controlled Modification of Object Prototype Attributes ('Prototype Pollution')",
        "CWE-538": "文件和路径信息暴露",
        "CWE-352": "跨站请求伪造(CSRF)",
        "CWE-367": "检查时间与使用时间(TOCTOU)的竞争条件",
        "CWE-835": "不可达退出条件的循环(无限循环)",
        "CWE-288": "使用候选路径或通道进行的认证绕过",
        "CWE-759": "使用未加Salt的单向哈希算法",
        "CWE-825": "无效指针解引用",
        "CWE-942": "过度许可的跨域白名单",
        "CWE-287": "认证机制不恰当",
        "CWE-863": "授权机制不正确",
        "CWE-384": "会话固定",
        "CWE-319": "敏感数据的明文传输",
        "CWE-644": "对HTTP头部进行脚本语法转义处理不恰当",
        "CWE-787": "跨界内存写",
        "CWE-306": "关键功能的认证机制缺失",
        "CWE-805": "使用不正确的长度值访问缓冲区",
        "CWE-908": "对未经初始化资源的使用",
        "CWE-405": "不对称的资源消耗(放大攻击)",
        "CWE-913": "动态管理代码资源的控制不恰当",
        "CWE-264": "权限、特权和访问控制",
        "CWE-315": "在Cookie中的明文存储",
        "CWE-233": "参数问题",
        "CWE-385": "隐蔽时间通道",
    },
)


LICENSE_DICT = {
    "GPL-1.0-only": {
        "id": 52,
        "identifier": "GPL-1.0-only",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "GPL-1.0-or-later": {
        "id": 53,
        "identifier": "GPL-1.0-or-later",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "GPL-2.0-only": {
        "id": 54,
        "identifier": "GPL-2.0-only",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "GPL-2.0-or-later": {
        "id": 55,
        "identifier": "GPL-2.0-or-later",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "GPL-3.0-only": {
        "id": 56,
        "identifier": "GPL-3.0-only",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "GPL-3.0-or-later": {
        "id": 57,
        "identifier": "GPL-3.0-or-later",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "GPL-1.0": {
        "id": 58,
        "identifier": "GPL-1.0",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "GPL-1.0+": {
        "id": 59,
        "identifier": "GPL-1.0+",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "GPL-2.0": {
        "id": 60,
        "identifier": "GPL-2.0",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "GPL-2.0+": {
        "id": 61,
        "identifier": "GPL-2.0+",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "GPL-2.0-with-autoconf-exception": {
        "id": 62,
        "identifier": "GPL-2.0-with-autoconf-exception",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "GPL-2.0-with-bison-exception": {
        "id": 63,
        "identifier": "GPL-2.0-with-bison-exception",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "GPL-2.0-with-classpath-exception": {
        "id": 64,
        "identifier": "GPL-2.0-with-classpath-exception",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "GPL-2.0-with-font-exception": {
        "id": 65,
        "identifier": "GPL-2.0-with-font-exception",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "GPL-2.0-with-GCC-exception": {
        "id": 66,
        "identifier": "GPL-2.0-with-GCC-exception",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "GPL-3.0": {
        "id": 67,
        "identifier": "GPL-3.0",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "GPL-3.0+": {
        "id": 68,
        "identifier": "GPL-3.0+",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "GPL-3.0-with-autoconf-exception": {
        "id": 69,
        "identifier": "GPL-3.0-with-autoconf-exception",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "GPL-3.0-with-GCC-exception": {
        "id": 70,
        "identifier": "GPL-3.0-with-GCC-exception",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "AGPL-1.0-only": {
        "id": 71,
        "identifier": "AGPL-1.0-only",
        "level_id": 1,
        "level_desc": "限制性商业闭源集成",
    },
    "AGPL-1.0-or-later": {
        "id": 72,
        "identifier": "AGPL-1.0-or-later",
        "level_id": 1,
        "level_desc": "限制性商业闭源集成",
    },
    "AGPL-3.0-only": {
        "id": 73,
        "identifier": "AGPL-3.0-only",
        "level_id": 1,
        "level_desc": "限制性商业闭源集成",
    },
    "AGPL-3.0-or-later": {
        "id": 74,
        "identifier": "AGPL-3.0-or-later",
        "level_id": 1,
        "level_desc": "限制性商业闭源集成",
    },
    "AGPL-1.0": {
        "id": 75,
        "identifier": "AGPL-1.0",
        "level_id": 1,
        "level_desc": "限制性商业闭源集成",
    },
    "AGPL-3.0": {
        "id": 76,
        "identifier": "AGPL-3.0",
        "level_id": 1,
        "level_desc": "限制性商业闭源集成",
    },
    "LGPL-2.0-only": {
        "id": 77,
        "identifier": "LGPL-2.0-only",
        "level_id": 2,
        "level_desc": "限制性商业闭源集成",
    },
    "LGPL-2.0-or-later": {
        "id": 78,
        "identifier": "LGPL-2.0-or-later",
        "level_id": 2,
        "level_desc": "限制性商业闭源集成",
    },
    "LGPL-2.1-only": {
        "id": 79,
        "identifier": "LGPL-2.1-only",
        "level_id": 2,
        "level_desc": "限制性商业闭源集成",
    },
    "LGPL-2.1-or-later": {
        "id": 80,
        "identifier": "LGPL-2.1-or-later",
        "level_id": 2,
        "level_desc": "限制性商业闭源集成",
    },
    "LGPL-3.0-only": {
        "id": 81,
        "identifier": "LGPL-3.0-only",
        "level_id": 2,
        "level_desc": "限制性商业闭源集成",
    },
    "LGPL-3.0-or-later": {
        "id": 82,
        "identifier": "LGPL-3.0-or-later",
        "level_id": 2,
        "level_desc": "限制性商业闭源集成",
    },
    "LGPLLR": {
        "id": 83,
        "identifier": "LGPLLR",
        "level_id": 2,
        "level_desc": "限制性商业闭源集成",
    },
    "LGPL-2.0": {
        "id": 84,
        "identifier": "LGPL-2.0",
        "level_id": 2,
        "level_desc": "限制性商业闭源集成",
    },
    "LGPL-2.0+": {
        "id": 85,
        "identifier": "LGPL-2.0+",
        "level_id": 2,
        "level_desc": "限制性商业闭源集成",
    },
    "LGPL-2.1": {
        "id": 86,
        "identifier": "LGPL-2.1",
        "level_id": 2,
        "level_desc": "限制性商业闭源集成",
    },
    "LGPL-2.1+": {
        "id": 87,
        "identifier": "LGPL-2.1+",
        "level_id": 2,
        "level_desc": "限制性商业闭源集成",
    },
    "LGPL-3.0": {
        "id": 88,
        "identifier": "LGPL-3.0",
        "level_id": 2,
        "level_desc": "限制性商业闭源集成",
    },
    "LGPL-3.0+": {
        "id": 89,
        "identifier": "LGPL-3.0+",
        "level_id": 2,
        "level_desc": "限制性商业闭源集成",
    },
    "Artistic-1.0": {
        "id": 90,
        "identifier": "Artistic-1.0",
        "level_id": 2,
        "level_desc": "限制性商业闭源集成",
    },
    "Artistic-1.0-cl8": {
        "id": 91,
        "identifier": "Artistic-1.0-cl8",
        "level_id": 2,
        "level_desc": "限制性商业闭源集成",
    },
    "Artistic-1.0-Perl": {
        "id": 92,
        "identifier": "Artistic-1.0-Perl",
        "level_id": 2,
        "level_desc": "限制性商业闭源集成",
    },
    "Artistic-2.0": {
        "id": 93,
        "identifier": "Artistic-2.0",
        "level_id": 2,
        "level_desc": "限制性商业闭源集成",
    },
    "ClArtistic": {
        "id": 94,
        "identifier": "ClArtistic",
        "level_id": 2,
        "level_desc": "限制性商业闭源集成",
    },
    "ISC": {"id": 95, "identifier": "ISC", "level_id": 0, "level_desc": "允许商业集成"},
    "BSD-4-Clause": {
        "id": 96,
        "identifier": "BSD-4-Clause",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "CC-BY-2.5": {
        "id": 97,
        "identifier": "CC-BY-2.5",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "CC-BY-ND-4.0": {
        "id": 98,
        "identifier": "CC-BY-ND-4.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "BSD-2-Clause-Views": {
        "id": 99,
        "identifier": "BSD-2-Clause-Views",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "FTL": {"id": 100, "identifier": "FTL", "level_id": 0, "level_desc": "允许商业集成"},
    "BSD-2-Clause-Patent": {
        "id": 101,
        "identifier": "BSD-2-Clause-Patent",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "MPL-2.0-no-copyleft-exception": {
        "id": 102,
        "identifier": "MPL-2.0-no-copyleft-exception",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "CC-BY-NC-3.0": {
        "id": 103,
        "identifier": "CC-BY-NC-3.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "CC-BY-NC-ND-2.5": {
        "id": 104,
        "identifier": "CC-BY-NC-ND-2.5",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "GFDL-1.3": {
        "id": 105,
        "identifier": "GFDL-1.3",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "libpng-2.0": {
        "id": 106,
        "identifier": "libpng-2.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "AML": {"id": 107, "identifier": "AML", "level_id": 0, "level_desc": "允许商业集成"},
    "MIT": {"id": 108, "identifier": "MIT", "level_id": 0, "level_desc": "允许商业集成"},
    "CC-BY-SA-2.5": {
        "id": 109,
        "identifier": "CC-BY-SA-2.5",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "EPL-2.0": {
        "id": 110,
        "identifier": "EPL-2.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "CC-BY-SA-2.0": {
        "id": 111,
        "identifier": "CC-BY-SA-2.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "Apache-2.0": {
        "id": 112,
        "identifier": "Apache-2.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "MPL-2.0": {
        "id": 113,
        "identifier": "MPL-2.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "BSD-3-Clause-Clear": {
        "id": 114,
        "identifier": "BSD-3-Clause-Clear",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "CC-BY-NC-ND-3.0": {
        "id": 115,
        "identifier": "CC-BY-NC-ND-3.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "CC-BY-NC-ND-4.0": {
        "id": 116,
        "identifier": "CC-BY-NC-ND-4.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "CC-BY-ND-3.0": {
        "id": 117,
        "identifier": "CC-BY-ND-3.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "CC-BY-NC-2.5": {
        "id": 118,
        "identifier": "CC-BY-NC-2.5",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "CC-BY-SA-3.0": {
        "id": 119,
        "identifier": "CC-BY-SA-3.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "ECL-2.0": {
        "id": 120,
        "identifier": "ECL-2.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "CDDL-1.0": {
        "id": 121,
        "identifier": "CDDL-1.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "MPL-1.1": {
        "id": 122,
        "identifier": "MPL-1.1",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "CC0-1.0": {
        "id": 123,
        "identifier": "CC0-1.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "CC-BY-NC-4.0": {
        "id": 124,
        "identifier": "CC-BY-NC-4.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "JSON": {"id": 125, "identifier": "JSON", "level_id": 0, "level_desc": "允许商业集成"},
    "bzip2-1.0.6": {
        "id": 126,
        "identifier": "bzip2-1.0.6",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "Apache-1.1": {
        "id": 127,
        "identifier": "Apache-1.1",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "Beerware": {
        "id": 128,
        "identifier": "Beerware",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "CC-BY-2.0": {
        "id": 129,
        "identifier": "CC-BY-2.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "CC-BY-NC-SA-3.0": {
        "id": 130,
        "identifier": "CC-BY-NC-SA-3.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "FSFAP": {"id": 131, "identifier": "FSFAP", "level_id": 0, "level_desc": "允许商业集成"},
    "CC-BY-3.0": {
        "id": 132,
        "identifier": "CC-BY-3.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "CC-BY-NC-SA-4.0": {
        "id": 133,
        "identifier": "CC-BY-NC-SA-4.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "CC-BY-4.0": {
        "id": 134,
        "identifier": "CC-BY-4.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "EPL-1.0": {
        "id": 135,
        "identifier": "EPL-1.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "UPL-1.0": {
        "id": 136,
        "identifier": "UPL-1.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "Zlib": {"id": 137, "identifier": "Zlib", "level_id": 0, "level_desc": "允许商业集成"},
    "MIT-0": {"id": 138, "identifier": "MIT-0", "level_id": 0, "level_desc": "允许商业集成"},
    "CC-BY-SA-4.0": {
        "id": 139,
        "identifier": "CC-BY-SA-4.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "Unlicense": {
        "id": 140,
        "identifier": "Unlicense",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "HPND-sell-variant": {
        "id": 141,
        "identifier": "HPND-sell-variant",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "BSD-3-Clause": {
        "id": 142,
        "identifier": "BSD-3-Clause",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "BSD-2-Clause": {
        "id": 143,
        "identifier": "BSD-2-Clause",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "libtiff": {
        "id": 144,
        "identifier": "libtiff",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
}

LICENSE_ID_DICT = {v["id"]: k for k, v in LICENSE_DICT.items()}


def get_cwe_name(cwe_id: str) -> str:
    return bc[cwe_id]
