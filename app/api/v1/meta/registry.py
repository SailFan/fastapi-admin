FIELD_TYPES = [
    {
        "code": "integer",
        "label": "整数",
        "category": "base",
        "config_schema": {
            "min": {
                "type": "number"
            },
            "max": {
                "type": "number"
            }
        }
    },
    {
        "code": "string",
        "label": "字符串",
        "category": "base",
        "config_schema": {
            "min_length": {
                "type": "number"
            },
            "max_length": {
                "type": "number"
            },
            "regex": {
                "type": "string"
            }
        }
    },
    {
        "code": "decimal",
        "label": "高精度数值",
        "category": "base",
        "config_schema": {
            "precision": {
                "type": "number"
            },
            "scale": {
                "type": "number"
            }
        }
    },
    {
        "code": "boolean",
        "label": "布尔值",
        "category": "base",
        "config_schema": {}
    },
    {
        "code": "datetime",
        "label": "时间",
        "category": "base",
        "config_schema": {
            "start": {
                "type": "string"
            },
            "end": {
                "type": "string"
            },
            "format": {
                "type": "string"
            }
        }
    },
    {
        "code": "enum",
        "label": "枚举",
        "category": "base",
        "config_schema": {
            "options": {
                "type": "array"
            }
        }
    },
    {
        "code": "json",
        "label": "JSON",
        "category": "base",
        "config_schema": {}
    }
]

STRATEGIES = [
    {
        "code": "fixed",
        "label": "固定值",
        "supported_types": [
            "integer",
            "string",
            "decimal",
            "boolean",
            "datetime",
            "enum",
            "json"
        ],
        "config_schema": {
            "value": {
                "type": "any"
            }
        }
    },
    {
        "code": "random_range",
        "label": "区间随机",
        "supported_types": [
            "integer",
            "decimal",
            "datetime"
        ],
        "config_schema": {
            "min": {
                "type": "number"
            },
            "max": {
                "type": "number"
            }
        }
    },
    {
        "code": "sequence",
        "label": "自增序列",
        "supported_types": [
            "integer",
            "string"
        ],
        "config_schema": {
            "start": {
                "type": "number"
            },
            "step": {
                "type": "number"
            }
        }
    },
    {
        "code": "expression",
        "label": "表达式",
        "supported_types": [
            "integer",
            "decimal",
            "string",
            "boolean"
        ],
        "config_schema": {
            "formula": {
                "type": "string"
            }
        }
    }
]

DISTRIBUTIONS = [
    {"code": "uniform", "label": "均匀分布"}, {"code": "normal", "label": "正态分布"} ]


CONSTRAINT_TYPES = [ "unique", "not_null", "primary_key" ]