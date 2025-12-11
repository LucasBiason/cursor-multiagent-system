# SSL/HTTPS com Let's Encrypt e Certbot

**última atualização:** 2025-12-09  
**aplicável a:** todos os projetos em produção com domínio próprio

---

## visão geral

SSL/HTTPS é essencial para segurança em produção. Este guia cobre:
- Configuração de certificados Let's Encrypt via Certbot
- Integração com Nginx em Docker
- Renovação automática de certificados
- Boas práticas de segurança

---

## pré-requisitos

1. **Domínio configurado** apontando para o IP do servidor
2. **Portas 80 e 443** abertas no firewall
3. **Docker e Docker Compose** instalados
4. **Acesso root/SSH** ao servidor

---

## arquitetura básica

```
┌─────────────┐
│   Cliente   │
└──────┬──────┘
       │ HTTPS (443)
       ▼
┌─────────────┐
│    Nginx    │ ← Certificado Let's Encrypt
└──────┬──────┘
       │ HTTP (80)
       ▼
┌─────────────┐
│  Backend    │
│  (Django/   │
│  FastAPI)   │
└─────────────┘
```

---

## configuração no docker-compose

### 1. volumes para certificados

```yaml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.prod.conf:/etc/nginx/conf.d/default.conf:ro
      - certbot_conf:/etc/letsencrypt:ro      # Certificados
      - certbot_www:/var/www/certbot:ro       # Challenge webroot
    depends_on:
      - backend

  certbot:
    image: certbot/certbot
    volumes:
      - certbot_conf:/etc/letsencrypt
      - certbot_www:/var/www/certbot
    entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"

volumes:
  certbot_conf:
  certbot_www:
```

### 2. configuração nginx para SSL

```nginx
# Redirecionar HTTP para HTTPS
server {
    listen 80;
    server_name seu-dominio.com.br www.seu-dominio.com.br;
    
    # Para validação inicial do Certbot (descomentar apenas na primeira vez)
    # location /.well-known/acme-challenge/ {
    #     root /var/www/certbot;
    # }
    
    # Redirecionar todo o resto para HTTPS
    return 301 https://$server_name$request_uri;
}

# Servidor HTTPS
server {
    listen 443 ssl http2;
    server_name seu-dominio.com.br;

    # Certificados Let's Encrypt
    ssl_certificate     /etc/letsencrypt/live/seu-dominio.com.br/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/seu-dominio.com.br/privkey.pem;

    # Configurações SSL modernas
    ssl_protocols       TLSv1.2 TLSv1.3;
    ssl_ciphers         HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # HSTS (opcional, mas recomendado)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Proxy para backend
    location / {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }

    # Static files
    location /static/ {
        alias /app/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /app/media/;
        expires 7d;
        add_header Cache-Control "public";
    }
}
```

---

## processo de configuração inicial

### passo 1: preparar nginx temporário para validação

Antes de obter o certificado, o Nginx precisa servir o challenge do Certbot:

```nginx
server {
    listen 80;
    server_name seu-dominio.com.br;

    # Permitir validação do Certbot
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    # Redirecionar o resto (comentar temporariamente)
    # return 301 https://$server_name$request_uri;
    
    # Servir aplicação normalmente (temporário)
    location / {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### passo 2: obter certificado inicial

```bash
# No servidor, executar:
docker compose run --rm certbot certonly \
  --webroot \
  --webroot-path=/var/www/certbot \
  --email seu-email@example.com \
  --agree-tos \
  --no-eff-email \
  -d seu-dominio.com.br \
  -d www.seu-dominio.com.br
```

**Parâmetros importantes:**
- `--webroot`: Usa validação via arquivo (não precisa parar Nginx)
- `--webroot-path`: Caminho onde o Nginx serve o challenge
- `--email`: Email para notificações de renovação
- `--agree-tos`: Aceita termos de serviço
- `--no-eff-email`: Não compartilha email com EFF
- `-d`: Domínios para certificar (pode ter múltiplos)

### passo 3: atualizar nginx para HTTPS

Após obter o certificado, atualizar `nginx.prod.conf` com a configuração HTTPS completa (ver exemplo acima).

### passo 4: reiniciar serviços

```bash
docker compose restart nginx
```

---

## renovação automática

### configuração no docker-compose

O serviço `certbot` já está configurado para renovar automaticamente:

```yaml
certbot:
  image: certbot/certbot
  volumes:
    - certbot_conf:/etc/letsencrypt
    - certbot_www:/var/www/certbot
  entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"
```

**Como funciona:**
- Executa `certbot renew` a cada 12 horas
- Renova apenas certificados próximos do vencimento (30 dias)
- Não precisa parar o Nginx

### renovação manual (teste)

```bash
# Testar renovação sem aplicar
docker compose run --rm certbot renew --dry-run

# Renovar de verdade
docker compose run --rm certbot renew

