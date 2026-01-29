import time
import os
import math

def clear_console():
    """清空控制台"""
    os.system('cls' if os.name == 'nt' else 'clear')

def heart_shape(t, scale=10):
    """生成爱心形状的坐标"""
    # 爱心参数方程
    x = 16 * math.sin(t)**3
    y = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
    
    # 缩放和调整位置
    x = int(x * scale / 16 + 40)
    y = int(-y * scale / 16 + 15)  # 负号是为了翻转
    
    return x, y

def draw_heart_frame(scale, beat_factor=1.0):
    """绘制一帧爱心"""
    width, height = 80, 30
    frame = [[' ' for _ in range(width)] for _ in range(height)]
    
    # 绘制爱心
    for i in range(0, 628, 2):  # 0 到 2π，步长0.02
        t = i / 100
        x, y = heart_shape(t, scale * beat_factor)
        
        if 0 <= x < width and 0 <= y < height:
            # 根据位置选择不同字符
            dist_from_center = abs(math.atan2(y-15, x-40)) / math.pi
            if dist_from_center < 0.2:
                frame[y][x] = '█'
            elif dist_from_center < 0.4:
                frame[y][x] = '▓'
            elif dist_from_center < 0.6:
                frame[y][x] = '▒'
            else:
                frame[y][x] = '░'
    
    # 添加文字
    message = "I ♥ YOU"
    start_x = (width - len(message)) // 2
    for i, char in enumerate(message):
        frame[height-3][start_x + i] = char
    
    return frame

def animate_console_heart():
    """控制台爱心动画"""
    colors = ['\033[91m', '\033[93m', '\033[95m', '\033[96m']  # 红、黄、紫、青
    
    try:
        frame_count = 0
        while True:
            clear_console()
            
            # 计算跳动效果
            beat = 1 + 0.2 * math.sin(frame_count * 0.2)
            
            # 生成并显示帧
            frame = draw_heart_frame(10, beat)
            
            # 添加颜色
            color = colors[frame_count % len(colors)]
            reset = '\033[0m'
            
            print(f"{color}")
            print(" " * 15 + "❤️ 动态爱心 ❤️")
            print()
            
            for row in frame:
                print(''.join(row))
            
            print(f"{reset}")
            print("\n" + " " * 25 + "按 Ctrl+C 退出")
            
            frame_count += 1
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        clear_console()
        print("\n" + " " * 20 + "❤️ 再见！ ❤️\n")

# 运行控制台版本
if __name__ == "__main__":
    print("选择爱心版本：")
    print("1. 图形界面版本 (需要matplotlib)")
    print("2. 控制台版本 (纯Python)")
    
    choice = input("请输入选择 (1 或 2): ")
    
    if choice == "1":
        try:
            import matplotlib
            # 运行第一个版本
            exec(open(__file__).read())
        except ImportError:
            print("需要安装matplotlib库，请运行: pip install matplotlib")
    elif choice == "2":
        animate_console_heart()