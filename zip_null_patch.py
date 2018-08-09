import zipfile, opcode
from types import CodeType


def patch_zipfile():
    code = zipfile.ZipInfo.__init__.__code__
    patched_code = code.co_code

    patched_code = patched_code[:6] + bytes([opcode.opmap["NOP"]]) * (40 - 6) + patched_code[40:]

    # Since CodeType objects are immutable, we have to create a new one.
    new_code = CodeType(code.co_argcount, code.co_kwonlyargcount,
                        code.co_nlocals, code.co_stacksize,
                        code.co_flags,
                        patched_code,
                        code.co_consts,
                        code.co_names, code.co_varnames,
                        code.co_filename, code.co_name,
                        code.co_firstlineno, code.co_lnotab,
                        code.co_freevars, code.co_cellvars)

    zipfile.ZipInfo.__init__.__code__ = new_code
