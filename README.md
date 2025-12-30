## 启动项目步骤

1. 生成虚拟环境
   ``python3 -m venv env``
2. 激活虚拟环境
   ``. env/bin/activate``
3. 通过 requirements.txt 安装依赖，如果有些依赖版本不对，手动修改requirements.txt中对应库的依赖版本
   ``pip install -r requirements.txt``
4. 生成新的requirements.txt
   ``pip freeze > requirements.txt``