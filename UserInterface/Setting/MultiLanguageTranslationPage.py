from PyQt5.QtWidgets import QFrame, QVBoxLayout, QGroupBox, QHBoxLayout
from qfluentwidgets import CheckBox, StrongBodyLabel, InfoBar, InfoBarPosition, Action, FluentIcon

from Base.Base import Base
from Widget.SwitchButtonCard import SwitchButtonCard
from Widget.CommandBarCard import CommandBarCard
from UserInterface import AppFluentWindow


class MultiLanguageTranslationPage(QFrame, Base):
    def __init__(self, text: str, window: AppFluentWindow) -> None:
        super().__init__(window)
        self.setObjectName(text.replace(" ", "-"))
        self.window = window

        # 默认配置
        self.default = {
            "multi_language_translation_switch": False,
            "selected_languages": []
        }

        # 载入配置文件
        config = self.load_config_from_default()

        # 设置主容器
        self.container = QVBoxLayout(self)
        self.container.setSpacing(8)
        self.container.setContentsMargins(24, 24, 24, 24)  # 左、上、右、下

        # 添加控件
        self.add_widget_head(self.container, config, window)
        self.add_widget_body(self.container, config, window)
        self.add_widget_description(self.container)

    # 头部
    def add_widget_head(self, parent: QVBoxLayout, config: dict, window: AppFluentWindow) -> None:
        def init(widget: SwitchButtonCard) -> None:
            widget.set_checked(config.get("multi_language_translation_switch", False))

        def checked_changed(widget: SwitchButtonCard, checked: bool) -> None:
            config = self.load_config()
            config["multi_language_translation_switch"] = checked
            self.save_config(config)

            # 如果关闭了多语言翻译，清空选中的语言
            if not checked:
                config["selected_languages"] = []
                self.save_config(config)
                # 更新复选框状态
                for checkbox in self.checkboxes.values():
                    checkbox.setChecked(False)

        parent.addWidget(
            SwitchButtonCard(
                self.tra("多语言批量翻译"),
                self.tra("启用此功能后，可以选择多个目标语言，一次性将原文翻译成所有选定的语言"),
                init=init,
                checked_changed=checked_changed,
            )
        )

    # 主体
    def add_widget_body(self, parent: QVBoxLayout, config: dict, window: AppFluentWindow) -> None:
        # 创建语言选择组
        language_group = QGroupBox(self.tra("选择目标语言"))
        language_layout = QVBoxLayout()

        # 添加操作按钮
        self.command_bar_card = CommandBarCard()
        self.add_command_bar_action_select_all(self.command_bar_card)
        self.command_bar_card.add_separator()
        self.add_command_bar_action_deselect_all(self.command_bar_card)
        language_layout.addWidget(self.command_bar_card)

        # 定义语言与值的配对列表（显示文本, 存储值）
        self.language_pairs = [
            (self.tra("简中"), "chinese_simplified"),
            (self.tra("繁中"), "chinese_traditional"),
            (self.tra("英语"), "english"),
            (self.tra("日语"), "japanese"),
            (self.tra("韩语"), "korean"),
            (self.tra("俄语"), "russian"),
            (self.tra("德语"), "german"),
            (self.tra("法语"), "french"),
            (self.tra("西班牙语"), "spanish"),
        ]

        # 创建复选框并添加到布局中
        self.checkboxes = {}
        selected_languages = config.get("selected_languages", [])

        for display, value in self.language_pairs:
            checkbox = CheckBox(display)
            checkbox.setChecked(value in selected_languages)
            checkbox.stateChanged.connect(self.update_selected_languages)
            language_layout.addWidget(checkbox)
            self.checkboxes[value] = checkbox

        language_group.setLayout(language_layout)
        parent.addWidget(language_group)

    # 全选按钮
    def add_command_bar_action_select_all(self, parent: CommandBarCard) -> None:
        def triggered() -> None:
            config = self.load_config()
            # 只有在多语言翻译开关打开时才执行全选操作
            if config.get("multi_language_translation_switch", False):
                # 设置所有复选框为选中状态
                for checkbox in self.checkboxes.values():
                    checkbox.setChecked(True)
                # 更新选中的语言列表
                self.update_selected_languages()
            else:
                # 如果多语言翻译开关关闭，显示提示
                InfoBar.warning(
                    title="",
                    content=self.tra("请先启用多语言批量翻译功能"),
                    parent=self,
                    duration=3000,
                    position=InfoBarPosition.TOP
                )

        parent.add_action(
            Action(FluentIcon.ADD_TO, self.tra("全选"), parent, triggered=triggered)
        )

    # 全不选按钮
    def add_command_bar_action_deselect_all(self, parent: CommandBarCard) -> None:
        def triggered() -> None:
            config = self.load_config()
            # 只有在多语言翻译开关打开时才执行全不选操作
            if config.get("multi_language_translation_switch", False):
                # 设置所有复选框为未选中状态
                for checkbox in self.checkboxes.values():
                    checkbox.setChecked(False)
                # 更新选中的语言列表
                self.update_selected_languages()
            else:
                # 如果多语言翻译开关关闭，显示提示
                InfoBar.warning(
                    title="",
                    content=self.tra("请先启用多语言批量翻译功能"),
                    parent=self,
                    duration=3000,
                    position=InfoBarPosition.TOP
                )

        parent.add_action(
            Action(FluentIcon.REMOVE_FROM, self.tra("全不选"), parent, triggered=triggered)
        )

    # 添加说明文本
    def add_widget_description(self, parent: QVBoxLayout) -> None:
        description = StrongBodyLabel(self.tra("选择完目标语言后，请返回「开始翻译」页面点击开始按钮进行翻译"))
        description.setWordWrap(True)
        parent.addWidget(description)

        # 添加填充
        parent.addStretch(1)

    # 更新选中的语言列表
    def update_selected_languages(self) -> None:
        config = self.load_config()

        # 只有在多语言翻译开关打开时才更新选中的语言
        if config.get("multi_language_translation_switch", False):
            selected_languages = self.get_selected_languages()
            config["selected_languages"] = selected_languages
            self.save_config(config)

            # 如果没有选择任何语言，显示提示
            if not selected_languages:
                InfoBar.warning(
                    title="",
                    content=self.tra("请至少选择一种目标语言"),
                    parent=self,
                    duration=3000,
                    position=InfoBarPosition.TOP
                )
        else:
            # 如果多语言翻译开关关闭，但用户尝试选择语言，显示提示
            for checkbox in self.checkboxes.values():
                checkbox.setChecked(False)

            InfoBar.warning(
                title="",
                content=self.tra("请先启用多语言批量翻译功能"),
                parent=self,
                duration=3000,
                position=InfoBarPosition.TOP
            )

    # 获取选中的语言列表
    def get_selected_languages(self) -> list:
        selected = []
        for value, checkbox in self.checkboxes.items():
            if checkbox.isChecked():
                selected.append(value)
        return selected

    # 从默认配置加载
    def load_config_from_default(self) -> dict:
        config = self.load_config()

        # 确保所有默认配置项存在
        for key, value in self.default.items():
            if key not in config:
                config[key] = value

        self.save_config(config)
        return config
