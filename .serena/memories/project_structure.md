# AiNiee 项目结构

## 根目录文件
- **AiNiee.py**: 主入口文件，启动 GUI 应用
- **requirements.txt**: Python 依赖列表
- **build_exe.bat**: Windows 打包脚本
- **cv2.py**: OpenCV 相关模块

## 核心目录结构

### Base/
基础架构模块
- **Base.py**: 基础类定义（Event, Status, Base）
- **EventManager.py**: 事件管理器
- **PluginManager.py**: 插件管理器

### ModuleFolders/
核心功能模块
- **Cache/**: 缓存管理系统
- **FileReader/**: 文件读取器（支持多种格式）
- **FileOutputer/**: 文件输出器（支持多种格式）
- **LLMRequester/**: LLM API 请求器（支持多个平台）
- **PromptBuilder/**: 提示词构建器
- **Translator/**: 翻译核心逻辑
- **RequestLimiter/**: 请求限制器
- **RequestTester/**: 请求测试器
- **ResponseChecker/**: 响应检查器
- **ResponseExtractor/**: 响应提取器
- **TextProcessor/**: 文本处理器

### UserInterface/
GUI 用户界面
- **AppFluentWindow.py**: 主窗口
- **Setting/**: 设置页面
- **Platform/**: 平台配置
- **Table/**: 表格组件
- **Monitoring/**: 监控界面

### DRWidget/
自定义 UI 组件
- 各种提取卡片组件
- 对话片段卡片
- 测试断点卡片

### PluginScripts/
插件脚本目录

### Resource/
资源文件
- 配置文件
- 本地化文件
- 图标和图片

### Tools/
工具脚本
- **pyinstall.py**: PyInstaller 打包配置

### StevExtraction/
文本提取工具

### Widget/
通用 UI 组件