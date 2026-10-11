use crate::l0::candle::Candle;
use crate::l0::order_placer::{OrderPlacer, Side};
use crate::l1::strategy::Strategy;

#[derive(Default)]
pub struct Momentum {
    last: Option<u32>,
}

impl Strategy for Momentum {
    fn on_tick(&mut self, placer: &mut dyn OrderPlacer, candle: &Candle) {
        if let Some(prev) = self.last {
            if candle.close > prev {
                placer.place_order(Side::Buy, 1);
            } else if candle.close < prev {
                placer.place_order(Side::Sell, 1);
            }
        }
        self.last = Some(candle.close);
    }
}
