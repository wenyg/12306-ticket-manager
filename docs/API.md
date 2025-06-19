# API 文档

## 概述

12306 车票信息管理系统提供 RESTful API 接口，用于获取和管理车票信息。

## 基础信息

- **基础URL**: `http://localhost:8888`
- **API版本**: v1.0.0
- **数据格式**: JSON

## 认证

目前API不需要认证，但在生产环境中建议添加适当的认证机制。

## 接口列表

### 1. 获取所有车票信息

获取系统中的所有车票信息。

**请求**
```http
GET /tickets
```

**响应**
```json
{
  "total": 10,
  "tickets": [
    {
      "order_id": "E123456789",
      "passenger_name": "温阳光",
      "departure_time": "2024-01-15T08:30:00",
      "departure_station": "北京",
      "arrival_station": "上海",
      "train_number": "G1次列车",
      "carriage_number": "8车",
      "seat_number": "12A号",
      "seat_type": "二等座",
      "price": 553.5,
      "is_waiting": false,
      "is_refunded": false,
      "is_changed": false,
      "service_fee": 0.0,
      "created_at": "2024-01-01T10:00:00",
      "updated_at": "2024-01-01T10:00:00"
    }
  ]
}
```

### 2. 获取车票统计信息

获取车票的统计信息，包括总数、金额等。

**请求**
```http
GET /tickets/stats
```

**响应**
```json
{
  "total_tickets": 10,
  "waiting_tickets": 2,
  "total_amount": 5535.0,
  "refund_count": 1,
  "total_fees": 50.0,
  "avg_price": 553.5,
  "waiting_percentage": 20.0
}
```

### 3. 根据日期范围获取车票

根据指定的日期范围获取车票信息。

**请求**
```http
GET /tickets/range?start_date=2024-01-01&end_date=2024-01-31
```

**参数**
- `start_date` (string): 开始日期，格式：YYYY-MM-DD
- `end_date` (string): 结束日期，格式：YYYY-MM-DD

**响应**
```json
{
  "start_date": "2024-01-01",
  "end_date": "2024-01-31",
  "total": 5,
  "tickets": [...]
}
```

### 4. 手动更新车票信息

手动触发从邮箱读取并更新车票信息。

**请求**
```http
GET /update_ticket
```

**响应**
```json
{
  "message": "Ticket updated successfully",
  "status": "success"
}
```

### 5. 健康检查

检查系统运行状态。

**请求**
```http
GET /health
```

**响应**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### 6. 获取Web页面

获取车票信息的Web界面。

**请求**
```http
GET /tickets/web
```

**响应**
返回HTML页面内容。

## 错误处理

当API发生错误时，会返回相应的HTTP状态码和错误信息。

**错误响应格式**
```json
{
  "detail": "错误描述信息"
}
```

**常见状态码**
- `200`: 请求成功
- `400`: 请求参数错误
- `404`: 资源不存在
- `500`: 服务器内部错误

## 示例

### 使用curl获取车票信息

```bash
# 获取所有车票
curl http://localhost:8888/tickets

# 获取统计信息
curl http://localhost:8888/tickets/stats

# 手动更新车票
curl http://localhost:8888/update_ticket
```

### 使用Python requests

```python
import requests

# 获取所有车票
response = requests.get('http://localhost:8888/tickets')
tickets = response.json()

# 获取统计信息
response = requests.get('http://localhost:8888/tickets/stats')
stats = response.json()

# 手动更新车票
response = requests.get('http://localhost:8888/update_ticket')
result = response.json()
```

## 数据模型

### 车票信息 (Ticket)

| 字段 | 类型 | 描述 |
|------|------|------|
| order_id | string | 订单号 |
| passenger_name | string | 乘客姓名 |
| departure_time | datetime | 出发时间 |
| departure_station | string | 出发站 |
| arrival_station | string | 到达站 |
| train_number | string | 车次号 |
| carriage_number | string | 车厢号 |
| seat_number | string | 座位号 |
| seat_type | string | 座位类型 |
| price | float | 票价 |
| is_waiting | boolean | 是否候补 |
| is_refunded | boolean | 是否退票 |
| is_changed | boolean | 是否改签 |
| service_fee | float | 手续费 |
| created_at | datetime | 创建时间 |
| updated_at | datetime | 更新时间 |

### 统计信息 (Statistics)

| 字段 | 类型 | 描述 |
|------|------|------|
| total_tickets | integer | 总车票数（不包括退票） |
| waiting_tickets | integer | 候补车票数 |
| total_amount | float | 总金额（不包括退票） |
| refund_count | integer | 退票次数 |
| total_fees | float | 总手续费 |
| avg_price | float | 平均票价 |
| waiting_percentage | float | 候补比例 |

## 注意事项

1. 所有时间字段使用ISO 8601格式
2. 金额字段使用浮点数，精确到小数点后2位
3. 布尔字段使用true/false
4. 建议在生产环境中添加适当的缓存机制
5. 大量数据查询时建议使用分页 