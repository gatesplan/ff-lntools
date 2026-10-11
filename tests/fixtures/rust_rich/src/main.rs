fn main() {
    match kit_core::App::run("1,2,3") {
        Ok(s) => println!("{s}"),
        Err(e) => eprintln!("{e}"),
    }
}
