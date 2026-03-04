-- 创建订单表
CREATE TABLE IF NOT EXISTS "order" (
    id BIGSERIAL PRIMARY KEY,
    uuid UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    order_no VARCHAR(100) UNIQUE NOT NULL,
    platform VARCHAR(50),
    shop_name VARCHAR(100),
    product_name VARCHAR(200),
    order_time TIMESTAMP WITH TIME ZONE,
    order_amount DECIMAL(10, 2) DEFAULT 0,
    user_id VARCHAR(100),
    order_count INT DEFAULT 1,
    total_amount DECIMAL(10, 2) DEFAULT 0,
    customer_name VARCHAR(100),
    customer_group VARCHAR(100),
    usage_time VARCHAR(100),
    operation_user VARCHAR(100),
    status VARCHAR(20) DEFAULT 'pending',
    remark TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_order_uuid ON "order"(uuid);
CREATE INDEX IF NOT EXISTS idx_order_no ON "order"(order_no);
CREATE INDEX IF NOT EXISTS idx_order_platform ON "order"(platform);
CREATE INDEX IF NOT EXISTS idx_order_time ON "order"(order_time);
CREATE INDEX IF NOT EXISTS idx_order_status ON "order"(status);
CREATE INDEX IF NOT EXISTS idx_order_created_at ON "order"(created_at);
CREATE INDEX IF NOT EXISTS idx_order_updated_at ON "order"(updated_at);

-- 插入测试数据
INSERT INTO "order" (order_no, platform, shop_name, product_name, order_time, order_amount, user_id, order_count, total_amount, customer_name, customer_group, usage_time, operation_user, status, remark)
VALUES 
('ORD20260302001', '淘宝', '测试店铺A', '商品A', NOW(), 99.99, 'USER001', 1, 99.99, '张三', 'VIP客户', '30天', 'admin', 'completed', '测试订单1'),
('ORD20260302002', '京东', '测试店铺B', '商品B', NOW(), 199.99, 'USER002', 2, 399.98, '李四', '普通客户', '60天', 'admin', 'pending', '测试订单2'),
('ORD20260302003', '拼多多', '测试店铺C', '商品C', NOW(), 49.99, 'USER003', 1, 49.99, '王五', 'VIP客户', '15天', 'admin', 'completed', '测试订单3'),
('ORD20260302004', '抖音', '测试店铺D', '商品D', NOW(), 299.99, 'USER004', 3, 899.97, '赵六', '企业客户', '90天', 'admin', 'pending', '测试订单4'),
('ORD20260302005', '淘宝', '测试店铺E', '商品E', NOW(), 79.99, 'USER005', 1, 79.99, '孙七', '普通客户', '30天', 'admin', 'cancelled', '测试订单5');
