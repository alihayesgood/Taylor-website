import sys, json, os, random
from datetime import date
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

# --- 2026 丙午马年 · 顶级喜庆色谱 ---
THEME = {
    "red_silk": "#B30000",      # 深红绸缎
    "gold_leaf": "#FFD700",     # 鎏金
    "paper_yellow": "#FFF3E0",  # 宣纸黄（用于替代纯白，视觉更高级）
    "cinnabar": "#E63946",      # 朱砂红
    "lantern_glow": "#FF4D00"   # 灯笼火光
}

class FireworkParticle:
    def __init__(self, pos, color):
        self.pos = QPointF(pos)
        self.vel = QPointF(random.uniform(-10, 10), random.uniform(-20, -2))
        self.life = 255
        self.color = color

class TaskPanel(QFrame):
    """磁贴式任务面板：宣纸黄背景 + 朱砂红文字"""
    clicked = Signal(str, int, QPoint)

    def __init__(self, name, pts, count, icon):
        super().__init__()
        self.name, self.pts, self.count, self.icon = name, pts, count, icon
        self.setCursor(Qt.PointingHandCursor)
        self.setup_ui()

    def setup_ui(self):
        # 宣纸黄背景，配上大红边框
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {THEME['paper_yellow']};
                border: 4px double {THEME['gold_leaf']};
                border-radius: 5px;
            }}
            QFrame:hover {{
                background-color: #FFECB3;
                border-color: {THEME['lantern_glow']};
            }}
        """)
        layout = QVBoxLayout(self)
        
        # 标题行
        title_lay = QHBoxLayout()
        icon_lbl = QLabel(self.icon)
        icon_lbl.setStyleSheet("font-size: 28px; border:none; background:transparent;")
        name_lbl = QLabel(self.name)
        name_lbl.setStyleSheet(f"color: {THEME['red_silk']}; font-size: 20px; font-weight: 900; border:none; background:transparent;")
        title_lay.addWidget(icon_lbl)
        title_lay.addWidget(name_lbl)
        title_lay.addStretch()
        layout.addLayout(title_lay)

        # 数据行
        self.info_lbl = QLabel(f"精进次数：{self.count}")
        self.info_lbl.setStyleSheet(f"color: {THEME['cinnabar']}; font-size: 14px; font-weight: bold; border:none; background:transparent;")
        self.pts_lbl = QLabel(f"修行奖励：+{self.pts} EXP")
        self.pts_lbl.setStyleSheet(f"color: #5D4037; font-size: 13px; font-style: italic; border:none; background:transparent;")
        
        layout.addWidget(self.info_lbl)
        layout.addWidget(self.pts_lbl)

    def mousePressEvent(self, event):
        self.clicked.emit(self.name, self.pts, event.globalPos())

class LunarEvolutionEngine(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1000, 850)
        self.setWindowTitle("2026 丙午马年 · 数字化进化引擎")
        self.data = self.load_data()
        self.fireworks = []
        
        # 动画循环
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)
        
        self.init_ui()

    def load_data(self):
        path = "lunar_v5.json"
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f: return json.load(f)
        return {"score": 0, "streak": 0, "last_date": "", "day": 1, 
                "counts": {"Python":0, "练字":0, "剪辑":0, "运动":0, "复盘":0, "家务":0}}

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(15)

        # 1. 顶部：EXP 大看板
        header = QHBoxLayout()
        exp_box = QVBoxLayout()
        self.score_lbl = QLabel(str(self.data['score']))
        self.score_lbl.setStyleSheet(f"color: {THEME['gold_leaf']}; font-size: 85px; font-weight: 900; font-family: 'Arial Black';")
        exp_box.addWidget(QLabel("马年累计功勋 (EXP)", styleSheet="color: white; font-size: 16px; font-weight: bold;"))
        exp_box.addWidget(self.score_lbl)
        header.addLayout(exp_box)
        
        # 连击看板
        self.streak_lbl = QLabel(f"🔥 连续精进: {self.data['streak']} 天")
        self.streak_lbl.setStyleSheet(f"color: {THEME['gold_leaf']}; font-size: 24px; font-weight: bold; background: rgba(0,0,0,50); padding: 10px; border: 2px solid {THEME['gold_leaf']};")
        header.addStretch()
        header.addWidget(self.streak_lbl)
        main_layout.addLayout(header)

        # 2. 中部：全空间任务网格
        grid = QGridLayout()
        grid.setSpacing(10)
        missions = [
            ("Python 核心", 40, "🐍"), ("每日练字", 25, "✍️"), ("视频剪辑", 40, "✂️"),
            ("每日运动", 30, "🏃"), ("思维复盘", 20, "🧠"), ("勤务家务", 15, "🧹")
        ]
        self.panels = []
        for i, (m, p, icon) in enumerate(missions):
            panel = TaskPanel(m, p, self.data["counts"].get(m, 0), icon)
            panel.clicked.connect(self.handle_click)
            grid.addWidget(panel, i // 3, i % 3)
            self.panels.append(panel)
        main_layout.addLayout(grid)

        # 3. 底部：策马奔腾进度
        footer = QVBoxLayout()
        self.prog_lbl = QLabel(f"寒假位面探索：第 {self.data['day']} 天 / 25")
        self.prog_lbl.setStyleSheet(f"color: {THEME['gold_leaf']}; font-size: 20px; font-weight: 900;")
        footer.addWidget(self.prog_lbl)

        self.pbar = QProgressBar()
        self.pbar.setFixedHeight(40)
        self.pbar.setRange(0, 25)
        self.pbar.setValue(self.data['day'])
        self.pbar.setTextVisible(False)
        self.pbar.setStyleSheet(f"""
            QProgressBar {{ background: rgba(0,0,0,80); border: 3px solid {THEME['gold_leaf']}; border-radius: 20px; }}
            QProgressBar::chunk {{ background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FFD700, stop:1 #FF4D00); border-radius: 17px; }}
        """)
        footer.addWidget(self.pbar)
        main_layout.addLayout(footer)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 背景：高级红渐变
        grad = QLinearGradient(0, 0, 0, self.height())
        grad.setColorAt(0, QColor("#D31027"))
        grad.setColorAt(1, QColor("#8E0E00"))
        painter.fillRect(self.rect(), grad)

        # 绘制背景装饰：马年祥云、灯笼、鞭炮
        painter.setOpacity(0.1)
        painter.setFont(QFont("Arial", 200))
        painter.drawText(self.rect(), Qt.AlignCenter, "🐎")
        painter.setOpacity(1.0)
        
        # 绘制烟花
        for fw in self.fireworks:
            painter.setBrush(QColor(fw.color))
            painter.setOpacity(fw.life / 255.0)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(fw.pos, 5, 5)

    def handle_click(self, name, pts, gpos):
        # 产生彩色烟花
        lpos = self.mapFromGlobal(gpos)
        colors = ["#FFD700", "#FF4D00", "#FFFFFF", "#FFEB3B", "#FF5252"]
        for _ in range(35):
            self.fireworks.append(FireworkParticle(lpos, random.choice(colors)))

        # 逻辑处理
        self.data["score"] += pts
        self.data["counts"][name] = self.data["counts"].get(name, 0) + 1
        
        today = str(date.today())
        if self.data["last_date"] != today:
            self.data["day"] = min(25, self.data["day"] + 1)
            self.data["streak"] += 1
            self.data["last_date"] = today
        
        # 刷新界面
        self.score_lbl.setText(str(self.data['score']))
        self.pbar.setValue(self.data['day'])
        self.prog_lbl.setText(f"寒假位面探索：第 {self.data['day']} 天 / 25")
        for p in self.panels:
            if p.name == name: p.info_lbl.setText(f"精进次数：{self.data['counts'][name]}")
            
        with open("lunar_v5.json", "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4)

    def animate(self):
        for fw in self.fireworks[:]:
            fw.pos += fw.vel
            fw.vel += QPointF(0, 0.7) # 重力
            fw.life -= 8
            if fw.life <= 0: self.fireworks.remove(fw)
        self.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LunarEvolutionEngine()
    window.show()
    sys.exit(app.exec())