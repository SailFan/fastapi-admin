# 订单管理系统

## 功能说明

订单管理系统用于管理电商平台的订单信息，支持多平台订单统一管理。

## 功能特性

### 1. 订单列表
- 支持按订单编号、平台、状态、客户名称搜索
- 显示订单详细信息（编号、平台、店铺、产品、金额等）
- 状态标签显示（待处理、已完成、已取消）
- 支持编辑和删除操作

### 2. 订单创建
- 订单基本信息：订单编号、平台、店铺名称、产品名称
- 时间信息：下单时间
- 金额信息：订单金额、订单数量、总金额
- 客户信息：客户名称、客户分组、使用时长
- 其他信息：操作人、状态、备注

### 3. 订单状态
- **pending**（待处理）：新创建的订单
- **completed**（已完成）：已完成的订单
- **cancelled**（已取消）：已取消的订单

### 4. 支持平台
- 淘宝
- 京东
- 拼多多
- 抖音

## API 接口

### 基础路径
```
http://localhost:9999/api/v1/order
```

### 接口列表

#### 1. 获取订单列表
```
GET /list
参数：
- page: 页码（默认1）
- page_size: 每页数量（默认20）
- order_no: 订单编号（模糊查询）
- platform: 平台名称
- status: 订单状态
- customer_name: 客户名称（模糊查询）
```

#### 2. 获取订单详情
```
GET /get?order_id=1
```

#### 3. 创建订单
```
POST /create
Body: {
  "order_no": "ORD20260302001",
  "platform": "淘宝",
  "shop_name": "测试店铺",
  "product_name": "测试商品",
  "order_amount": 99.99,
  "order_count": 1,
  "total_amount": 99.99,
  "customer_name": "张三",
  "status": "pending"
}
```

#### 4. 更新订单
```
POST /update
Body: {
  "id": 1,
  "status": "completed"
}
```

#### 5. 删除订单
```
DELETE /delete?order_id=1
```

## 数据库表结构

### order 表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGSERIAL | 主键 |
| uuid | UUID | 唯一标识 |
| order_no | VARCHAR(100) | 订单编号（唯一） |
| platform | VARCHAR(50) | 平台名称 |
| shop_name | VARCHAR(100) | 店铺名称 |
| product_name | VARCHAR(200) | 产品名称 |
| order_time | TIMESTAMP | 下单时间 |
| order_amount | DECIMAL(10,2) | 订单金额 |
| user_id | VARCHAR(100) | 用户ID |
| order_count | INT | 订单数量 |
| total_amount | DECIMAL(10,2) | 总金额 |
| customer_name | VARCHAR(100) | 客户名称 |
| customer_group | VARCHAR(100) | 客户分组 |
| usage_time | VARCHAR(100) | 使用时长 |
| operation_user | VARCHAR(100) | 操作人 |
| status | VARCHAR(20) | 订单状态 |
| remark | TEXT | 备注 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

## 使用说明

### 1. 创建数据库表
```bash
# 方法1：使用 SQL 文件
psql -U admin -d fastapi_admin -f sql/create_order_table.sql

# 方法2：使用 Aerich 迁移
aerich migrate
aerich upgrade
```

### 2. 访问页面
在菜单中添加"订单管理"菜单，路径为 `/order/list`

### 3. 测试数据
SQL 文件中已包含5条测试数据，可直接使用

## 前端页面

### 订单列表页面
- 路径：`/order/list`
- 文件：`web/src/views/order/list/index.vue`
- 功能：订单列表展示、搜索、新建、编辑、删除

## 注意事项

1. 订单编号必须唯一
2. 金额字段使用 DECIMAL 类型，保留2位小数
3. 订单状态只能是：pending、completed、cancelled
4. 删除订单前请确认，删除后无法恢复
