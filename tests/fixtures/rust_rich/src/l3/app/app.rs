use crate::l1::grid::Grid;
use crate::l2::parser::Parser;
use crate::l2::report::{Report, ReportError};
use crate::l2::store::Cache;

/// 모든 부품을 엮는다
#[derive(Debug)]
pub struct App;

impl App {
    pub fn run(input: &str) -> Result<String, ReportError> {
        let parsed = Parser::strict().parse(input)?;
        let mut cache = Cache::default();
        for (i, m) in parsed.into_iter().enumerate() {
            cache.put(i as u64, m)?;
        }
        let grid = Grid::<3>::filled(2);
        let tag = grid.tagged("g");
        let report = Report::default().with_circle(1.0);
        let evens = Parser::evens(&[1, 2, 4]).count();
        drop(Parser::strict().parse_later(String::new()));
        Ok(format!("{}\n{} {} {} {} {} {}", report.render(cache.total()), tag.tag, tag.value.len(), grid.id(), Grid::<3>::SIZE, evens, report.scaled_area()))
    }
}
