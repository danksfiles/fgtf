from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from enum import Enum


class AlertSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class SystemHealth(BaseModel):
    id: Optional[int] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    component: str
    status: str = Field(..., pattern=r'^(healthy|warning|critical)$')
    cpu_usage: Optional[float] = Field(None, ge=0, le=100)
    memory_usage: Optional[float] = Field(None, ge=0, le=100)
    disk_usage: Optional[float] = Field(None, ge=0, le=100)
    api_latency_ms: Optional[int] = Field(None, ge=0)
    error_rate: Optional[float] = Field(None, ge=0, le=1)


class Alert(BaseModel):
    alert_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.now)
    severity: AlertSeverity
    component: str
    message: str
    is_resolved: bool = False
    resolved_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)