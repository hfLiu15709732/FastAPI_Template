
## 安装

1.  **克隆仓库**

    ```bash
    git clone <您的仓库地址>
    cd FastAPI_Prj_Con
    ```

2.  **创建并激活虚拟环境**

    推荐使用 `poetry` 进行依赖管理：

    ```bash
    poetry install
    poetry shell
    ```

    或者使用 `pip`：

    ```bash
    python -m venv .venv
    .venv\Scripts\activate  # Windows
    # source .venv/bin/activate # macOS/Linux
    pip install -r requirements.txt # 如果有requirements.txt文件
    # 或者手动安装依赖
    pip install fastapi uvicorn pandas python-multipart openpyxl
    ```

3.  **安装必要的依赖**

    确保安装了文件上传和处理所需的库：

    ```bash
    pip install pandas python-multipart openpyxl
    ```

## 运行项目

使用 `uvicorn` 启动FastAPI应用：

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 3008