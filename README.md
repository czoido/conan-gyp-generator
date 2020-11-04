# Conan gyp generator:

This [Conan generator](https://docs.conan.io/en/latest/howtos/custom_generators.html) will generate a
gyp file with all the dependencies. The original intended use of this generator is to make easier
link with third party libraries when adding native modules to node.

# To use:

``` bash
git clone https://github.com/czoido/conan-gyp-generator
cd conan-gyp-generator
conan create .
```

Create your consumer project ([see docs](https://docs.conan.io/en/latest/getting_started.html)) with
a conanfile.txt like this:

```
[requires]
yaml-cpp/0.6.3

[generators]
node_gyp

[build_requires]
gyp-generator/0.1

[options]
yaml-cpp:shared=True
```

A file conanbuildinfo.gyp will be generated, you have to add dependencies via that file in your
binding.gyp like this one:

```json
{
    "targets": [{
        "target_name": "conan_node_module",
        "sources": ["main.cpp"],
        "include_dirs": ["<!(node -e \"require('nan')\")"],
        "dependencies": ["<(module_root_dir)/conan_build/conanbuildinfo.gyp:yaml-cpp"],
        "conditions": [[
            "OS=='mac'", {
                "xcode_settings": {
                    "GCC_ENABLE_CPP_EXCEPTIONS": "YES"
                }
            }
        ]]
    }]
}
```