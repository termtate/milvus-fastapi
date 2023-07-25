# milvus-backend

## 运行前准备

1. 安装rye
   1. [下载rye](https://rye-up.com/guide/installation/)
   2. [添加 `%USERPROFILE%\.rye\shims` 到 Path 环境变量](https://rye-up.com/guide/installation/#add-shims-to-path)
2. 运行milvus
   
## 运行
在当前目录下运行cmd命令：
1. `rye sync`
2. 如果是第一次运行，输入 `rye run python src/app/initial_data.py` 初始化数据
3. `rye run python src/app/pre_start.py`
4. `rye run python src/app/main.py`
   
运行以后，在浏览器输入 http://127.0.0.1:8000/docs 打开api文档