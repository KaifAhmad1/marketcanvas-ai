import reflex as rx
from frontend.pages import home, editor, gallery
from frontend.states.app_state import AppState
from frontend.styles.themes import get_theme_styles
import asyncio
import uvicorn
from backend.api.main import app as fastapi_app

config = rx.Config(
    app_name="marketcanvas_ai",
    cors_allowed_origins=["http://localhost:3000", "http://localhost:8000"],
    api_url="http://localhost:8000",
)

app = rx.App(
    state=AppState,
    style=get_theme_styles(),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
        "/static/custom.css"
    ]
)

app.add_page(home.index, route="/", title="MarketCanvas AI")
app.add_page(editor.index, route="/editor", title="Visual Editor")
app.add_page(gallery.index, route="/gallery", title="Gallery")

app.add_custom_code("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --primary: #6366f1;
    --primary-dark: #4f46e5;
    --secondary: #f1f5f9;
    --accent: #06b6d4;
    --background: #ffffff;
    --surface: #f8fafc;
    --text: #0f172a;
    --text-muted: #64748b;
    --border: #e2e8f0;
    --shadow: rgba(0, 0, 0, 0.1);
}

[data-theme="dark"] {
    --background: #0f172a;
    --surface: #1e293b;
    --text: #f8fafc;
    --text-muted: #94a3b8;
    --border: #334155;
    --shadow: rgba(0, 0, 0, 0.3);
}

.gradient-bg {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.glass-effect {
    backdrop-filter: blur(10px);
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.animate-float {
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

.animate-pulse-slow {
    animation: pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.animate-gradient {
    background-size: 200% 200%;
    animation: gradient 3s ease infinite;
}

@keyframes gradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
</style>
""")

async def run_servers():
    fastapi_config = uvicorn.Config(
        "backend.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
    fastapi_server = uvicorn.Server(fastapi_config)

    await asyncio.gather(
        fastapi_server.serve(),
    )

if __name__ == "__main__":
    app.compile()
