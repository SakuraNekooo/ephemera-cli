# Ephemera CLI

Alice EVO Cloud API 命令行工具。

## 安装

### 从 GitHub 安装

```bash
pip install git+https://github.com/SakuraNekooo/ephemera-cli.git
```

### 从源码安装

```bash
git clone https://github.com/SakuraNekooo/ephemera-cli.git
cd ephemera-cli
pip install -e .
```

## 配置

```bash
export EPHEMERA_ACCESS_KEY="your_access_key"
export EPHEMERA_SECRET_KEY="your_secret_key"
```

或创建配置文件 `~/.ephemera/credentials`:

```
access_key=your_access_key
secret_key=your_secret_key
```

## 使用

### 账户

```bash
ephemera profile        # 查看账户信息
ephemera ssh-keys       # 查看SSH密钥
ephemera permissions    # 查看权限
```

### 实例管理

```bash
ephemera plans                      # 查看可用计划
ephemera os-images 38               # 查看计划的可用系统
ephemera list                       # 列出实例
ephemera state <id>                 # 查看实例状态
ephemera deploy --product-id 38 --os-id 1 --time 24  # 部署实例
ephemera power <id> shutdown        # 关机
ephemera power <id> boot            # 开机
ephemera renew <id> --time 12       # 续费
ephemera rebuild <id> --os-id 1     # 重装系统
ephemera delete <id>                # 删除实例
```

### 远程执行

```bash
ephemera exec <id> "uptime"         # 执行命令
ephemera exec-result <id> <uid>     # 查看结果
```

## 版本

当前版本: 1.1.0

## 仓库

https://github.com/SakuraNekooo/ephemera-cli
