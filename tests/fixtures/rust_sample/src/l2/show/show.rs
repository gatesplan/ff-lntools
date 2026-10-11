use std::fmt;

use crate::l1::order::Order;

pub struct Show;

impl fmt::Display for Order {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.qty)
    }
}
