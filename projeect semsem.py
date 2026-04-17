import pygame
import sys

# 1. الإعدادات الأساسية
pygame.init()
WIDTH, HEIGHT = 700, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Master - Final Fix")

# 2. الألوان
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (30, 80, 250)      # لأرقام اللاعب
LIGHT_GRAY = (240, 240, 240) # لتظليل الصف والعمود
GRAY = (200, 200, 200)    # للخطوط العادية
HIGHLIGHT = (200, 220, 255) # للخلية المختارة
RED = (255, 50, 50)       # للرسائل الخطأ

# 3. الخطوط
font = pygame.font.SysFont("Arial", 45, bold=True)
small_font = pygame.font.SysFont("Arial", 25)

# 4. شبكة اللعبة (الثابتة)
# نستخدم مصفوفة تانية عشان نعرف إيه اللي ينفع يتمسح وإيه لأ
original_grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# نسخة اللاعب اللي هيعدل فيها
current_grid = [row[:] for row in original_grid]

CELL_SIZE = 65
OFFSET_X = (WIDTH - (9 * CELL_SIZE)) // 2
OFFSET_Y = 100

selected = None
msg = "Click a cell to start!"

def is_safe(board, row, col, num):
    for x in range(9):
        if board[row][x] == num or board[x][col] == num:
            return False
    start_r, start_c = row - row % 3, col - col % 3
    for i in range(3):
        for j in range(3):
            if board[i + start_r][j + start_c] == num:
                return False
    return True

def draw():
    screen.fill(WHITE)
    
    # رسم تظليل الصف والعمود المختار
    if selected:
        r, c = selected
        pygame.draw.rect(screen, LIGHT_GRAY, (OFFSET_X, OFFSET_Y + r * CELL_SIZE, 9 * CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, LIGHT_GRAY, (OFFSET_X + c * CELL_SIZE, OFFSET_Y, CELL_SIZE, 9 * CELL_SIZE))
        pygame.draw.rect(screen, HIGHLIGHT, (OFFSET_X + c * CELL_SIZE, OFFSET_Y + r * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # رسم الشبكة والأرقام
    for r in range(9):
        for c in range(9):
            rect = pygame.Rect(OFFSET_X + c * CELL_SIZE, OFFSET_Y + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            
            # تمييز الأرقام (الأسود للأصلي، الأزرق للاعب)
            if current_grid[r][c] != 0:
                color = BLACK if original_grid[r][c] != 0 else BLUE
                num_surface = font.render(str(current_grid[r][c]), True, color)
                screen.blit(num_surface, (rect.x + 20, rect.y + 10))
            
            # رسم خطوط الشبكة
            thickness = 4 if (r % 3 == 0 or c % 3 == 0) else 1
            pygame.draw.rect(screen, BLACK, rect, thickness)
    
    # رسم خطوط الإغلاق النهائية للشبكة
    pygame.draw.line(screen, BLACK, (OFFSET_X, OFFSET_Y + 9*CELL_SIZE), (OFFSET_X + 9*CELL_SIZE, OFFSET_Y + 9*CELL_SIZE), 4)
    pygame.draw.line(screen, BLACK, (OFFSET_X + 9*CELL_SIZE, OFFSET_Y), (OFFSET_X + 9*CELL_SIZE, OFFSET_Y + 9*CELL_SIZE), 4)

    # الرسائل التوضيحية
    info = small_font.render(msg, True, RED if "Wrong" in msg else BLACK)
    screen.blit(info, (WIDTH//2 - info.get_width()//2, 40))

def main():
    global selected, msg
    clock = pygame.time.Clock()

    while True:
        draw()
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                c = (mx - OFFSET_X) // CELL_SIZE
                r = (my - OFFSET_Y) // CELL_SIZE
                if 0 <= r < 9 and 0 <= c < 9:
                    selected = (r, c)
                    msg = f"Selected: Row {r+1}, Col {c+1}"
                else:
                    selected = None

            if event.type == pygame.KEYDOWN and selected:
                r, c = selected
                
                # منع التعديل على الأرقام الأصلية
                if original_grid[r][c] != 0:
                    msg = "Cannot change original numbers!"
                    continue

                if pygame.K_1 <= event.key <= pygame.K_9:
                    val = event.key - pygame.K_0
                    if is_safe(current_grid, r, c, val):
                        current_grid[r][c] = val
                        msg = "Nice move!"
                    else:
                        msg = f"Wrong! {val} is already in the row, column, or box."
                
                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    current_grid[r][c] = 0
                    msg = "Cleared cell."

        clock.tick(30)

if __name__ == "__main__":
    main()