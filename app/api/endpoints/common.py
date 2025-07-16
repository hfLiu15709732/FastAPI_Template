from typing import List
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
import datetime
import random
import uuid
import pandas as pd
import io
from app.utils.response_models import success_response, error_response, UnifiedResponse

router = APIRouter()

class User(BaseModel):
    username: str
    email: str
    age: int
    hobbies:List[str]

# 1.最一般的get请求
@router.get("/time",summary="最一般的get请求")
def get_server_time():
    return {"server_time": datetime.datetime.now()}

# 2.get请求---接收queryparam参数
@router.get("/random",summary="get请求---接收queryparam参数")
def generate_random_number(min: int = 0, max: int = 100):
    if min > max:
        raise HTTPException(status_code=400, detail="最小值不能大于最大值")
    return {"random_number": random.randint(min, max)}

# 3.get请求---接收动态路由参数
@router.get("/videos/{videoId}",summary="get请求---接收动态路由参数")
def get_Videos(videoId: str):
    try:
        video_id_int = int(videoId)
    except ValueError:
        raise HTTPException(status_code=400, detail="videoId 必须是整数")
    return {"originalVideoData": f"第{video_id_int}个视频信息"}

# 4.POST请求----接收JSON Body
@router.post("/user/create", response_model=UnifiedResponse,summary="POST请求----接收JSON Body")
async def create_user(user: User):
    try:
        user_data = user.dict()
        user_data["id"] = str(uuid.uuid4())
        user_data["created_at"] = datetime.datetime.now().isoformat()
        return success_response(
            data=user_data,
            message="用户创建成功"
        )
    except Exception as e:
        return error_response(
            message=f"创建用户失败: {str(e)}",
            code=400
        )

# 5. POST请求----接收CSV文件并返回JSON
@router.post("/upload-csv/",summary="POST请求----接收CSV文件并返回JSON")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="文件类型不正确，请上传CSV文件")
    
    try:
        contents = await file.read()
        # 使用io.StringIO将字节内容转换为字符串，以便pandas读取
        sio = io.StringIO(contents.decode('utf-8'))
        df = pd.read_csv(sio)
        
        # 将DataFrame转换为JSON格式
        # orient='records' 将DataFrame转换为列表，其中每个元素是一个字典，代表一行数据
        json_data = df.to_dict(orient='records')
        
        return {"filename": file.filename, "data": json_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理文件时发生错误: {e}")

@router.post("/upload-file/",summary="POST请求----接收通用文件并返回JSON")
async def upload_file(file: UploadFile = File(...)):
    """
    上传文件接口，支持CSV、TXT和Excel格式（暂时项目未引用openpyxl，所有暂时不能使用）
    """
    try:
        # 检查文件类型
        file_extension = file.filename.split('.')[-1].lower()
        if file_extension not in ['csv', 'txt', 'xlsx', 'xls']:
            raise HTTPException(status_code=400, detail="只支持CSV、TXT或Excel文件 (.xlsx, .xls)")
        
        # 读取文件内容
        contents = await file.read()
        
        # 根据文件类型处理内容
        if file_extension == 'csv':
            # 处理CSV文件
            df = pd.read_csv(io.StringIO(contents.decode('gbk')))
            return df.to_dict(orient='records')
        elif file_extension == 'txt':
            # 处理TXT文件
            text = contents.decode('gbk')
            return {"filename": file.filename, "content": text}
        elif file_extension in ['xlsx', 'xls']:
            # 处理Excel文件
            df = pd.read_excel(io.BytesIO(contents))
            return df.to_dict(orient='records')
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件处理错误: {str(e)}")
