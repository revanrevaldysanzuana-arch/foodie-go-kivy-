[app]
title = FOODIE GO
package.name = foodiego
package.domain = com.revan
source.dir = .
source.include_exts = py,txt,png,jpg,kv
version = 1.0.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0

# Buildozer Android settings
android.permissions =
android.api = 35
android.minapi = 23
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
