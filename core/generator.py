from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from .schema import Resume

_HERE = Path(__file__).parent.parent
_TEMPLATE_DIR = _HERE / "templates"
_OUTPUT_DIR = _HERE / "output"

_env = Environment(loader=FileSystemLoader(str(_TEMPLATE_DIR)))
_template = _env.get_template("resume.html")


def generate_html(resume: Resume, filename: str = "resume.html") -> Path:
    """将 Resume 对象渲染为 HTML 文件"""
    _OUTPUT_DIR.mkdir(exist_ok=True)
    html = _template.render(resume=resume)
    out_path = _OUTPUT_DIR / filename
    out_path.write_text(html, encoding="utf-8")
    return out_path
