import http.server
import socketserver
import urllib.parse
import json
import traceback

# 这是一个模拟的 bili_ticket_gt_python 模块，用于在没有安装该库时进行测试。
# 如果您已经安装了该库，可以删除或注释掉这部分。
try:
    import bili_ticket_gt_python
except ImportError:
    print("警告: 'bili_ticket_gt_python' 库未找到。")
    print("将使用一个模拟库进行测试。请使用 'pip install bili-ticket-gt-python' 进行安装。")


    class MockClickPy:
        def simple_match(self, gt, challenge):
            print(f"模拟识别: gt={gt}, challenge={challenge}")
            # 模拟返回一个 validate 字符串
            return {"validate": "mock_validate_string", "seccode": "mock_seccode"}


    class MockBiliTicket:
        ClickPy = MockClickPy


    bili_ticket_gt_python = MockBiliTicket()


class GeetestHandler(http.server.BaseHTTPRequestHandler):
    """
    处理 /geetest 请求的处理器
    """

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)

        # 检查请求路径是否为 /geetest
        if parsed_path.path == '/geetest':
            try:
                # 解析 URL 中的查询参数
                query_params = urllib.parse.parse_qs(parsed_path.query)
                gt = query_params.get('gt', [None])[0]
                challenge = query_params.get('challenge', [None])[0]

                # 检查参数是否存在
                if not gt or not challenge:
                    self._send_response(400, {
                        "status": "error",
                        "message": "缺少 'gt' 或 'challenge' 参数"
                    })
                    return

                # --- 调用核心识别代码 ---
                click = bili_ticket_gt_python.ClickPy()
                validate_result = click.simple_match(gt, challenge)
                # -------------------------

                print(f"识别成功: {validate_result}")
                self._send_response(200, {
                    "code":"0",
                    "status": "success",
                    "data": {"validate":validate_result
                             }
                })

            except Exception as e:
                print("识别失败")
                traceback.print_exc()  # 打印详细的错误堆栈信息
                self._send_response(500, {
                    "code":"503",
                    "status": "error",
                    "message": "识别过程中发生内部错误",
                    "detail": str(e)
                })
        else:
            # 如果路径不是 /geetest，返回 404
            self._send_response(404, {
                    "code":"503","status": "error", "message": "Not Found"})

    def _send_response(self, status_code, content):
        """统一发送响应的辅助函数"""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(content, ensure_ascii=False).encode('utf-8'))

    def log_message(self, format, *args):
        """覆盖默认的日志输出，使其更简洁"""
        return


def run_server(port=59590):
    """
    启动服务器
    """
    with socketserver.TCPServer(("", port), GeetestHandler) as httpd:
        print(f"✅ 服务器已启动，正在监听端口: {port}")
        print(f"请向以下地址发送 GET 请求来进行验证码识别:")
        print(f"   http://localhost:{port}/geetest?gt=<gt_value>&challenge=<challenge_value>")
        httpd.serve_forever()


if __name__ == "__main__":
    run_server()
