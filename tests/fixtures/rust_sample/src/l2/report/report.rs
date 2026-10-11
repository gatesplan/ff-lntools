use crate::l1::order::Order;

pub struct Report;

impl Report {
    pub const NAME: &'static str = "report";
}

impl Order {
    pub fn line(&self) -> String {
        format!("qty {}", self.qty)
    }
}

pub trait OrderExt {
    fn label(&self) -> String;
}

impl OrderExt for Order {
    fn label(&self) -> String {
        self.line()
    }
}
