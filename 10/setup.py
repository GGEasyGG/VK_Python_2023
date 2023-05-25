from distutils.core import setup, Extension


module = Extension("cjson", sources=["cjson.c"])
setup(name="cjson", version="1.0", description="JSON parsing and serialization module", ext_modules=[module])
