use crate::l0::order_placer::{OrderPlacer, Side};
use crate::l1::book::l0::position::Position;

#[derive(Default)]
pub struct Ledger {
    items: Vec<Position>,
}

impl Ledger {
    pub fn position(&self) -> i64 {
        self.items.iter().map(|p| p.qty).sum()
    }
}

impl OrderPlacer for Ledger {
    fn place_order(&mut self, side: Side, qty: u32) {
        let qty = i64::from(qty);
        self.items.push(Position { qty: if side == Side::Buy { qty } else { -qty } });
    }
}
