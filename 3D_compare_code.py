
import struct, numpy as np, pyvista as pv

import struct
import plotly.graph_objects as go
from pathlib import Path
from tkinterdnd2 import TkinterDnD, DND_FILES
import sys
import tkinter as tk



def get_file_path():
    # 드래그 앤 드롭 창 생성
    root = TkinterDnD.Tk()
    root.withdraw()  # 창을 최소화한 상태로 시작

    # 파일 경로를 저장할 변수 생성
    file_path = None

    # 드롭 이벤트 처리 함수
    def on_drop(event):
        nonlocal file_path
        file_path = event.data  # 드롭된 파일의 경로 저장
        root.quit()  # 경로 저장 후 창 닫기
        root.destroy()

    def on_close():
        sys.exit()
    # 드래그 앤 드롭 설정
    root.drop_target_register(DND_FILES)
    root.dnd_bind('<<Drop>>', on_drop)
    root.protocol("WM_DELETE_WINDOW", on_close)  # 창 닫기 이벤트 처리
    # 드래그 앤 드롭 안내 라벨 생성
    label = tk.Label(root, text="Drag a file here", width=40, height=10)
    label.pack(padx=20, pady=20)

    root.deiconify()  # 창을 화면에 보이게 함
    root.mainloop()  # 이벤트 루프 실행

    # 창이 닫힌 후 경로 반환
    return file_path



def read_dat_memmap(path: str) -> np.memmap:
    with open(path, "rb") as f:
        w, h = struct.unpack("<2i", f.read(8))
    return np.memmap(path, dtype="<f4", mode="r", offset=8, shape=(h, w))




img_0_path = get_file_path()
img_1_path = get_file_path()
# Load the two uploaded height‑map files


z0 = read_dat_memmap(img_0_path)
z1 = read_dat_memmap(img_1_path)

ny, nx = z0.shape
x = np.arange(nx, dtype=np.float32)
y = np.arange(ny, dtype=np.float32)
xx, yy = np.meshgrid(x, y)

grid0 = pv.StructuredGrid(xx, yy, z0)        # 1, 5, 9, …
grid1 = pv.StructuredGrid(xx, yy, z1)

# ---------------------------------------------------------------------
# 3. Plotter + 두 surface + 슬라이더 세 개
# ---------------------------------------------------------------------
p = pv.Plotter(window_size=(1200, 800))
p.add_axes()

actor0 = p.add_mesh(grid0, color="dodgerblue", name="tip0", cmap="viridis", opacity=1.0)
actor1 = p.add_mesh(grid1, color="orangered", name="tip1", cmap="magma",    opacity=0.5)

# ── Tip0 Opacity ─────────────────────────────────────────────────────
def cb_tip0_opacity(val):
    actor0.GetProperty().SetOpacity(val)

p.add_slider_widget(
    callback=cb_tip0_opacity, value=1.0, rng=[0.0, 1.0], title="Tip0 Opacity",
    pointa=(.02, .1), pointb=(.32, .1), style='modern'
)

# ── Tip1 Opacity ─────────────────────────────────────────────────────
def cb_tip1_opacity(val):
    actor1.GetProperty().SetOpacity(val)

p.add_slider_widget(
    callback=cb_tip1_opacity, value=0.5, rng=[0.0, 1.0], title="Tip1 Opacity",
    pointa=(.02, .05), pointb=(.32, .05), style='modern'
)

# ── Z-Scale  (두 actor를 Z축만 스케일) ───────────────────────────────
def cb_zscale(scale):
    actor0.SetScale(1, 1, scale)
    actor1.SetScale(1, 1, scale)

p.add_slider_widget(
    callback=cb_zscale, value=1.0, rng=[0.25, 1.0], title="Z-Scale",
    pointa=(.02, .15), pointb=(.32, .15), style='modern'
)

# ---------------------------------------------------------------------
# 4. 스타트!
# ---------------------------------------------------------------------
p.camera.zoom(1.4)          # 초기 확대 비율 살짝 조정 (옵션)
p.show(title="Solder-Tip Height-Map Overlay (PyVista)")