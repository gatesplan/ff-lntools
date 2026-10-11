use crate::l0::Candle;
use crate::l1::book::Ledger;
use crate::l1::strategy::Strategy;

pub struct Engine {
    strategy: Box<dyn Strategy>,
    ledger: Ledger,
}

impl Engine {
    pub fn new(strategy: Box<dyn Strategy>) -> Self {
        Self { strategy, ledger: Ledger::default() }
    }

    pub fn run(&mut self, closes: &[u32]) -> i64 {
        for &c in closes {
            self.strategy.on_tick(&mut self.ledger, &Candle::new(c));
        }
        self.ledger.position()
    }
}
