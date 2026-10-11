use crate::l0::{Candle, OrderPlacer};

pub trait Strategy {
    fn on_tick(&mut self, placer: &mut dyn OrderPlacer, candle: &Candle);
}
