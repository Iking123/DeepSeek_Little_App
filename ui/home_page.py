import os
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QPushButton,
    QLabel,
    QSizePolicy,
    QHBoxLayout,
    QFrame,
    QGraphicsDropShadowEffect,
)
from PyQt5.QtGui import QFont, QColor, QTransform
from PyQt5.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve, pyqtProperty


class HomePage(QWidget):
    """主页面，显示四个功能方块和中央设置按钮"""

    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        # 主布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        self.setStyleSheet(
            "background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f5f7fa, stop:1 #e4e7ed);"
        )

        # 标题区域
        title_layout = QVBoxLayout()
        title_label = QLabel("DeepSeek 多功能小应用")
        title_label.setFont(QFont("Microsoft YaHei", 36, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2C3E50; margin-bottom: 10px;")

        subtitle_label = QLabel("Created by Iking")
        subtitle_label.setFont(QFont("Microsoft YaHei", 16))
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #7f8c8d; margin-bottom: 40px;")

        empty_space = QWidget()

        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        title_layout.addWidget(empty_space)
        layout.addLayout(title_layout)

        self.resources_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),  # 向上退两级到项目根目录
            "resources",
            "images",
        )

        # 功能方块网格布局
        grid_layout = QGridLayout()
        grid_layout.setSpacing(30)
        grid_layout.setContentsMargins(50, 0, 50, 0)

        # 创建四个功能按钮
        self.chat_btn = self.create_function_button("聊天", "#3498DB")
        self.game_btn = self.create_function_button("小游戏", "#27ae60")
        self.interactive_btn = self.create_function_button("交互小说", "#f39c12")
        self.creative_btn = self.create_function_button("创意写作", "#9b59b6")

        # 设置按钮
        self.settings_btn = self.create_circle_button()
        grid_layout.addWidget(self.settings_btn, 1, 2)

        grid_layout.addWidget(self.chat_btn, 0, 0)
        grid_layout.addWidget(self.game_btn, 0, 1)
        grid_layout.addWidget(self.interactive_btn, 1, 0)
        grid_layout.addWidget(self.creative_btn, 1, 1)
        layout.addLayout(grid_layout)
        layout.addStretch(1)

        # 连接信号
        self.chat_btn.clicked.connect(lambda: self.switch_to_page(1))
        self.game_btn.clicked.connect(lambda: self.switch_to_page(2))
        self.interactive_btn.clicked.connect(lambda: self.switch_to_page(3))
        self.creative_btn.clicked.connect(lambda: self.switch_to_page(4))
        self.settings_btn.clicked.connect(lambda: self.switch_to_page(5))

        # 设置动画效果
        self.setup_animations()

    def create_function_button(self, text, color):
        """创建带图标和优化样式的功能按钮"""
        button = QPushButton()
        button.setMinimumHeight(550)
        button.setFixedWidth(600)

        # 渐变色
        base_color = QColor(color)
        darker_color = base_color.darker(110)
        lighter_color = base_color.lighter(130)

        # 设置图片路径（根据按钮文字映射）
        img_map = {
            "聊天": "chat_bg.png",
            "小游戏": "game_bg.png",
            "交互小说": "interactive_bg.png",
            "创意写作": "creative_writing_bg.png",
        }
        img_path = os.path.join(self.resources_dir, img_map[text])

        # 使用绝对路径并转换路径分隔符
        abs_path = os.path.abspath(img_path).replace("\\", "/")

        button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {lighter_color.name()}, stop:1 {darker_color.name()});
                border-radius: 20px;
                color: white;
                text-align: center;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-image: url({abs_path}) 0 0 0 0 stretch stretch;
            }}
            QPushButton:hover {{
                border: 2px solid #FFFF00;
            }}
            QPushButton:pressed {{
                background-color: {darker_color.name()};
            }}
        """
        )

        # 添加阴影
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 60))
        button.setGraphicsEffect(shadow)

        # 保存阴影效果的引用，用于动画
        button.shadow_effect = shadow

        return button

    def create_circle_button(self):
        """创建带阴影的圆形按钮"""
        button = QPushButton()
        button.setFixedSize(240, 240)

        img_path = os.path.join(self.resources_dir, "settings_bg.png")
        abs_path = os.path.abspath(img_path).replace("\\", "/")

        button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: #F5F5F5;
                border-radius: 120px;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-image: url({abs_path}) 0 0 0 0 stretch stretch;
            }}
            QPushButton:hover {{
                background-color: #E4E4E4;
            }}
            QPushButton:pressed {{
                background-color: #E4E4E4;
            }}
        """
        )

        # 添加阴影
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 12)
        shadow.setColor(QColor(0, 0, 0, 60))
        button.setGraphicsEffect(shadow)

        # 保存阴影效果的引用，用于动画
        button.shadow_effect = shadow

        return button

    def switch_to_page(self, index):
        """切换到指定页面"""
        if self.main_window:
            self.main_window.switch_page(index)

    def setup_animations(self):
        """设置按钮动画效果"""
        # 功能按钮悬停动画
        for btn in [
            self.chat_btn,
            self.game_btn,
            self.interactive_btn,
            self.creative_btn,
        ]:
            btn.original_pos = btn.pos()

            # 悬停事件
            def enter(e, b=btn):
                # 上移5px
                pos_animation = QPropertyAnimation(b, b"pos")
                pos_animation.setDuration(200)
                pos_animation.setStartValue(b.original_pos)
                pos_animation.setEndValue(b.original_pos - QPoint(0, 5))
                pos_animation.setEasingCurve(QEasingCurve.OutBack)
                pos_animation.start()

                # 增加阴影效果
                b.shadow_effect.setBlurRadius(30)
                b.shadow_effect.setOffset(0, 12)
                b.shadow_effect.setColor(QColor(0, 0, 0, 200))

                # 改变边框颜色
                b.setStyleSheet(
                    b.styleSheet().replace(
                        "border: 2px solid rgba(255, 255, 255, 0.3);",
                        "border: 2px solid #FFFF00;",
                    )
                )

            # 离开事件
            def leave(e, b=btn):
                # 恢复位置
                pos_animation = QPropertyAnimation(b, b"pos")
                pos_animation.setDuration(200)
                pos_animation.setStartValue(b.pos())
                pos_animation.setEndValue(b.original_pos)
                pos_animation.setEasingCurve(QEasingCurve.OutBack)
                pos_animation.start()

                # 恢复阴影效果
                b.shadow_effect.setBlurRadius(15)
                b.shadow_effect.setOffset(0, 8)
                b.shadow_effect.setColor(QColor(0, 0, 0, 60))

                # 恢复边框颜色
                b.setStyleSheet(
                    b.styleSheet().replace(
                        "border: 2px solid #FFFF00;",
                        "border: 2px solid rgba(255, 255, 255, 0.3);",
                    )
                )

            btn.enterEvent = enter
            btn.leaveEvent = leave

        # 设置按钮悬停动画
        def settings_enter(e):
            # 增加阴影效果
            self.settings_btn.shadow_effect.setBlurRadius(30)
            self.settings_btn.shadow_effect.setOffset(0, 15)

        def settings_leave(e):
            # 恢复阴影效果
            self.settings_btn.shadow_effect.setBlurRadius(20)
            self.settings_btn.shadow_effect.setOffset(0, 10)

        self.settings_btn.enterEvent = settings_enter
        self.settings_btn.leaveEvent = settings_leave
