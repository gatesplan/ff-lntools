// 모듈 표면. lnt doc 이 생성한다

mod money;
#[cfg(test)]
mod tests;

pub use money::Money;
