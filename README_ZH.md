# Tabby Config Sync

[English](README.md) | 中文

一个用于同步 Tabby 配置的简易服务。

实现了 [tabby-web](https://github.com/Eugeny/tabby-web) 配置同步功能，并提供了基础的管理界面。

## 为什么要开发这个项目？

截至目前，tabby-web 项目已经停止维护，且 OAuth 功能存在异常，导致无法正常使用。

因此，我开发了这个简单的项目，用于解决 tabby 客户端配置同步问题，其他功能来说对我都是无用的。

## 如何使用？

### 使用 Docker 部署

运行以下命令即可部署服务：

```bash
docker volume create tabby-config-sync-data
export JWT__SECRET=$(openssl rand -base64 32)
docker run -d \
    --name tabby-config-sync \
    --restart unless-stopped \
    -p 8000:8000 \
    -v tabby-config-sync-data:/app/data \
    -e JWT__SECRET=${JWT__SECRET} \
    ghcr.io/terracecn/tabby-config-sync
```

### 使用 Docker-Compose 部署

```bash
touch .env
echo "JWT__SECRET=$(openssl rand -base64 32)" >> .env
docker compose up -d
```