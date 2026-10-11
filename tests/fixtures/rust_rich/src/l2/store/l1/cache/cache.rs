use std::collections::HashMap;

use super::super::super::l0::key::Key;
use crate::l0::Money;
use crate::l1::KitError;

#[derive(Debug, Default)]
pub struct Cache {
    items: HashMap<Key, Money>,
}

impl Cache {
    pub fn put(&mut self, id: u64, m: Money) -> Result<(), KitError> {
        if m < Money::ZERO {
            return Err(KitError::Negative(m));
        }
        self.items.insert(Key(id), m);
        Ok(())
    }

    pub fn total(&self) -> Money {
        self.items.values().fold(Money::ZERO, |a, &b| a + b)
    }
}
