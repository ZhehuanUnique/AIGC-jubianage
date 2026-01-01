# Vercel MCP 工具开启/关闭清单

## ✅ 需要开启的工具（保留）

### 部署相关（必须开启）
- ✅ `vercel_get_deployment` - 获取部署信息
- ✅ `vercel_list_deployments` - 列出部署列表
- ✅ `vercel_get_deployment_events` - 获取部署事件
- ✅ `vercel_get_deployment_logs` - 获取部署日志
- ✅ `vercel_get_deployment_events` - 获取部署事件日志

### 项目相关（必须开启）
- ✅ `vercel_get_project` - 获取项目信息
- ✅ `vercel_list_projects` - 列出项目列表

### 域名管理（全部开启）
- ✅ `vercel_list_domains` - 列出域名
- ✅ `vercel_get_domain` - 获取域名信息
- ✅ `vercel_add_domain` - 添加域名
- ✅ `vercel_remove_domain` - 删除域名
- ✅ `vercel_verify_domain` - 验证域名
- ✅ `vercel_list_dns_records` - 列出 DNS 记录
- ✅ `vercel_create_dns_record` - 创建 DNS 记录

### 环境变量管理（全部开启）
- ✅ `vercel_list_env_vars` - 列出环境变量
- ✅ `vercel_create_env_var` - 创建环境变量
- ✅ `vercel_update_env_var` - 更新环境变量
- ✅ `vercel_delete_env_var` - 删除环境变量
- ✅ `vercel_bulk_create_env_vars` - 批量创建环境变量

---

## ❌ 需要关闭的工具（禁用）

### 团队管理工具（全部关闭）
- ❌ `vercel_list_teams` - 列出团队
- ❌ `vercel_get_team` - 获取团队信息
- ❌ `vercel_list_team_members` - 列出团队成员
- ❌ `vercel_invite_team_member` - 邀请团队成员
- ❌ `vercel_remove_team_member` - 移除团队成员
- ❌ `vercel_update_team_member_role` - 更新团队成员角色
- ❌ `vercel_get_team_activity` - 获取团队活动
- ❌ `vercel_get_team_usage` - 获取团队使用情况

### 监控和分析工具（全部关闭）
- ❌ `vercel_get_runtime_logs_stream` - 获取运行时日志流
- ❌ `vercel_get_build_logs` - 获取构建日志
- ❌ `vercel_get_error_logs` - 获取错误日志
- ❌ `vercel_get_bandwidth_usage` - 获取带宽使用情况
- ❌ `vercel_get_function_invocations` - 获取函数调用次数
- ❌ `vercel_get_cache_metrics` - 获取缓存指标
- ❌ `vercel_get_traces` - 获取追踪数据
- ❌ `vercel_get_performance_insights` - 获取性能洞察
- ❌ `vercel_get_web_vitals` - 获取 Web Vitals
- ❌ `vercel_get_project_analytics` - 获取项目分析
- ❌ `vercel_get_deployment_health` - 获取部署健康状态
- ❌ `vercel_get_error_rate` - 获取错误率
- ❌ `vercel_get_response_time` - 获取响应时间
- ❌ `vercel_get_uptime_metrics` - 获取正常运行时间指标
- ❌ `vercel_get_usage_metrics` - 获取使用指标
- ❌ `vercel_get_billing_summary` - 获取账单摘要
- ❌ `vercel_get_cost_breakdown` - 获取成本明细
- ❌ `vercel_export_usage_report` - 导出使用报告
- ❌ `vercel_get_middleware_logs` - 获取中间件日志
- ❌ `vercel_get_middleware_metrics` - 获取中间件指标

### 安全设置工具（全部关闭）
- ❌ `vercel_list_firewall_rules` - 列出防火墙规则
- ❌ `vercel_create_firewall_rule` - 创建防火墙规则
- ❌ `vercel_update_firewall_rule` - 更新防火墙规则
- ❌ `vercel_delete_firewall_rule` - 删除防火墙规则
- ❌ `vercel_get_firewall_analytics` - 获取防火墙分析
- ❌ `vercel_list_blocked_ips` - 列出被阻止的 IP
- ❌ `vercel_block_ip` - 阻止 IP
- ❌ `vercel_unblock_ip` - 取消阻止 IP
- ❌ `vercel_enable_attack_challenge_mode` - 启用攻击挑战模式
- ❌ `vercel_get_security_events` - 获取安全事件
- ❌ `vercel_scan_deployment_security` - 扫描部署安全性
- ❌ `vercel_get_security_headers` - 获取安全头
- ❌ `vercel_update_security_headers` - 更新安全头

