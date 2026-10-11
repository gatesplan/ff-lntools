use super::side::Side;

pub trait OrderPlacer {
    fn place_order(&mut self, side: Side, qty: u32);
}
