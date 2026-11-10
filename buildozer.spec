[app]
title = Bukulaptah
package.name = Laptah
package.domain = org.contohku
source.dir = .
source.include_exts = py,png,jpg,kv,db,json,txt
version = 1.0
requirements = python3,kivy
orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 1

[android]
api = 34
minapi = 24
archs = arm64-v8a,armeabi-v7a
accept_sdk_license = True