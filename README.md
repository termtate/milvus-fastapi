# milvus-backend

## 运行前准备

1. 安装rye
   1. 下载rye (https://rye-up.com/guide/installation/)
   2. [添加 `%USERPROFILE%\.rye\shims` 到 Path 环境变量](https://rye-up.com/guide/installation/#add-shims-to-path)
2. 运行milvus
3. 进行词嵌入的模型是从 huggingface.co 下载的，所以很可能需要科学上网；或者可以自行从 https://www.sbert.net/docs/pretrained_models.html 下载模型，然后把src/app/core/config.py的MilvusSettings中`MODEL_NAME_OR_PATH`属性修改为模型的路径
   
## 运行
在当前目录下运行cmd命令：
1. `rye sync`
2. 如果是第一次运行，输入 `rye run init` 初始化数据
3. `rye run pre-start`
4. `rye run main`
   
运行以后，在浏览器输入 http://127.0.0.1:8000/docs 打开api文档（可能需要科学上网）


## 打包

`rye run pack`（很可能需要科学上网）
