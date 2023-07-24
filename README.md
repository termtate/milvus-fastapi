# milvus-backend

## 运行前准备

1. 安装rye
   1. [下载rye](https://rye-up.com/guide/installation/)
   2. [添加 `%USERPROFILE%\.rye\shims` 到Path环境变量](https://rye-up.com/guide/installation/#add-shims-to-path)
2. 运行milvus
   
## 运行
在当前目录下运行cmd命令：
1. `rye sync`
2. 如果是第一次运行，输入 `rye run python src/milvus_backend/initial_data.py` 初始化数据
3. 