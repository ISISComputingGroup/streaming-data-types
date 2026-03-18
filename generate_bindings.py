import os
import sys
import shutil
import subprocess


def generate_python_bindings():
    pass


def to_rust_file_name(schema: str):
    name, ext = schema.split(".")
    return f"{name}.rs"


def to_rust_mod_name(schema: str):
    name, ext = schema.split(".")
    return f"{name[5:]}_{name[0:4]}"


def generate_rust_bindings():
    shutil.rmtree("rust/src/flatbuffers_generated/")
    os.makedirs("rust/src/flatbuffers_generated/")

    for schema in os.listdir("schemas"):
        if not schema.endswith(".fbs"):
            continue
        subprocess.run(
            [
                "flatc",
                "--rust",
                "-o",
                os.path.join("rust", "src", "flatbuffers_generated"),
                "--filename-suffix",
                "",
                "--gen-all",
                os.path.join("schemas", schema),
            ],
            check=True,
        )

        with open("rust/src/flatbuffers_generated/mod.rs", "a") as f:
            f.writelines(
                [
                    f'#[path = "{to_rust_file_name(schema)}"]\n',
                    f"pub mod {to_rust_mod_name(schema)};\n",
                ]
            )


def main():
    generate_rust_bindings()
    generate_python_bindings()


if __name__ == "__main__":
    main()
