import zipfile, opcode
from types import CodeType


def _patch_code_obj(code, custom_co_code):
    return CodeType(
        code.co_argcount, code.co_kwonlyargcount, code.co_nlocals,
        code.co_stacksize, code.co_flags, custom_co_code,
        code.co_consts, code.co_names, code.co_varnames,
        code.co_filename, code.co_name, code.co_firstlineno,
        code.co_lnotab, code.co_freevars, code.co_cellvars
    )


def patch_zipfile():
    code = zipfile.ZipInfo.__init__.__code__
    patched_co_code = code.co_code

    nop_padding = bytes([opcode.opmap["NOP"] for _ in range(34)])
    patched_co_code = patched_co_code[:6] + nop_padding + patched_co_code[40:]
    zipfile.ZipInfo.__init__.__code__ = _patch_code_obj(code, patched_co_code)
