[app]

title = Тренажёр знаков
package.name = sporttrainer
package.domain = org.orient

source.dir = .
source.include_exts = py,png,jpg,kv

version = 1.0

requirements = python3,kivy==2.2.1

orientation = portrait
fullscreen = 0

resource.entrypoint = main.py

android.api = 33
android.minapi = 21
android.ndk = 25c

android.accept_sdk_license = True

android.archs = arm64-v8a

android.debug = True

python.version = 3.10

source.include_patterns = images/*.png

[buildozer]
log_level = 2
p4a.branch = develop#    -----------------------------------------------------------------------------
#    Profiles
#
#    You can extend section / key with a profile
#    For example, you want to deploy a demo version of your application without
#    HD content. You could first change the title to add "(demo)" in the name
#    and extend the excluded directories to remove the HD content.
#
#[app@demo]
#title = My Application (demo)
#
#[app:source.exclude_patterns@demo]
#images/hd/*
#
#    Then, invoke the command line with the "demo" profile:
#
#buildozer --profile demo android debug
