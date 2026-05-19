"""
Unit 7.3: QNetworkAccessManager —— 网络请求
学习目标:
  1. 掌握 QNetworkAccessManager 的异步 HTTP 请求
  2. 学会 get(), post() 方法的使用
  3. 理解 QNetworkReply 和 finished 信号
  4. 学会处理响应: QJsonDocument 解析 JSON 数据
  5. 理解 QNetworkRequest 的配置 (header, URL 等)

关键概念:
  - QNetworkAccessManager: 管理网络请求的中央对象
  - QNetworkRequest: 封装 URL 和请求头
  - QNetworkReply: 表示请求的响应，提供数据流读取
  - 所有网络操作都是异步的 (不阻塞 UI)
  - finished(reply) 信号: 请求完成时触发

注意:
  - 本例使用 httpbin.org 作为测试 API (无需 API Key)
  - 网络请求可能因网络问题失败，需处理错误

API 参考:
  https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtnetwork/qnetworkaccessmanager.html
"""
import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QGroupBox,
    QPushButton, QLabel, QLineEdit, QTextEdit
)
from PyQt6.QtCore import Qt, QUrl, QByteArray
from PyQt6.QtNetwork import (
    QNetworkAccessManager, QNetworkRequest, QNetworkReply
)


class NetworkDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QNetworkAccessManager 网络请求演示")
        self.resize(600, 550)

        central = QWidget()
        main_layout = QVBoxLayout(central)

        # --- GET 请求 ---
        get_group = QGroupBox("1. GET 请求 (获取 JSON)")
        get_layout = QHBoxLayout(get_group)

        get_btn = QPushButton("GET /get")
        get_btn.clicked.connect(self._do_get_request)
        get_layout.addWidget(get_btn)

        get_with_params_btn = QPushButton("GET with 参数")
        get_with_params_btn.clicked.connect(self._do_get_with_params)
        get_layout.addWidget(get_with_params_btn)

        main_layout.addWidget(get_group)

        # --- POST 请求 ---
        post_group = QGroupBox("2. POST 请求 (发送 JSON)")
        post_layout = QHBoxLayout(post_group)

        self.post_data_edit = QLineEdit()
        self.post_data_edit.setPlaceholderText("输入要发送的数据...")
        post_layout.addWidget(self.post_data_edit)

        post_btn = QPushButton("POST /post")
        post_btn.clicked.connect(self._do_post_request)
        post_layout.addWidget(post_btn)

        main_layout.addWidget(post_group)

        # --- 下载文件 ---
        download_group = QGroupBox("3. 下载文件 (自定义 URL)")
        download_layout = QHBoxLayout(download_group)

        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText("输入要下载的 URL...")
        download_layout.addWidget(self.url_edit)

        download_btn = QPushButton("下载")
        download_btn.clicked.connect(self._do_download)
        download_layout.addWidget(download_btn)

        main_layout.addWidget(download_group)

        # --- 响应区域 ---
        resp_group = QGroupBox("请求 / 响应")
        resp_layout = QVBoxLayout(resp_group)

        self.status_label = QLabel("就绪 (未发起请求)")
        resp_layout.addWidget(self.status_label)

        self.resp_text = QTextEdit()
        self.resp_text.setReadOnly(True)
        self.resp_text.setPlaceholderText("响应数据将显示在这里...")
        resp_layout.addWidget(self.resp_text)

        clear_btn = QPushButton("清空响应")
        clear_btn.clicked.connect(self.resp_text.clear)
        resp_layout.addWidget(clear_btn)

        main_layout.addWidget(resp_group)

        self.setCentralWidget(central)
        """
        ### QNetworkAccessManager 是什么？
        它是 Qt 网络模块的核心类，负责：

        - 发送 HTTP 请求（ get() 、 post() 、 put() 等）
        - 管理所有网络操作的生命周期
        - 异步收发数据 ，内部使用操作系统的网络栈，不阻塞 UI 线程

        一个 QNetworkAccessManager 可以同时管理多个并发请求，
        每个请求返回时都会触发 finished 信号，并携带对应的 QNetworkReply 对象。
        槽函数 _on_reply_finished 负责统一处理所有请求的响应数据
        """
        # 创建 QNetworkAccessManager (整个应用程序通常只需一个实例)
        # self 作为父对象传入，意味着当窗口销毁时，这个管理器也会被自动清理，避免内存泄漏
        self._manager = QNetworkAccessManager(self)
        # 将管理器的 finished 信号 连接到 _on_reply_finished 槽函数
        self._manager.finished.connect(self._on_reply_finished)

    def _do_get_request(self):
        """简单的 GET 请求"""
        url = QUrl("https://httpbin.org/get")
        # 用该 URL 构建一个 HTTP 请求对象， 
        # QNetworkRequest 相当于"信封"，承载 URL、Header 等请求信息
        request = QNetworkRequest(url)
        # 设置请求头 Content-Type: application/json ，
        # 告诉服务器"我期望的响应格式是 JSON"
        request.setHeader(
            QNetworkRequest.KnownHeaders.ContentTypeHeader,
            "application/json"
        )
        # 通过 QNetworkAccessManager 发起 GET 请求 。
        # 这是 异步 的，不会阻塞 UI 线程，响应通过信号/槽机制返回
        self._manager.get(request)
        self.status_label.setText("正在 GET /get ...")

    def _do_get_with_params(self):
        """带参数的 GET 请求"""
        url = QUrl("https://httpbin.org/get")
        from PyQt6.QtCore import QUrlQuery
        query = QUrlQuery()
        query.addQueryItem("name", "PyQt6")
        query.addQueryItem("version", "6.0")
        url.setQuery(query)

        request = QNetworkRequest(url)
        self._manager.get(request)
        self.status_label.setText("正在 GET (with params) ...")

    def _do_post_request(self):
        """POST 请求发送 JSON 数据"""
        url = QUrl("https://httpbin.org/post")
        request = QNetworkRequest(url)
        request.setHeader(
            QNetworkRequest.KnownHeaders.ContentTypeHeader,
            "application/json"
        )

        data_text = self.post_data_edit.text().strip() or "测试数据"
        payload = QByteArray(
            json.dumps({"message": data_text, "source": "PyQt6"}).encode("utf-8")
        )

        # post(request, data): 发送 POST 请求
        self._manager.post(request, payload)
        self.status_label.setText(f"正在 POST '{data_text}' ...")

    def _do_download(self):
        """下载文件 (自定义 URL)"""
        raw_url = self.url_edit.text().strip()
        if not raw_url:
            raw_url = "https://httpbin.org/json"

        url = QUrl(raw_url)
        if not url.isValid():
            self.status_label.setText(f"无效的 URL: {raw_url}")
            return

        request = QNetworkRequest(url)
        self._manager.get(request)
        self.status_label.setText(f"正在下载 {raw_url} ...")

    def _on_reply_finished(self, reply: QNetworkReply):
        """所有网络请求完成后的回调"""
        # error() 检查是否有错误
        if reply.error() != QNetworkReply.NetworkError.NoError:
            error_msg = reply.errorString()
            self.resp_text.setPlainText(f"网络错误: {error_msg}")
            self.status_label.setText(f"请求失败: {error_msg}")
            reply.deleteLater()
            return

        # 读取响应体
        raw_data = reply.readAll().data()
        try:
            text = raw_data.decode("utf-8")
        except UnicodeDecodeError:
            self.resp_text.setPlainText(f"[二进制数据] {len(raw_data)} bytes")
            self.status_label.setText(f"下载完成 ({len(raw_data)} bytes)")
            reply.deleteLater()
            return

        # 尝试格式化 JSON
        try:
            parsed = json.loads(text)
            # 不将非 ASCII 字符转义为 \uXXXX 。
            # 例如中文 "你好" 会直接保留，而不是变成 "\u4f60\u597d"
            formatted = json.dumps(parsed, ensure_ascii=False, indent=2)
        except json.JSONDecodeError:
            formatted = text

        # 截断过长的响应
        if len(formatted) > 5000:
            formatted = formatted[:5000] + "\n... (已截断)"

        self.resp_text.setPlainText(formatted)


        """
        获取 HTTP 状态码和 URL
        QNetworkReply 中的 HTTP 相关元数据（状态码、状态文本、重定向目标等）
        不是通过直接属性访问的，而是存放在一个 通用的键值存储 中，通过 attribute(key) 来获取。
        
        HttpStatusCodeAttribute      HTTP 状态码  如 200 、 404 、 500 
        HttpReasonPhraseAttribute    状态描述文本  如 "OK" 、 "Not Found" 
        RedirectionTargetAttribute   重定向目标 URL
        """
        status = reply.attribute(
            QNetworkRequest.Attribute.HttpStatusCodeAttribute
        )
        url = reply.url().toString()
        self.status_label.setText(f"完成 | HTTP {status} | {url}")

        # 清理 QNetworkReply
        reply.deleteLater()


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = NetworkDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
