import time
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional

import pynvim

try:
    import black
except ModuleNotFoundError:
    black = None
try:
    import isort
except ModuleNotFoundError:
    isort = None
try:
    import autoflake
except ModuleNotFoundError:
    autoflake = None


@pynvim.plugin
class PyFormat:
    def __init__(self, nvim: pynvim.api.Nvim):
        self.n = nvim

    @pynvim.function("PyFormat")
    def pyformat(self, modules: List[str]) -> None:
        if self.n.current.buffer.options.get("filetype") != "python":
            self.n.err_write("Not in a python file.\n")
            return
        if len(modules) == 0:
            self.n.err_write(
                "Pass one or more formatter names. Valid formatters are 'black', 'isort', and 'autoflake'.\n"
            )
            return

        start = time.perf_counter()
        code_original = "\n".join(self.n.current.buffer) + "\n"
        code = code_original
        time_breakdown = {}
        for mod in modules:
            mod_start = time.perf_counter()
            if mod == "black":
                code = self.black(code)
            elif mod == "isort":
                code = self.isort(code)
            elif mod == "autoflake":
                code = self.autoflake(code)
            else:
                self.n.err_write(
                    f"Unknown formatter {mod}. Known formatters are 'black', 'isort', and 'autoflake'"
                )
                return
            time_breakdown[mod] = time.perf_counter() - mod_start
        if code == code_original:
            self.n.out_write(fmt_result("Unchanged", start, time_breakdown))
            return
        # Cursor position is maintained automatically
        self.n.current.buffer[:] = code.split("\n")[:-1]
        self.n.out_write(fmt_result("Formatted", start, time_breakdown))

    @pynvim.function("PyFormatSync", sync=True)
    def pyformat_sync(self, args: List[str]) -> None:
        return self.pyformat(args)

    def get_autoflake_opts(self) -> Dict[str, Any]:
        options = {}
        user_options = self.n.vars.get("autoflake#settings")
        if user_options is not None:
            options.update(user_options)
        return options

    def autoflake(self, to_format: str) -> str:
        if autoflake is None:
            raise ModuleNotFoundError(fmt_missing("autoflake"))
        autoflake_opts = self.get_autoflake_opts()
        return autoflake.fix_code(to_format, **autoflake_opts)

    def get_black_opts(self) -> Dict[str, Any]:
        options = {
            "fast": False,
            "line_length": 88,
            "is_pyi": self.n.current.buffer.name.endswith(".pyi"),
        }
        tw: int = self.n.current.buffer.options.get("textwidth")
        if tw > 0:
            options["line_length"] = tw
        user_options = self.n.vars.get("black#settings")
        if user_options is not None:
            options.update(user_options)
        return options

    def black(self, to_format: str) -> str:
        if black == None:
            raise ModuleNotFoundError(fmt_missing("black"))
        black_opts = self.get_black_opts()
        mode = black.FileMode(line_length=black_opts["line_length"], is_pyi=black_opts["is_pyi"])
        try:
            return black.format_file_contents(to_format, fast=black_opts["fast"], mode=mode)
        except black.NothingChanged:
            return to_format
        except black.InvalidInput:
            self.n.err_write(traceback.format_exc(limit=1) + "\n")
            return to_format

    def get_isort_opts(self) -> Dict[str, Any]:
        options: Dict[str, Any] = {
            "profile": "black",
        }
        tw: int = self.n.current.buffer.options.get("textwidth")
        if tw > 0:
            options["line_length"] = tw
        user_options = self.n.vars.get("isort#settings")
        if user_options is not None:
            options.update(user_options)
        return options

    def isort(self, to_format: str) -> str:
        if isort is None:
            raise ModuleNotFoundError(fmt_missing("isort"))
        isort_opts = self.get_isort_opts()
        return isort.api.sort_code_string(to_format, file_path=self.get_file_path(), **isort_opts)

    def get_file_path(self) -> Optional[Path]:
        bufname = self.n.current.buffer.name
        if bufname is None:
            return None
        file_path = Path(bufname)
        if file_path.is_absolute() and file_path.exists():
            return file_path
        return None

    def write_result(self, res: str, start: float, time_breakdown: Dict[str, float]) -> None:
        total = round(1000 * (time.perf_counter() - start))
        breakdown = ", ".join([f"{k} {round(1000 * v)}" for k, v in time_breakdown.items()])
        (f"PyFormat: {res} in {total}ms ({breakdown}).\n")


def fmt_missing(mod: str) -> str:
    return f"{mod} is not installed in your g:python3_host_prog, please install it with pip and restart neovim"


def fmt_result(res: str, start: float, time_breakdown: Dict[str, float]) -> str:
    total = round(1000 * (time.perf_counter() - start))
    breakdown = ", ".join([f"{k} {round(1000 * v)}ms" for k, v in time_breakdown.items()])
    return f"PyFormat: {res} in {total}ms ({breakdown}).\n"
