# © 2019-2020 Aman Verma <https://aman.raoverma.com/contact.html>
# Distributed under the MIT license, see LICENSE.md file for details.

import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Union

import pynvim

try:
    import black
except ImportError:
    print(
        "[*] black is not installed in your g:python3_host_prog, "
        "please install it with pip and try again",
        file=sys.stderr,
    )
    sys.exit(1)
try:
    import isort
except ImportError:
    print(
        "[*] isort is not installed in your g:python3_host_prog, "
        "please install it with pip and try again",
        file=sys.stderr,
    )
    sys.exit(1)


@pynvim.plugin
class BlackIsorter:
    def __init__(self, nvim: pynvim.api.Nvim):
        self.n = nvim

    @pynvim.function("BlackIsort")
    # args is not used but needs to be there to avoid an error.
    def black_isort(self, args: List[str]) -> None:
        if self.n.current.buffer.options.get("filetype") != "python":
            self.n.err_write("Not in a python file.\n")
            return

        start = time.perf_counter()
        black_opts = self.get_black_opts()
        isort_opts = self.get_isort_opts()
        buf_str = "\n".join(self.n.current.buffer) + "\n"
        self.format_buff(buf_str, black_opts, isort_opts, start)

    @pynvim.function("BlackIsortSync", sync=True)
    def black_isort_sync(self, args: List[str]) -> None:
        return self.black_isort(args)

    def get_black_opts(self) -> Dict[str, Union[int, bool]]:
        options = {
            "fast": False,
            "line_length": 88,
            "is_pyi": self.n.current.buffer.name.endswith(".pyi"),
        }
        user_options = self.n.vars.get("black#settings")
        if user_options is not None:
            options.update(user_options)
        tw: int = self.n.current.buffer.options.get("textwidth")
        if tw > 0:
            options["line_length"] = tw
        return options

    def get_isort_opts(self) -> Dict[str, Union[int, str]]:
        options: Dict[str, Union[int, str]] = {
            "profile": "black",
        }
        user_options = self.n.vars.get("isort#settings")
        if user_options is not None:
            options.update(user_options)
        tw: int = self.n.current.buffer.options.get("textwidth")
        if tw > 0:
            options["line_length"] = tw
        return options

    def format_buff(
        self,
        to_format: str,
        black_opts: Dict[str, Union[int, bool]],
        isort_opts: Dict[str, Union[int, bool]],
        start: float,
    ) -> None:
        mode = black.FileMode(line_length=black_opts["line_length"], is_pyi=black_opts["is_pyi"])
        try:
            new_buffer = black.format_file_contents(to_format, fast=black_opts["fast"], mode=mode)
        except black.NothingChanged:
            new_buffer = to_format
        except black.InvalidInput:
            self.n.err_write(traceback.format_exc(limit=1))
        try:
            new_buffer = isort.api.sort_code_string(
                new_buffer, file_path=self.get_file_path(), **isort_opts
            )
        except black.InvalidInput:
            self.n.err_write(traceback.format_exc(limit=1))
        if to_format == new_buffer:
            self.n.out_write(
                f"BlackIsort: Unchanged in {round(1000 * (time.perf_counter() - start))}ms.\n"
            )
        else:
            # update buffer, remembering the location of the cursor
            cursor = self.n.current.window.cursor

            self.n.current.buffer[:] = new_buffer.split("\n")[:-1]
            try:
                self.n.current.window.cursor = cursor
            except pynvim.api.NvimError:
                # if cursor is outside buffer, set it to last line.
                self.n.current.window.cursor = (len(self.n.current.buffer), 0)

            self.n.out_write(
                f"BlackIsort: Formatted in {round(1000 * (time.perf_counter() - start))}ms.\n"
            )

    def get_file_path(self) -> Optional[Path]:
        bufname = self.n.current.buffer.name
        if bufname is None:
            return None
        file_path = Path(bufname)
        if file_path.is_absolute() and file_path.exists():
            return file_path
        return None
