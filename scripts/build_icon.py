from pathlib import Path
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "campusmate.svg"
ICONSET = ROOT / "build" / "CampusMate.iconset"


def main():
    app = QGuiApplication(sys.argv)
    renderer = QSvgRenderer(str(SOURCE))
    if not renderer.isValid():
        raise RuntimeError(f"Could not load app icon: {SOURCE}")

    ICONSET.mkdir(parents=True, exist_ok=True)
    sizes = [
        ("icon_16x16.png", 16),
        ("icon_16x16@2x.png", 32),
        ("icon_32x32.png", 32),
        ("icon_32x32@2x.png", 64),
        ("icon_128x128.png", 128),
        ("icon_128x128@2x.png", 256),
        ("icon_256x256.png", 256),
        ("icon_256x256@2x.png", 512),
        ("icon_512x512.png", 512),
        ("icon_512x512@2x.png", 1024),
    ]

    for filename, size in sizes:
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        renderer.render(painter)
        painter.end()
        if not pixmap.save(str(ICONSET / filename), "PNG"):
            raise RuntimeError(f"Could not write {filename}")

    app.quit()


if __name__ == "__main__":
    main()
