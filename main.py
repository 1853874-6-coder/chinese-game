import pygame
import sys
import asyncio

# ---------- 初始化 Pygame ----------
pygame.init()
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("生字大挑战 · 同音字｜理解｜书写")
clock = pygame.time.Clock()

# 颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (100, 180, 80)
LIGHT_GREEN = (160, 220, 130)
RED = (220, 80, 60)
BROWN = (100, 60, 30)
BG_COLOR = (254, 247, 224)      # 暖米色
BUTTON_COLOR = (242, 235, 210)
BUTTON_HOVER = (255, 239, 207)
TEXT_COLOR = (45, 62, 43)

# 字体
try:
    font_large = pygame.font.Font("NotoSansTC-Regular.otf", 28)
    font_medium = pygame.font.Font("NotoSansTC-Regular.otf", 22)
    font_small = pygame.font.Font("NotoSansTC-Regular.otf", 18)
except:
    font_large = pygame.font.SysFont("simhei", 28)
    font_medium = pygame.font.SysFont("simhei", 22)
    font_small = pygame.font.SysFont("simhei", 18)

# ---------- 题库 (与原 HTML 完全一致) ----------
QUESTIONS = [
    {"type": "📖 理解·运用", "text": "他一听到下课铃声，就______地收拾书包冲出教室。",
     "options": ["A. 停驻", "B. 忙不迭", "C. 比手画脚", "D. 动如脱兔"],
     "correct": 1, "explanation": "「忙不迭」形容急忙不停，最符合急忙收拾的情境。"},
    {"type": "📖 理解·运用", "text": "奥运百米决赛，选手们起跑瞬间个个______，爆发力惊人。",
     "options": ["A. 精神奕奕", "B. 动如脱兔", "C. 吼叫", "D. 探问"],
     "correct": 1, "explanation": "「动如脱兔」比喻动作十分敏捷，符合赛跑起跑。"},
    {"type": "📖 理解·运用", "text": "站在人生的______上，他犹豫了很久，最后选择了行医这条路。",
     "options": ["A. 裤管", "B. 丹田", "C. 岔路", "D. 开关"],
     "correct": 2, "explanation": "「岔路」指道路分岔的地方，也比喻人生抉择点。"},
    {"type": "📖 理解·运用", "text": "下列哪一个词语最适合形容「人很有活力、神采飞扬的样子」？",
     "options": ["A. 精神奕奕", "B. 比手画脚", "C. 中气", "D. 回响"],
     "correct": 0, "explanation": "「精神奕奕」指精神饱满、容光焕发。"},
    {"type": "✍️ 书写·识字", "text": "以下哪一个选项「有」错别字？",
     "options": ["A. 精神弈弈", "B. 比手画脚", "C. 裤管", "D. 攀谈"],
     "correct": 0, "explanation": "「精神奕奕」正确写法为「奕奕」，不是「弈棋」的弈。"},
    {"type": "✍️ 书写·识字", "text": "下列词语书写「完全正确」的是？",
     "options": ["A. 忙不叠", "B. 动如脱兔", "C. 停注", "D. 回向"],
     "correct": 1, "explanation": "「动如脱兔」正确；A应为「忙不迭」；C应为「停驻」；D应为「回响」。",},
    {"type": "✍️ 书写·识字", "text": "哪个词语含有「错字」？",
     "options": ["A. 回向", "B. 呼应", "C. 膝盖", "D. 吼叫"],
     "correct": 0, "explanation": "「回响」才是正确写法，「向」字义不符。"},
    {"type": "✍️ 书写·识字", "text": "「膝盖」的「膝」字，右边部分的正确写法（部件）是？",
     "options": ["A. 桼", "B. 漆", "C. 泰", "D. 水"],
     "correct": 0, "explanation": "「膝」从月（肉）部，右边是「桼」，读音qī，为本字部件。"},
    {"type": "🔊 同音字·辨识", "text": "「尼龙」的「尼」字，与下列哪一个字读音完全相同？",
     "options": ["A. 妮", "B. 离 (lí)", "C. 泥 (ní)", "D. 梨 (lí)"],
     "correct": 2, "explanation": "「尼」读 ní 第二声。选项C「泥」同样读 ní (泥土)，是完全同音字。"},
    {"type": "🔊 同音字·辨识", "text": "「丹田」的「丹」字，与下列哪一个字读音完全相同？",
     "options": ["A. 单 (简单)", "B. 担 (担忧)", "C. 耽 (耽误)", "D. 胆 (胆子)"],
     "correct": 0, "explanation": "「丹」读 dān，一声。「单」同样读 dān (简单)，为正确同音字。"},
    {"type": "🔊 同音字·辨识", "text": "「膝盖」的「膝」，下列哪一个选项是它的同音字？",
     "options": ["A. 西 (xī)", "B. 夕 (xī)", "C. 希 (xī)", "D. 吸 (xī)"],
     "correct": 3, "explanation": "「膝」读 xī，选项D「吸」是同音字。"},
    {"type": "🔊 同音字·辨识", "text": "「回响」的「响」字，与下列哪一个字读音完全相同（含声调）？",
     "options": ["A. 想 (xiǎng)", "B. 享 (xiǎng)", "C. 饷 (xiǎng)", "D. 向 (xiàng)"],
     "correct": 2, "explanation": "「响」读 xiǎng (三声)，「饷」同为三声 xiǎng，是同音字。注意「向」为四声。"}
]

# 游戏状态
current_q = 0
score = 0
answered = False
selected_opt = None
game_over = False
restart_btn_rect = None

# 选项按钮区域 (四个)
option_rects = []

