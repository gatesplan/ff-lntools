use crate::l1::order::Order;

pub struct Money(pub u32);

impl Money {
    pub fn of(o: &Order) -> Money {
        Money(o.qty)
    }
}
