# Vercel MCP 工具选择指南

## 需要保留的工具

### 部署相关（必须保留）
- ✅ `get_deployment` - 获取部署信息
- ✅ `get_deployment_events` - 获取部署事件
- ✅ `get_deployment_logs` - 获取部署日志

### 项目相关（必须保留）
- ✅ `get_project` - 获取项目信息
- ✅ `list_projects` - 列出项目列表（可能需要）

### 域名管理（需要保留）
- ✅ `list_domains` - 列出域名
- ✅ `get_domain` - 获取域名信息
- ✅ `add_domain` - 添加域名
- ✅ `remove_domain` - 删除域名
- ✅ `verify_domain` - 验证域名

### 环境变量管理（需要保留）
- ✅ `list_environment_variables` - 列出环境变量
- ✅ `get_environment_variable` - 获取环境变量
- ✅ `create_environment_variable` - 创建环境变量
- ✅ `update_environment_variable` - 更新环境变量
- ✅ `delete_environment_variable` - 删除环境变量

## 需要禁用的工具类别

### 团队管理工具（禁用）
- ❌ `list_teams` - 列出团队
- ❌ `get_team` - 获取团队信息
- ❌ `create_team` - 创建团队
- ❌ `update_team` - 更新团队
- ❌ `delete_team` - 删除团队
- ❌ `list_team_members` - 列出团队成员
- ❌ `add_team_member` - 添加团队成员
- ❌ `remove_team_member` - 移除团队成员
- ❌ `update_team_member_role` - 更新团队成员角色
- ❌ 其他所有团队相关工具

### 监控和分析工具（禁用）
- ❌ `get_analytics` - 获取分析数据
- ❌ `get_metrics` - 获取指标
- ❌ `get_usage` - 获取使用情况
- ❌ `get_performance` - 获取性能数据
- ❌ `get_logs_analytics` - 获取日志分析
- ❌ `get_web_vitals` - 获取 Web Vitals
- ❌ 其他所有监控和分析相关工具

### 安全设置工具（禁用）
- ❌ `get_security_settings` - 获取安全设置
- ❌ `update_security_settings` - 更新安全设置
- ❌ `get_ssl_certificates` - 获取 SSL 证书
- ❌ `create_ssl_certificate` - 创建 SSL 证书
- ❌ `get_firewall_rules` - 获取防火墙规则
- ❌ `create_firewall_rule` - 创建防火墙规则
- ❌ 其他所有安全相关工具

## 其他可以禁用的工具

### 如果不需要的功能
- ❌ 函数管理（如果不需要）
- ❌ 边缘配置（如果不需要）
- ❌ 集成管理（如果不需要）
- ❌ Webhook 管理（如果不需要）
- ❌ 支付和账单（如果不需要）

## 在 Cursor 中操作步骤

1. **打开 Cursor 设置**
   - 按 `Ctrl + ,` (Windows) 或 `Cmd + ,` (Mac)
   - 或点击菜单 → Settings

2. **找到 MCP 设置**
   - 搜索 "MCP" 或 "Model Context Protocol"
   - 找到 `vercel` 服务器

3. **展开 vercel 服务器**
   - 点击 `vercel` 旁边的展开按钮
   - 查看所有可用工具

4. **禁用不需要的工具**
   - 对于每个不需要的工具，点击旁边的开关或复选框将其禁用
   - 按照上面的列表，禁用所有团队管理、监控分析、安全设置相关的工具

5. **保留需要的工具**
   - 确保以下工具保持启用：
     - 部署相关：`get_deployment`, `get_deployment_events`, `get_deployment_logs`
     - 项目相关：`get_project`, `list_projects`
     - 域名管理：所有 `domain` 相关的工具
     - 环境变量：所有 `environment_variable` 相关的工具

6. **重启 Cursor**
   - 完全关闭并重新打开 Cursor
   - 检查工具总数是否降至 80 以下

## 验证

配置完成后：
- ✅ 总工具数量应该降至 80 以下
- ✅ 警告消息应该消失
- ✅ 仍然可以使用部署检查、域名管理、环境变量管理功能

