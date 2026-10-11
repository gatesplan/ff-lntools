// 모듈 표면. lnt doc 이 생성한다

mod parser;
#[cfg(test)]
mod tests;

pub use parser::Parser;
