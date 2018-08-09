import zipfile, opcode
from types import CodeType


def patch_zipfile():
    code = zipfile.ZipInfo.__init__.__code__
    payload = code.co_code

    payload = payload[:6] + bytes([opcode.opmap["NOP"]]) * 34 + payload[40:]
    new_code = CodeType(code.co_argcount,
                        code.co_kwonlyargcount,
                        code.co_nlocals,
                        code.co_stacksize,
                        code.co_flags,
                        payload,
                        code.co_consts,
                        code.co_names,
                        code.co_varnames,
                        code.co_filename,
                        code.co_name,
                        code.co_firstlineno,
                        code.co_lnotab,
                        code.co_freevars,
                        code.co_cellvars)

    zipfile.ZipInfo.__init__.__code__ = new_code
