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