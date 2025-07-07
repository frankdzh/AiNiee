# AiNiee 代码风格和约定

## 命名约定
- **类名**: 使用 PascalCase（如 `FileReader`, `TranslatorConfig`）
- **函数名**: 使用 snake_case（如 `load_config`, `display_banner`）
- **变量名**: 使用 snake_case（如 `config_path`, `script_dir`）
- **常量**: 使用 UPPER_SNAKE_CASE（如 `_ATOMIC_TYPES`, `MODULES_TO_EXCLUDE`）
- **私有成员**: 以单下划线开头（如 `_AINIEE_CONFIG_INSTANCE`）

## 文件组织
- **模块化设计**: 功能按模块分离，每个模块有明确职责
- **基类模式**: 使用 Base 类定义通用接口（如 `BaseReader`, `BaseWriter`）
- **工厂模式**: 使用工厂类创建对象（如 `LLMClientFactory`）
- **插件系统**: 支持插件扩展功能

## 代码结构
- **导入顺序**: 标准库 → 第三方库 → 本地模块
- **类结构**: 属性定义 → 构造函数 → 公共方法 → 私有方法
- **错误处理**: 使用 try-catch 块处理异常

## 注释风格
- **文件头注释**: 包含 ASCII 艺术和项目信息
- **函数注释**: 简洁描述功能和参数
- **行内注释**: 解释复杂逻辑
- **中文注释**: 项目主要使用中文注释

## 配置管理
- **配置文件**: 使用 JSON 格式存储在 `Resource/config.json`
- **环境变量**: 用于运行时配置（如 `QT_SCALE_FACTOR`）
- **默认值**: 提供合理的默认配置

## 国际化
- **多语言支持**: 使用 `@with_language` 装饰器
- **文本包装**: 使用 `t()` 函数包装需要翻译的字符串
- **本地化文件**: 存储在 `Resource/Localization/` 目录

## 架构模式
- **事件驱动**: 使用 EventManager 进行组件间通信
- **插件架构**: 支持动态加载插件
- **缓存系统**: 实现翻译结果缓存
- **多线程**: 支持并行处理提高效率