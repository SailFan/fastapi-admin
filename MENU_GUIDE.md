# 添加新的一级菜单和二级菜单操作指南

## 📋 操作步骤

### 第一步：添加一级菜单（目录类型）

1. **访问菜单管理页面**
   - 登录系统后，进入：**系统管理 → 菜单管理**

2. **点击"新建根菜单"按钮**

3. **填写一级菜单信息：**
   ```
   菜单类型：目录 (catalog)
   上级菜单：根目录 (parent_id = 0)
   菜单名称：业务管理 (示例)
   访问路径：/business
   组件路径：留空（目录类型不需要）
   跳转路径：/business/order (可选，点击一级菜单时默认跳转到第一个二级菜单)
   菜单图标：选择一个图标，如 mdi:briefcase-outline
   显示排序：3
   是否隐藏：关闭
   KeepAlive：根据需要
   ```

4. **点击保存**

### 第二步：添加二级菜单（菜单类型）

在菜单列表中，找到刚创建的一级菜单，点击右侧的 **"子菜单"** 按钮，然后逐个添加二级菜单：

#### 示例：订单管理（二级菜单1）
```
菜单类型：菜单 (menu)
上级菜单：业务管理（会自动选中）
菜单名称：订单管理
访问路径：order (相对路径，会自动拼接到 /business 后面，最终路径为 /business/order)
组件路径：/business/order ⚠️ 重要：这个路径对应前端组件文件位置
菜单图标：material-symbols:shopping-cart-outline
显示排序：1
是否隐藏：关闭
KeepAlive：根据需要
```

#### 示例：商品管理（二级菜单2）
```
菜单类型：菜单 (menu)
上级菜单：业务管理
菜单名称：商品管理
访问路径：product
组件路径：/business/product
菜单图标：material-symbols:inventory-2-outline
显示排序：2
是否隐藏：关闭
KeepAlive：根据需要
```

#### 示例：客户管理（二级菜单3）
```
菜单类型：菜单 (menu)
上级菜单：业务管理
菜单名称：客户管理
访问路径：customer
组件路径：/business/customer
菜单图标：material-symbols:people-outline
显示排序：3
是否隐藏：关闭
KeepAlive：根据需要
```

### 第三步：创建前端组件文件

⚠️ **重要：** 必须为每个二级菜单创建对应的 Vue 组件文件，否则路由无法正常工作。

组件文件的路径规则：
- **组件路径 `/business/order`** → **文件路径** `web/src/views/business/order/index.vue`
- **组件路径 `/business/product`** → **文件路径** `web/src/views/business/product/index.vue`
- **组件路径 `/business/customer`** → **文件路径** `web/src/views/business/customer/index.vue`

#### 创建目录结构：
```bash
mkdir -p web/src/views/business/order
mkdir -p web/src/views/business/product
mkdir -p web/src/views/business/customer
```

#### 组件文件示例（简单版）：

**`web/src/views/business/order/index.vue`**
```vue
<template>
  <AppPage>
    <n-card title="订单管理">
      <p>订单管理页面内容</p>
    </n-card>
  </AppPage>
</template>

<script setup>
defineOptions({ name: '订单管理' })
</script>
```

**`web/src/views/business/product/index.vue`**
```vue
<template>
  <AppPage>
    <n-card title="商品管理">
      <p>商品管理页面内容</p>
    </n-card>
  </AppPage>
</template>

<script setup>
defineOptions({ name: '商品管理' })
</script>
```

**`web/src/views/business/customer/index.vue`**
```vue
<template>
  <AppPage>
    <n-card title="客户管理">
      <p>客户管理页面内容</p>
    </n-card>
  </AppPage>
</template>

<script setup>
defineOptions({ name: '客户管理' })
</script>
```

### 第四步：刷新路由

添加菜单和创建组件后，需要：
1. **退出登录并重新登录**（路由会在登录时重新生成）
2. 或者手动刷新页面，系统会自动重新加载菜单

## 📝 重要说明

### 路径规则

1. **访问路径（path）**：
   - 一级菜单：`/business`（绝对路径，以 `/` 开头）
   - 二级菜单：`order`（相对路径，不以 `/` 开头）

2. **组件路径（component）**：
   - 必须与前端文件路径对应
   - 格式：`/business/order` → 对应 `web/src/views/business/order/index.vue`
   - 必须以 `/` 开头，且必须以 `/index.vue` 的文件名映射

3. **跳转路径（redirect）**：
   - 只有一级菜单（目录）可以设置
   - 用于点击一级菜单时，默认跳转到指定的二级菜单

### 菜单类型说明

- **目录（catalog）**：一级菜单，不直接显示页面，只作为容器
- **菜单（menu）**：二级菜单，对应具体的页面组件

### 注意事项

1. ⚠️ **组件路径和文件路径必须一致**，否则路由会404
2. ⚠️ **必须创建对应的组件文件**，否则无法访问页面
3. ⚠️ **菜单保存后需要重新登录**才能生效
4. ✅ 可以使用"子菜单"按钮快速添加，会自动设置父级关系
5. ✅ 菜单排序可以通过"显示排序"字段控制显示顺序

## 🔍 示例：完整的"业务管理"菜单结构

```
一级菜单：业务管理
├── 访问路径：/business
├── 跳转路径：/business/order
├── 组件路径：Layout（自动，目录类型）
│
├── 二级菜单1：订单管理
│   ├── 访问路径：order
│   ├── 完整路径：/business/order
│   └── 组件路径：/business/order
│       └── 对应文件：web/src/views/business/order/index.vue
│
├── 二级菜单2：商品管理
│   ├── 访问路径：product
│   ├── 完整路径：/business/product
│   └── 组件路径：/business/product
│       └── 对应文件：web/src/views/business/product/index.vue
│
└── 二级菜单3：客户管理
    ├── 访问路径：customer
    ├── 完整路径：/business/customer
    └── 组件路径：/business/customer
        └── 对应文件：web/src/views/business/customer/index.vue
```

## 🛠️ 故障排查

如果菜单不显示或404：

1. **检查组件文件是否存在**：确认 `web/src/views/{组件路径}/index.vue` 文件存在
2. **检查路径是否正确**：组件路径必须以 `/` 开头
3. **检查权限**：确认当前角色有该菜单的访问权限
4. **刷新路由**：退出登录后重新登录
5. **查看浏览器控制台**：检查是否有路由错误信息
