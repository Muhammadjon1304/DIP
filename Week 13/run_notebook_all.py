import json
import traceback
from pathlib import Path

NOTEBOOK_PATH = Path("simple_segmentation_training_notebook.ipynb")

with NOTEBOOK_PATH.open() as f:
    notebook = json.load(f)

namespace = {"__name__": "__main__"}

try:
    import matplotlib

    matplotlib.use("Agg")
except Exception:
    pass

local_project_dir = Path.cwd() / "simple_segmentation_training"
local_project_dir.mkdir(parents=True, exist_ok=True)


class _DummyDrive:
    def mount(self, *args, **kwargs):
        print("Colab drive mount skipped (local run).")


namespace["drive"] = _DummyDrive()

executed = 0

for i, cell in enumerate(notebook.get("cells", []), start=1):
    if cell.get("cell_type") != "code":
        continue

    source = "".join(cell.get("source", []))

    if "from google.colab import drive" in source:
        source = "drive.mount('/content/drive')\n"

    source = source.replace(
        "/content/drive/MyDrive/simple_segmentation_training",
        str(local_project_dir),
    )

    print(f"\n=== Running code cell {i} ===")

    try:
        exec(compile(source, f"{NOTEBOOK_PATH} [cell {i}]", "exec"), namespace)
        executed += 1
    except Exception:
        print(f"!!! Error in code cell {i}")
        traceback.print_exc()
        print(f"\nExecuted {executed} code cells before failure.")
        raise SystemExit(1)

print(f"\nAll code cells executed successfully ({executed} cells).")
