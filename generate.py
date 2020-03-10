from app.license_util import license_generate

try:
    license_generate.license_generate()
except Exception as ex:
    print(ex)