### 其他不需要的工具（可以关闭）
- ❌ `vercel_create_deployment` - 创建部署（如果不需要通过 MCP 创建）
- ❌ `vercel_cancel_deployment` - 取消部署（如果不需要）
- ❌ `vercel_delete_deployment` - 删除部署（如果不需要）
- ❌ `vercel_redeploy` - 重新部署（如果不需要）
- ❌ `vercel_rollback_deployment` - 回滚部署（如果不需要）
- ❌ `vercel_pause_deployment` - 暂停部署（如果不需要）
- ❌ `vercel_resume_deployment` - 恢复部署（如果不需要）
- ❌ `vercel_get_deployment_diff` - 获取部署差异（如果不需要）
- ❌ `vercel_update_project` - 更新项目（如果不需要）
- ❌ `vercel_create_project` - 创建项目（如果不需要）
- ❌ `vercel_delete_project` - 删除项目（如果不需要）
- ❌ `vercel_list_webhooks` - 列出 Webhooks（如果不需要）
- ❌ `vercel_create_webhook` - 创建 Webhook（如果不需要）
- ❌ `vercel_delete_webhook` - 删除 Webhook（如果不需要）
- ❌ `vercel_list_aliases` - 列出别名（如果不需要）
- ❌ `vercel_assign_alias` - 分配别名（如果不需要）
- ❌ `vercel_delete_alias` - 删除别名（如果不需要）
- ❌ `vercel_list_secrets` - 列出密钥（如果不需要）
- ❌ `vercel_create_secret` - 创建密钥（如果不需要）
- ❌ `vercel_delete_secret` - 删除密钥（如果不需要）
- ❌ `vercel_list_edge_configs` - 列出边缘配置（如果不需要）
- ❌ `vercel_create_edge_config` - 创建边缘配置（如果不需要）
- ❌ `vercel_list_checks` - 列出检查（如果不需要）
- ❌ `vercel_create_check` - 创建检查（如果不需要）
- ❌ `vercel_list_deployment_files` - 列出部署文件（如果不需要）
- ❌ `vercel_blob_list` - 列出 Blob（如果不需要）
- ❌ `vercel_blob_put` - 上传 Blob（如果不需要）
- ❌ `vercel_kv_get` - KV 存储获取（如果不需要）
- ❌ `vercel_kv_set` - KV 存储设置（如果不需要）
- ❌ `vercel_postgres_list_databases` - 列出 Postgres 数据库（如果不需要）
- ❌ `vercel_list_integrations` - 列出集成（如果不需要）
- ❌ `vercel_list_audit_logs` - 列出审计日志（如果不需要）
- ❌ `vercel_list_cron_jobs` - 列出定时任务（如果不需要）
- ❌ `vercel_list_redirects` - 列出重定向（如果不需要）
- ❌ `vercel_list_custom_headers` - 列出自定义头（如果不需要）
- ❌ `vercel_list_comments` - 列出评论（如果不需要）
- ❌ `vercel_list_git_repositories` - 列出 Git 仓库（如果不需要）
- ❌ `vercel_list_middleware` - 列出中间件（如果不需要）
- ❌ `vercel_create_alert` - 创建警报（如果不需要）
- ❌ `vercel_get_invoice` - 获取发票（如果不需要）
- ❌ `vercel_list_invoices` - 列出发票（如果不需要）
- ❌ `vercel_get_spending_limits` - 获取支出限制（如果不需要）
- ❌ `vercel_get_storage_usage` - 获取存储使用情况（如果不需要）
- ❌ `vercel_optimize_storage` - 优化存储（如果不需要）
- ❌ `vercel_export_blob_data` - 导出 Blob 数据（如果不需要）
- ❌ `vercel_import_blob_data` - 导入 Blob 数据（如果不需要）
- ❌ `vercel_clone_storage` - 克隆存储（如果不需要）
- ❌ `vercel_promote_deployment` - 提升部署（如果不需要）

---

## 📊 快速识别方法

### 需要开启的工具关键词
- `get_deployment` - 部署信息
- `list_deployments` - 部署列表
- `deployment_events` - 部署事件
- `deployment_logs` - 部署日志
- `get_project` - 项目信息
- `list_projects` - 项目列表
- `domain` - 域名相关
- `dns` - DNS 相关
- `env_var` - 环境变量相关

### 需要关闭的工具关键词
- `team` - 团队相关（全部关闭）
- `member` - 成员相关（全部关闭）
- `analytics` - 分析相关（全部关闭）
- `metrics` - 指标相关（全部关闭）
- `logs` - 日志相关（除了 deployment_logs，其他关闭）
- `usage` - 使用情况（全部关闭）
- `performance` - 性能相关（全部关闭）
- `web_vitals` - Web Vitals（关闭）
- `firewall` - 防火墙（全部关闭）
- `security` - 安全相关（全部关闭）
- `blocked` - 阻止相关（全部关闭）
- `billing` - 账单相关（全部关闭）
- `invoice` - 发票相关（全部关闭）
- `audit` - 审计相关（全部关闭）
- `integration` - 集成相关（如果不需要，关闭）
- `webhook` - Webhook（如果不需要，关闭）
- `secret` - 密钥（如果不需要，关闭）
- `edge_config` - 边缘配置（如果不需要，关闭）
- `blob` - Blob 存储（如果不需要，关闭）
- `kv` - KV 存储（如果不需要，关闭）
- `postgres` - Postgres（如果不需要，关闭）
- `middleware` - 中间件（如果不需要，关闭）
- `cron` - 定时任务（如果不需要，关闭）
- `redirect` - 重定向（如果不需要，关闭）
- `comment` - 评论（如果不需要，关闭）
- `git` - Git 仓库（如果不需要，关闭）

---

## 🎯 操作步骤

1. **在 Cursor 设置中找到 Vercel MCP**
   - 打开 Cursor 设置（`Ctrl + ,`）
   - 搜索 "MCP" 或找到 "Model Context Protocol"
   - 展开 `vercel` 服务器

2. **批量关闭不需要的工具**
   - 按照上面的清单，关闭所有标记为 ❌ 的工具
   - 保留所有标记为 ✅ 的工具

3. **验证工具数量**
   - 关闭后，总工具数量应该大幅减少
   - 目标：控制在 80 个以下

4. **重启 Cursor**
   - 完全关闭并重新打开 Cursor
   - 检查警告是否消失

---

## 📝 总结

**需要开启的工具数量**：约 15-20 个
- 部署相关：5 个
- 项目相关：2 个
- 域名管理：7 个
- 环境变量：5 个

**需要关闭的工具数量**：约 130+ 个
- 团队管理：8 个
- 监控分析：20+ 个
- 安全设置：12+ 个
- 其他不需要的功能：90+ 个

关闭后，工具总数应该从 150 个降至 20 个左右，远低于 80 个的限制。

