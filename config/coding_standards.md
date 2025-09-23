# 团队编码规范

## SEC-001: 禁止硬编码数据库密码
- **类别**: 安全
- **描述**: 数据库连接字符串中不得包含明文密码
- **示例（错误）**: `jdbc:mysql://localhost:3306/db?user=root&password=123456`
- **建议**: 使用环境变量或配置中心加载

## PERF-002: 及时关闭资源
- **类别**: 性能
- **描述**: 打开的文件、数据库连接、网络流必须在 finally 块或 try-with-resources 中关闭
- **示例（错误）**: `InputStream is = new FileInputStream("a.txt");` 无 close()
- **建议**: 使用 try-with-resources 或 finally 块关闭

## LOG-003: 日志禁止打印敏感信息
- **类别**: 安全
- **描述**: 不得在日志中打印密码、身份证、手机号等敏感信息
- **示例（错误）**: `log.info("用户登录: " + user.getPassword());`
- **建议**: 打码或忽略敏感字段