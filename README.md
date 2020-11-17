# Conan gyp generator:

This [Conan generator](https://docs.conan.io/en/latest/howtos/custom_generators.html) will generate a
gyp file with all the dependencies. The original intended use of this generator is to make easier
link with third party libraries when adding native modules to node using node-gyp. 

It's just a minimal implementation and has only been tested on MacOS and shared libraries.

Find some more detailed information in [this blogpost](https://czoido.github.io/posts/node-native-module-conan/).

# To install the generator:

``` bash
git clone https://github.com/czoido/conan-gyp-generator
cd conan-gyp-generator
conan config install gyp-generator.py -tf generators
```

Create your consumer project ([see docs](https://docs.conan.io/en/latest/getting_started.html)) with
a conanfile.txt like this:

```
[requires]
yaml-cpp/0.6.3

[generators]
node_gyp

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
