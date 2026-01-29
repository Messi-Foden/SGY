import os, time, math, random

# ===== 核心配置 =====
W, H = 80, 40  # 终端尺寸
CHARS = " ·░▒▓█❤️💖💗✨"
FPS = 20

# ===== 粒子系统 =====
class Particle:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-0.5, 0.5)
        self.life = 1.0
        self.trail = []
    
    def update(self, dt):
        self.vx *= 0.98; self.vy *= 0.98
        self.x += self.vx; self.y += self.vy
        self.life -= dt * 0.1
        
        # 吸引到中心
        dist = (self.x**2 + self.y**2)**0.5
        if dist > 0.1:
            self.vx -= self.x * 0.01 / dist
            self.vy -= self.y * 0.01 / dist
        
        self.trail.append((self.x, self.y))
        if len(self.trail) > 15:
            self.trail.pop(0)
    
    @property
    def char(self):
        if self.life > 0.7: return '❤️'
        elif self.life > 0.4: return '💖'
        elif self.life > 0.2: return '💗'
        else: return '✨'

# ===== 爱心生成 =====
def heart_func(t, beat=1.0):
    """爱心参数方程"""
    x = 16 * math.sin(t)**3
    y = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
    scale = 10 * (1 + 0.2 * math.sin(time.time() * 2))
    return x * scale * beat, y * scale * beat

def generate_heart(particles, mode="beat"):
    """生成爱心粒子"""
    new_particles = []
    
    for i in range(0, 628, 5):
        t = i / 100
        beat = 1 + 0.1 * math.sin(time.time() * 3)
        
        if mode == "spiral":
            # 螺旋效果
            r = t * 0.5
            a = t * 5 + time.time()
            x = math.cos(a) * r
            y = math.sin(a) * r
            base_x, base_y = heart_func(t, 1)
            x += base_x * 0.5
            y += base_y * 0.5
        else:
            # 跳动效果
            x, y = heart_func(t, beat)
            # 添加扰动
            x += random.uniform(-0.5, 0.5)
            y += random.uniform(-0.5, 0.5)
        
        p = Particle(x, y)
        new_particles.append(p)
    
    return particles + new_particles

# ===== 渲染引擎 =====
class Renderer:
    def __init__(self):
        self.buffer = [[' ' for _ in range(W)] for _ in range(H)]
    
    def clear(self):
        self.buffer = [[' ' for _ in range(W)] for _ in range(H)]
    
    def plot(self, x, y, char):
        ix = int(x * 0.6 + W//2)
        iy = int(-y * 0.6 + H//2)
        if 0 <= ix < W and 0 <= iy < H:
            self.buffer[iy][ix] = char
    
    def draw_particle(self, p):
        # 绘制轨迹
        for i, (tx, ty) in enumerate(p.trail):
            self.plot(tx, ty, '·' if i%2 else '°')
        # 绘制粒子
        self.plot(p.x, p.y, p.char)
    
    def render(self):
        return '\n'.join(''.join(row) for row in self.buffer)

# ===== 主动画循环 =====
def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[95m❤️ 动态爱心 ❤️\033[0m")
    print("按 Ctrl+C 退出\n")
    
    renderer = Renderer()
    particles = []
    mode = "beat"
    last_switch = time.time()
    
    try:
        while True:
            renderer.clear()
            
            # 每5秒切换模式
            if time.time() - last_switch > 5:
                mode = "spiral" if mode == "beat" else "beat"
                last_switch = time.time()
                particles = []
            
            # 生成新粒子
            particles = generate_heart(particles, mode)
            
            # 更新并绘制粒子
            alive = []
            for p in particles:
                p.update(0.05)
                if p.life > 0.1:
                    renderer.draw_particle(p)
                    alive.append(p)
            
            particles = alive[:150]  # 限制数量
            
            # 显示
            output = renderer.render()
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\033[95m{'❤️ 动态爱心 ❤️':^80}\033[0m")
            print(f"\033[92m模式: {mode.upper():^10} | 粒子数: {len(particles):^10}\033[0m\n")
            print(output)
            print(f"\n\033[93m{'按 Ctrl+C 退出':^80}\033[0m")
            
            time.sleep(1/FPS)
            
    except KeyboardInterrupt:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" * 5)
        print(" " * 30 + "\033[91m❤️ 再见！ ❤️\033[0m")
        print("\n" * 5)

if __name__ == "__main__":
    main()