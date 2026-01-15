# Tabby Config Sync

English | [中文](README_ZH.md)

A simple service for syncing Tabby configurations.

It implements the configuration synchronization function of [tabby-web](https://github.com/Eugeny/tabby-web) and provides a basic management interface.

## Why develop this project?

As of now, the tabby-web project is no longer maintained, and its OAuth functionality is malfunctioning, making it unusable.

Therefore, I developed this simple project to solve the problem of syncing tabby client configurations, as other features are not necessary for my use case.

## How to use?

### Deploy with Docker

Run the following command to deploy the service:

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

### Deploy with Docker Compose

```bash
touch .env
echo "JWT__SECRET=$(openssl rand -base64 32)" >> .env
docker compose up -d
```
