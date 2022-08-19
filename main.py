from routers import user, chart
from routers import project
from routers import report
from routers import auth
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# TODO
"""
例外処理
バリデーション
認証
Dockerに乗せる。DBも

updateの際存在したいプロパティを指定しても200が返ってくる(全て）
create_atの付与。自動で入るようにする。nowが

"""
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(project.router)
app.include_router(report.router)
app.include_router(auth.router)
app.include_router(chart.router)


@app.get('/')  # methodとendpointの指定
async def hello():
    text = 'text'
    return {"text": text}
