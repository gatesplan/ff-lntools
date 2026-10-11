use crate::l1::order::Order;

pub struct Ext(pub Order);

impl Ext {
    pub fn json(&self) -> String {
        serde_json::json!({ "qty": self.0.qty }).to_string()
    }
}
