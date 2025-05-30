from pydantic import BaseModel, Field
from typing import Optional, Any, Dict, List, Generic, TypeVar
from datetime import datetime

T = TypeVar('T')


class BaseResponse(BaseModel, Generic[T]):
    """基础响应模型"""
    code: int = Field(default=0, description="响应码：0成功，其他失败")
    message: str = Field(default="success", description="响应消息")
    data: Optional[T] = Field(default=None, description="响应数据")
    request_id: Optional[str] = Field(default=None, description="请求ID")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="响应时间")


class PaginationResponse(BaseModel, Generic[T]):
    """分页响应模型"""
    total: int = Field(..., description="总记录数")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页记录数")
    total_pages: int = Field(..., description="总页数")
    items: List[T] = Field(..., description="数据列表")

    @classmethod
    def create(cls, items: List[T], total: int, page: int, page_size: int):
        """创建分页响应"""
        total_pages = (total + page_size - 1) // page_size
        return cls(
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            items=items
        )


class ErrorResponse(BaseModel):
    """错误响应模型"""
    code: int = Field(..., description="错误码")
    message: str = Field(..., description="错误消息")
    details: Optional[Dict[str, Any]] = Field(default=None, description="错误详情")
    request_id: Optional[str] = Field(default=None, description="请求ID")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="错误时间")


class SuccessResponse(BaseModel):
    """成功响应模型"""
    code: int = Field(default=0, description="响应码")
    message: str = Field(default="操作成功", description="响应消息")
    data: Optional[Dict[str, Any]] = Field(default=None, description="响应数据")


class ValidationErrorDetail(BaseModel):
    """验证错误详情"""
    field: str = Field(..., description="字段名")
    message: str = Field(..., description="错误消息")
    value: Optional[Any] = Field(default=None, description="错误值")


class BatchOperationRequest(BaseModel):
    """批量操作请求"""
    action: str = Field(..., description="操作类型")
    ids: List[int] = Field(..., description="ID列表")
    data: Optional[Dict[str, Any]] = Field(default=None, description="操作数据")


class BatchOperationResponse(BaseModel):
    """批量操作响应"""
    success_count: int = Field(..., description="成功数量")
    failed_count: int = Field(..., description="失败数量")
    success_ids: List[int] = Field(..., description="成功ID列表")
    failed_items: List[Dict[str, Any]] = Field(..., description="失败项目列表")


class FileUploadResponse(BaseModel):
    """文件上传响应"""
    file_id: str = Field(..., description="文件ID")
    file_name: str = Field(..., description="文件名")
    file_url: str = Field(..., description="文件URL")
    file_size: int = Field(..., description="文件大小(字节)")
    content_type: str = Field(..., description="文件类型")
    upload_time: datetime = Field(default_factory=datetime.utcnow, description="上传时间")
