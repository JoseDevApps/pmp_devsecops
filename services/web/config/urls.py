from django.contrib import admin
from django.http import HttpResponse, JsonResponse
from django.urls import path


def health(request):
    return JsonResponse({"status": "ok", "service": "web"})


def home(request):
    html = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PMP — Portal de Gestión</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #0f172a;
      color: #e2e8f0;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .container {
      max-width: 720px;
      width: 100%;
      padding: 2rem;
      text-align: center;
    }
    .badge {
      display: inline-block;
      background: #22c55e22;
      color: #22c55e;
      border: 1px solid #22c55e44;
      border-radius: 9999px;
      padding: 0.25rem 0.9rem;
      font-size: 0.78rem;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      margin-bottom: 1.5rem;
    }
    h1 {
      font-size: 2.5rem;
      font-weight: 700;
      color: #f8fafc;
      margin-bottom: 0.75rem;
    }
    h1 span { color: #38bdf8; }
    p.subtitle {
      color: #94a3b8;
      font-size: 1rem;
      margin-bottom: 2.5rem;
    }
    .services {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
      gap: 1rem;
      margin-bottom: 2rem;
    }
    .card {
      background: #1e293b;
      border: 1px solid #334155;
      border-radius: 12px;
      padding: 1.25rem 1rem;
      text-decoration: none;
      color: inherit;
      transition: border-color 0.2s, transform 0.1s;
    }
    .card:hover { border-color: #38bdf8; transform: translateY(-2px); }
    .card .icon { font-size: 1.8rem; margin-bottom: 0.5rem; }
    .card .name { font-size: 0.9rem; font-weight: 600; color: #f1f5f9; }
    .card .desc { font-size: 0.75rem; color: #64748b; margin-top: 0.25rem; }
    .card .dot {
      display: inline-block;
      width: 7px; height: 7px;
      border-radius: 50%;
      background: #22c55e;
      margin-right: 4px;
      vertical-align: middle;
    }
    .stack {
      font-size: 0.72rem;
      color: #475569;
      margin-top: 1.5rem;
    }
    .stack span {
      display: inline-block;
      background: #1e293b;
      border: 1px solid #334155;
      border-radius: 4px;
      padding: 2px 8px;
      margin: 2px;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="badge">&#x2022; DevSecOps — Microservicios activos</div>
    <h1>PMP <span>Portal</span></h1>
    <p class="subtitle">
      Entorno de desarrollo · Django 4.2 · Python 3.12
    </p>

    <div class="services">
      <a class="card" href="/health/">
        <div class="icon">&#x1F4BB;</div>
        <div class="name"><span class="dot"></span>Web</div>
        <div class="desc">Dashboard &amp; Auth</div>
      </a>
      <a class="card" href="http://localhost:8051/api/health/" target="_blank">
        <div class="icon">&#x1F527;</div>
        <div class="name"><span class="dot"></span>API REST</div>
        <div class="desc">DRF + JWT · :8051</div>
      </a>
      <a class="card" href="http://localhost:8052/health/" target="_blank">
        <div class="icon">&#x26A1;</div>
        <div class="name"><span class="dot"></span>WebSocket</div>
        <div class="desc">Channels · :8052</div>
      </a>
      <a class="card" href="/admin/" >
        <div class="icon">&#x1F512;</div>
        <div class="name">Admin</div>
        <div class="desc">Django Admin</div>
      </a>
      <a class="card" href="http://localhost:9011" target="_blank">
        <div class="icon">&#x1F5C4;</div>
        <div class="name">MinIO</div>
        <div class="desc">Object storage</div>
      </a>
    </div>

    <div class="stack">
      <span>PostgreSQL 15</span>
      <span>Redis 7</span>
      <span>MinIO</span>
      <span>Celery 5.3</span>
      <span>Nginx 1.27</span>
      <span>Docker Compose</span>
    </div>
  </div>
</body>
</html>
"""
    return HttpResponse(html)


urlpatterns = [
    path("", home),
    path("health/", health),
    path("admin/", admin.site.urls),
]
