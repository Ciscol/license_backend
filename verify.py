from app.license_util import license_generate, license_verify

try:
    print(license_verify.license_verify())
except Exception as ex:
    print(ex)
