use std::fs;
use std::fs::{File, OpenOptions, create_dir_all};
use std::io::Write;
use std::path::Path;

fn mod_name_from_stem(name: &str) -> String {
    format!("{}_{}", name.get(5..).unwrap(), name.get(0..4).unwrap()).to_owned()
}

fn main() {
    create_dir_all("src/flatbuffers_generated")
        .expect("Unable to create src/flatbuffers_generated");
    File::create("src/flatbuffers_generated/mod.rs")
        .expect("Failed to create src/flatbuffers_generated/mod.rs");

    let mut mod_file = OpenOptions::new()
        .append(true)
        .open("src/flatbuffers_generated/mod.rs")
        .expect("Could not open src/flatbuffers_generated/mod.rs");

    fs::read_dir("../schemas")
        .expect("Could not read schemas directory")
        .filter_map(|e| e.ok())
        .for_each(|entry| {
            println!(
                "cargo:rerun-if-changed={}",
                entry.path().as_path().to_str().unwrap()
            );
            flatc_rust::run(flatc_rust::Args {
                inputs: &[entry.path().as_path()],
                out_dir: Path::new("src/flatbuffers_generated/"),
                extra: &[
                    "--include-prefix",
                    "flatbuffers_generated",
                    "--filename-suffix",
                    "",
                    "--gen-all",
                ],
                ..Default::default()
            })
            .expect("cannot find flatc compiler");

            let path = entry.path();
            let stem = path
                .file_stem()
                .expect("Can't get file stem")
                .to_str()
                .expect("Can't convert file stem to str");
            let rust_name = mod_name_from_stem(stem);

            writeln!(
                mod_file,
                "#[path = \"{stem}.rs\"]
pub mod {rust_name};
"
            )
            .expect("Could not write to src/flatbuffers_generated/mod.rs");
        })
}
