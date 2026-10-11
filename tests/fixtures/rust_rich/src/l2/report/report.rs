use crate::l0::shape::Shape;
use crate::l0::Money;
use crate::l1::{Circle, KitError};

macro_rules! line {
    ($label:expr, $v:expr) => {
        format!("{}: {}", $label, $v)
    };
}

/// 금액을 보고서 줄로 바꾸는 확장
pub trait MoneyExt {
    fn report_line(&self) -> String;
}

impl MoneyExt for Money {
    fn report_line(&self) -> String {
        line!("money", self)
    }
}

#[derive(Debug, thiserror::Error)]
pub enum ReportError {
    #[error(transparent)]
    Kit(#[from] KitError),
}

#[derive(Debug, Default)]
pub struct Report {
    shapes: Vec<Box<dyn Shape<Unit = f64>>>,
}

impl Report {
    pub fn with_circle(mut self, r: f64) -> Self {
        self.shapes.push(Box::new(Circle { r }));
        self
    }

    pub fn area(&self) -> f64 {
        self.shapes.iter().map(|s| s.area()).sum()
    }

    pub fn scaled_area(&self) -> f64 {
        crate::l1::Circle { r: 1.0 }.scaled(2.0)
    }

    pub fn render(&self, total: Money) -> String {
        [line!("area", format!("{:.1}", self.area())), total.report_line()].join("\n")
    }
}
