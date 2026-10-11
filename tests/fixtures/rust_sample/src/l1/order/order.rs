use crate::l0::candle::Candle;

pub struct Order {
    pub qty: u32,
}

impl Order {
    pub fn value(&self, c: &Candle) -> u32 {
        self.qty * c.close
    }
}

#[cfg(test)]
use crate::l2::report::Report;
