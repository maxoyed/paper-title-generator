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
cd uwsgi && uwsgi --stop uwsgi.pid
```

## 重启

```shell
cd uwsgi && uwsgi --reload uwsgi.pid
```