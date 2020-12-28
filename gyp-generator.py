from jinja2 import Template

from conans.model import Generator
from pathlib import PurePath
import textwrap


class node_gyp(Generator):
    @property
    def filename(self):
        return "conanbuildinfo.gyp"

    def get_build_requires_names(self):
        return [name for (name, _) in self.conanfile.build_requires]

    @property
    def content(self):
        target_template = textwrap.dedent("""\
            {
                "target_name": "{{dep}}",
                "type": "<(library)",
                "direct_dependent_settings": {
                    "include_dirs": [
                        {% for include_path in include_paths -%}
                        "{{ include_path }}",
                        {%- endfor %}                    
                    ],
                    {% if lib_paths -%}
                    "libraries": [
                        {% for lib in libs -%}
                        "-l{{ lib }}", 
                        {%- endfor %}
                        {% for lib_path in lib_paths -%}
                        "-L{{ lib_path }}",
                        {%- endfor %}
                        "-Wl,-rpath,<(module_root_dir)/build/Release/"
                    ]
                    {%- endif %}
                }
            }
        """)
        gyp_template = textwrap.dedent("""\
            {
            "targets": [
                    {{- targets -}}
                ]
            }
            """)
        sections = []
        for dep in self.conanfile.deps_cpp_info.deps:
            if dep not in self.get_build_requires_names():
                info = {
                    "dep": dep,
                    "libs": [PurePath(folder).as_posix() for folder in self.conanfile.deps_cpp_info[dep].libs],
                    "lib_paths": [PurePath(folder).as_posix() for folder in self.conanfile.deps_cpp_info[dep].lib_paths],
                    "include_paths": [PurePath(folder).as_posix() for folder in self.conanfile.deps_cpp_info[dep].include_paths],
                }
                t = Template(target_template)
                sections.append(t.render(**info))
        t = Template(gyp_template)
        return t.render(targets=",\n".join(sections))
