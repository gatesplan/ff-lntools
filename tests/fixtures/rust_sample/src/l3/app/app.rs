use crate::l2::report::Report;

pub struct App;

impl App {
    pub fn name() -> &'static str {
        Report::NAME
    }
}
