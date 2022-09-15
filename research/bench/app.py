from ui.ui_web import ViewUI
from benchmark.queue_manager import QueueManager


def on_click():
    queue = QueueManager()
    queue.run()


if __name__ == '__main__':
    ui = ViewUI()
    ui.draw(on_click)
