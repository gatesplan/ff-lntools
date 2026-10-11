pub struct Logger;

impl Logger {
    pub fn log() {
        println!("{}", crate::l2::report::Report::NAME);
    }
}
