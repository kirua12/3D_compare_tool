
# 3D Compare Tool – Windows EXE Builder

이 저장소를 **Fork**(또는 새 리포지토리를 만든 뒤 파일 업로드) 한 후  
**Actions → Build EXE → Run workflow** 버튼만 클릭하면  
Windows용 `3D_compare_code.exe` 실행 파일을 자동으로 받아볼 수 있습니다.

## Workflow Steps
1. **Set up Python 3.11** on a fresh `windows-latest` runner  
2. **Install dependencies**  
   - `pyvista`, `vtk` (3D rendering)  
   - `plotly` (for future extensions)  
   - `tkinterdnd2`, `numpy`  
   - `pyinstaller` + `pyinstaller-hooks-contrib`
3. **Build EXE** using:  
   ```bash
   pyinstaller --onefile --collect-all plotly --collect-all pyvista --collect-all vtk --hidden-import=tkinterdnd2 3D_compare_code.py
   ```
   `--collect-all` 옵션이 validator JSON·DLL·ICONS 등을 자동 포함합니다.
4. **Upload artifact** → `3D_compare_code.exe`

> **파일 크기**  
> VTK 동적 라이브러리 포함으로 결과 EXE가 300 MB 이상일 수 있습니다.  
> GitHub Artifacts 한도(2 GB)에 안전하며 다운로드 시 자동 압축됩니다.