def draw_text_center(surface, text, font, color, y_offset):
    """在屏幕水平居中绘制文本"""
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=(WIDTH//2, y_offset))
    surface.blit(text_surf, text_rect)

def wrap_text(text, font, max_width):
    """自动换行"""
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word + " "
    if current_line:
        lines.append(current_line)
    return lines

def draw_question():
    """绘制题目区域"""
    q = QUESTIONS[current_q]
    # 题型标签
    type_surf = font_small.render(q["type"], True, BROWN)
    screen.blit(type_surf, (50, 80))
    # 题目文本（自动换行）
    lines = wrap_text(q["text"], font_medium, WIDTH - 100)
    y = 130
    for line in lines:
        text_surf = font_medium.render(line, True, TEXT_COLOR)
        screen.blit(text_surf, (50, y))
        y += 35
    return y + 20  # 返回选项开始 y 坐标

def draw_options(start_y):
    """绘制选项按钮，返回按钮矩形列表"""
    q = QUESTIONS[current_q]
    option_rects.clear()
    btn_height = 55
    btn_margin = 15
    x = 80
    for i, opt in enumerate(q["options"]):
        # 确定按钮背景色
        color = BUTTON_COLOR
        if answered:
            if i == q["correct"]:
                color = LIGHT_GREEN
            elif i == selected_opt:
                color = RED
        # 绘制按钮
        rect = pygame.Rect(x, start_y + i*(btn_height+btn_margin), WIDTH-160, btn_height)
        pygame.draw.rect(screen, color, rect, border_radius=30)
        pygame.draw.rect(screen, (200, 180, 140), rect, 2, border_radius=30)
        # 选项文本
        text_surf = font_medium.render(opt, True, BLACK)
        screen.blit(text_surf, (rect.x + 20, rect.y + 12))
        option_rects.append(rect)
    return start_y + 4*(btn_height+btn_margin) + 10

def draw_feedback(y):
    """绘制反馈信息"""
    if not answered:
        return
    q = QUESTIONS[current_q]
    if selected_opt == q["correct"]:
        fb_text = f"✅ 答对了！ +10分  {q['explanation']}"
        color = (100, 180, 80)
    else:
        correct_letter = chr(65 + q["correct"])
        fb_text = f"❌ 答错了！ 正确答案是 {correct_letter}. {q['options'][q['correct']]}  {q['explanation']}"
        color = (200, 70, 60)
    lines = wrap_text(fb_text, font_small, WIDTH - 100)
    y_start = y
    for line in lines:
        text_surf = font_small.render(line, True, color)
        screen.blit(text_surf, (50, y_start))
        y_start += 25
    return y_start

def draw_score_progress():
    """绘制得分和进度"""
    total = len(QUESTIONS)
    score_surf = font_large.render(f"🏆 得分: {score}", True, (80, 60, 30))
    screen.blit(score_surf, (30, 20))
    prog_surf = font_large.render(f"📌 第 {current_q+1}/{total} 题", True, (80, 60, 30))
    screen.blit(prog_surf, (WIDTH - 200, 20))

def draw_restart_button():
    """绘制重新开始按钮（游戏结束时显示）"""
    global restart_btn_rect
    btn = pygame.Rect(WIDTH//2 - 100, HEIGHT - 100, 200, 50)
    pygame.draw.rect(screen, (100, 160, 80), btn, border_radius=30)
    pygame.draw.rect(screen, (60, 100, 40), btn, 2, border_radius=30)
    text = font_medium.render("重新开始", True, WHITE)
    screen.blit(text, (btn.x + 50, btn.y + 10))
    restart_btn_rect = btn

def draw_game_over():
    """游戏结束画面"""
    screen.fill(BG_COLOR)
    total_possible = len(QUESTIONS) * 10
    msg1 = f"🎉 游戏完成！ 🎉"
    msg2 = f"最终得分: {score} / {total_possible}"
    msg3 = "感谢三位专员与规则员协力！"
    draw_text_center(screen, msg1, font_large, (180, 100, 50), HEIGHT//2 - 80)
    draw_text_center(screen, msg2, font_large, (45, 62, 43), HEIGHT//2 - 20)
    draw_text_center(screen, msg3, font_medium, (100, 80, 40), HEIGHT//2 + 40)
    draw_restart_button()
    pygame.display.flip()

async def main():
    global current_q, score, answered, selected_opt, game_over
    running = True
    while running:
        screen.fill(BG_COLOR)
        
        if game_over:
            draw_game_over()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if restart_btn_rect and restart_btn_rect.collidepoint(event.pos):
                        # 重置游戏
                        current_q = 0
                        score = 0
                        answered = False
                        selected_opt = None
                        game_over = False
        else:
            # 正常游戏界面
            draw_score_progress()
            start_y = draw_question()
            opt_y = draw_options(start_y)
            feedback_y = draw_feedback(opt_y + 20)
            
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if not answered:
                        # 检测点击了哪个选项
                        for i, rect in enumerate(option_rects):
                            if rect.collidepoint(event.pos):
                                selected_opt = i
                                answered = True
                                if i == QUESTIONS[current_q]["correct"]:
                                    score += 10
                                break
                    else:
                        # 已答题，点击任意处进入下一题
                        if current_q + 1 < len(QUESTIONS):
                            current_q += 1
                            answered = False
                            selected_opt = None
                        else:
                            # 游戏结束
                            game_over = True
            
            # 可选：显示下一步提示
            if answered and not game_over:
                next_text = font_small.render("点击任意位置继续...", True, (150, 120, 70))
                screen.blit(next_text, (WIDTH - 180, HEIGHT - 40))
        
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)  # 必须，pygbag 异步要求
    
    pygame.quit()
    sys.exit()

# pygbag 入口
if __name__ == "__main__":
    asyncio.run(main())
