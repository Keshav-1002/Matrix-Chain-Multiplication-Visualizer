from tkinter import *
import winsound

dims = []
n = 0
dp = []
s = []
node_radius = 20
draw_steps = []

def play_click_sound():
    winsound.Beep(800, 75)

def play_success_sound():
    winsound.Beep(1000, 150)

def play_error_sound():
    winsound.Beep(400, 250)

def visualize():
    global dims, n, dp, s, draw_steps

    dims_input = input_entry.get().strip().split()
    
    if len(dims_input) < 3:
        cost_label.config(text="Enter at least 3 dimensions!")
        play_error_sound()
        return
    
    try:
        dims = list(map(int, dims_input))
        
    except:
        cost_label.config(text="Invalid input! Enter integers separated by space.")
        play_error_sound()
        return

    play_click_sound()
    n = len(dims) - 1

    canvas.delete("all")
    cost_label.config(text="Minimum Multiplication Cost: Calculating...")

    dp = [[0] * (n + 1) for _ in range(n + 1)]
    s = [[0] * (n + 1) for _ in range(n + 1)]

    for length in range(2, n + 1):
        
        for i in range(1, n - length + 2):
            j = i + length - 1
            dp[i][j] = float('inf')
            
            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + dims[i - 1] * dims[k] * dims[j]
                
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    s[i][j] = k

    cost_label.config(text=f"Minimum Multiplication Cost: {dp[1][n]}")

    draw_steps.clear()

    total_width = calculate_width(1, n)
    build_draw_steps(1, n, 1000, 50, total_width)
    draw_next_step(0)

def calculate_width(i, j):
    
    if i == j:
        return 1
    
    k = s[i][j]
    return calculate_width(i, k) + calculate_width(k + 1, j)

def build_draw_steps(i, j, x, y, width):
    
    if i == j:
        label = f"A{i} ({dims[i - 1]}x{dims[i]})"
        draw_steps.append(("node", x, y, label))
        return x, y, 1

    k = s[i][j]
    left_width = calculate_width(i, k)
    right_width = calculate_width(k + 1, j)
    total_width = left_width + right_width
    unit = 100

    left_x = x - (right_width / total_width) * width * unit
    right_x = x + (left_width / total_width) * width * unit
    next_y = y + 100

    lx, ly, _ = build_draw_steps(i, k, left_x, next_y, left_width)
    rx, ry, _ = build_draw_steps(k + 1, j, right_x, next_y, right_width)

    label = f"({i},{j})"
    draw_steps.append(("node", x, y, label))
    draw_steps.append(("line", x, y + node_radius, lx, ly - node_radius))
    draw_steps.append(("line", x, y + node_radius, rx, ry - node_radius))

    return x, y, total_width

def draw_next_step(step_idx):
    if step_idx >= len(draw_steps):
        play_success_sound()
        return

    step = draw_steps[step_idx]
    
    if step[0] == "node":
        _, x, y, label = step
        draw_node(x, y, label)
        
    elif step[0] == "line":
        _, x1, y1, x2, y2 = step
        canvas.create_line(x1, y1, x2, y2, width=2)

    delay = int(speed_var.get() * 1000)
    root.after(delay, draw_next_step, step_idx + 1)

def draw_node(x, y, text):
    r = node_radius
    canvas.create_oval(x - r, y - r, x + r, y + r, fill='lightblue', outline='black')
    canvas.create_text(x, y, text=text, font=("Arial", 12, "bold"))

root = Tk()
root.title("Matrix Chain Multiplication Visualizer")
root.geometry("1000x600")
root.config(bg='white')

input_frame = Frame(root, bg='white')
input_frame.pack(pady=10)

Label(input_frame, text="Enter dimensions (space separated):", bg='white', font=8).pack(side=LEFT,
        padx=5)
input_entry = Entry(input_frame, width=30, font=6)
input_entry.pack(side=LEFT, padx=5)
input_entry.focus_set()
Button(input_frame, text="Visualize", command=visualize, font=8).pack(side=LEFT, padx=5)

speed_frame = Frame(root, bg='white')
speed_frame.pack(pady=5)
Label(speed_frame, text="Animation Speed (s):", bg='white', font=6).pack(side=LEFT)
speed_var = DoubleVar(value=0.01)
speed_slider = Scale(speed_frame, from_=0.01, to=2.0, resolution=0.1, orient=HORIZONTAL,
                        variable=speed_var)
speed_slider.pack(side=LEFT)

canvas = Canvas(root, bg='white', width=1000, height=400, scrollregion=(0, 0, 2500, 800))
canvas.pack(pady=10, fill=BOTH, expand=True)

h_scroll = Scrollbar(root, orient=HORIZONTAL, command=canvas.xview)
h_scroll.pack(fill=X)
canvas.config(xscrollcommand=h_scroll.set)

cost_label = Label(root, text="Minimum Multiplication Cost: ", bg='white', font=("Arial", 20))
cost_label.pack(pady=10)

root.mainloop()
