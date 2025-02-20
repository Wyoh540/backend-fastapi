# FastAPI 示例工程

## 数据库

生成迁移数据

```bash
alembic revision --autogenerate -m "init db"
```

更新迁移

```bash
alembic upgrade head
```

## 工程启动

启动celery worker

```bash
celery -A app.celery worker -p solo --concurrency=2  --loglevel=INFO
```
