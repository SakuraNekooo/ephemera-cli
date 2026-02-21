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

```bash
# 查看账户信息
ephemera profile

# 查看可用计划
ephemera plans

# 列出实例
ephemera list

# 部署实例
ephemera deploy --product-id 38 --os-id 1 --time 24

# 实例操作
ephemera state <id>
ephemera power <id> shutdown
ephemera renew <id> --time 12
ephemera delete <id>
```

## 仓库

https://github.com/SakuraNekooo/ephemera-cli