# Após renovar, recarregar Nginx
docker compose exec nginx nginx -s reload
```

---

## boas práticas

### 1. segurança SSL

```nginx
# ✅ Usar apenas TLS 1.2 e 1.3
ssl_protocols TLSv1.2 TLSv1.3;

# ✅ Ciphers seguros
ssl_ciphers HIGH:!aNULL:!MD5;

# ✅ HSTS (forçar HTTPS)
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

# ✅ Headers de segurança adicionais
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
```

### 2. performance

```nginx
# ✅ HTTP/2 (já incluído com ssl http2)
listen 443 ssl http2;

# ✅ Cache de sessões SSL
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;

# ✅ OCSP stapling (melhora performance)
ssl_stapling on;
ssl_stapling_verify on;
ssl_trusted_certificate /etc/letsencrypt/live/seu-dominio.com.br/chain.pem;
```

### 3. monitoramento

```bash
# Verificar validade do certificado
docker compose run --rm certbot certificates

# Verificar logs do Certbot
docker compose logs certbot

# Testar SSL online
# https://www.ssllabs.com/ssltest/
```

---

## troubleshooting

### erro: "Failed to obtain certificate"

**Causas comuns:**
1. Domínio não aponta para o servidor
2. Porta 80 bloqueada no firewall
3. Nginx não está servindo `.well-known/acme-challenge/`

**Solução:**
```bash
# Verificar DNS
dig seu-dominio.com.br

# Verificar porta 80
curl -I http://seu-dominio.com.br/.well-known/acme-challenge/test

# Verificar logs do Certbot
docker compose logs certbot
```

### erro: "Certificate not yet due for renewal"

Normal. O Certbot só renova quando faltam menos de 30 dias.

### erro: "Nginx não carrega certificado"

**Verificar:**
1. Caminho do certificado está correto no nginx.conf
2. Volume `certbot_conf` está montado
3. Permissões do certificado

```bash
# Verificar se certificado existe
docker compose exec nginx ls -la /etc/letsencrypt/live/seu-dominio.com.br/

# Verificar configuração do Nginx
docker compose exec nginx nginx -t
```

---

## exemplo completo: django + nginx + certbot

### docker-compose.prod.yml

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    command: prod
    restart: always
    networks:
      - app-network

  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.prod.conf:/etc/nginx/conf.d/default.conf:ro
      - static_files:/app/staticfiles:ro
      - media_files:/app/media:ro
      - certbot_conf:/etc/letsencrypt:ro
      - certbot_www:/var/www/certbot:ro
    depends_on:
      - backend
    networks:
      - app-network

  certbot:
    image: certbot/certbot
    volumes:
      - certbot_conf:/etc/letsencrypt
      - certbot_www:/var/www/certbot
    entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"

volumes:
  static_files:
  media_files:
  certbot_conf:
  certbot_www:

networks:
  app-network:
    driver: bridge
```

### nginx.prod.conf

```nginx
# HTTP → HTTPS redirect
server {
    listen 80;
    server_name seu-dominio.com.br www.seu-dominio.com.br;
    return 301 https://seu-dominio.com.br$request_uri;
}

# HTTPS
server {
    listen 443 ssl http2;
    server_name seu-dominio.com.br;

    # SSL
    ssl_certificate     /etc/letsencrypt/live/seu-dominio.com.br/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/seu-dominio.com.br/privkey.pem;
    ssl_protocols       TLSv1.2 TLSv1.3;
    ssl_ciphers         HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;

    # Backend
    location / {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static
    location /static/ {
        alias /app/staticfiles/;
        expires 30d;
    }

    # Media
    location /media/ {
        alias /app/media/;
        expires 7d;
    }
}
```

---

## checklist de deploy SSL

- [ ] Domínio aponta para IP do servidor
- [ ] Portas 80 e 443 abertas no firewall
- [ ] Nginx configurado para servir `.well-known/acme-challenge/`
- [ ] Certificado obtido via Certbot
- [ ] Nginx configurado com certificados SSL
- [ ] Redirecionamento HTTP → HTTPS funcionando
- [ ] Certbot configurado para renovação automática
- [ ] Headers de segurança configurados
- [ ] Teste SSL realizado (SSLLabs)
- [ ] Monitoramento de renovação configurado

---

## referências

- [Let's Encrypt](https://letsencrypt.org/)
- [Certbot Documentation](https://certbot.eff.org/docs/)
- [SSL Labs Test](https://www.ssllabs.com/ssltest/)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)

---

## responsabilidade do agente CI/CD

O agente CI/CD é responsável por:
1. **Configurar SSL/HTTPS** em todos os projetos em produção
2. **Obter certificados iniciais** via Certbot
3. **Configurar renovação automática** no Docker Compose
4. **Atualizar configurações Nginx** para HTTPS
5. **Monitorar renovação** e resolver problemas
6. **Documentar domínios e certificados** no contexto do projeto

**Arquivos a gerenciar:**
- `nginx.prod.conf` - Configuração Nginx com SSL
- `docker-compose.prod.yml` - Serviços Certbot e volumes
- Documentação do projeto com domínio e status SSL

