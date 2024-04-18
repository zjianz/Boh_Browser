import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QSizePolicy
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class Card_UI(QWidget):
    def __init__(self, card_image_path, card_id, parent=None):
        super().__init__(parent)

        # 初始化布局
        self.init_layout(card_image_path, card_id)

    def init_layout(self, card_image_path, card_id):
        # 创建网格布局
        grid_layout = QGridLayout(self)

        # 设置卡图
        self.card_image = QLabel(self)
        pixmap = QPixmap(card_image_path)
        self.card_image.setPixmap(pixmap.scaled(self.width(), int(self.height() * 0.3), Qt.AspectRatioMode.KeepAspectRatio))
        grid_layout.addWidget(self.card_image, 0, 0, 1, 3)  # 占据第一行，跨越三列

        # 设置ID标签
        self.card_id_label = QLabel(f"ID: {card_id}", self)
        grid_layout.addWidget(self.card_id_label, 1, 0, 1, 1)  # 占据第二行第一列

        # 预留空间用于标签栏（由子类实现）
        self.tag_bar_placeholder = QWidget(self)
        grid_layout.addWidget(self.tag_bar_placeholder, 1, 1, 1, 2)  # 占据第二行第二列和第三列

    def set_tag_bar(self, widget):
        """由子类调用以设置标签栏"""
        grid_layout = self.layout()
        # 获取当前布局中tag_bar_placeholder的位置
        row, col, row_span, col_span = grid_layout.getItemPosition(self.tag_bar_placeholder)
        # 移除旧的tag_bar_placeholder
        grid_layout.removeWidget(self.tag_bar_placeholder)
        # 添加新的widget到对应的位置
        grid_layout.addWidget(widget, row, col, row_span, col_span)

# 示例使用
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 假设的卡片图片路径和ID
    card_image_path = r"C:/Users\12615\Pictures\Unpacking\20240107_0001.png"
    card_id = 123

    # 创建 Card_UI 实例
    card_ui = Card_UI(card_image_path, card_id)
    card_ui.show()

    # 假设的标签栏部件
    tag_widget = QLabel("Tags: Example, Tag, Another")
    tag_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    # 设置标签栏
    card_ui.set_tag_bar(tag_widget)

    sys.exit(app.exec())