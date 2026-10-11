use crate::l2::{Engine, Momentum};

pub struct App;

impl App {
    pub fn run(closes: &[u32]) -> i64 {
        let mut engine = Engine::new(Box::new(Momentum::default()));
        engine.run(closes)
    }
}
