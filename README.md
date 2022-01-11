## 安装依赖

```shell
pipenv install
```

## 启动

```shell
uwsgi --ini uwsgi.ini
```

## 停止

```shell
uwsgi --stop uwsgi/uwsgi.pid
```

## 重启

```shell
uwsgi --reload uwsgi/uwsgi.pid
```