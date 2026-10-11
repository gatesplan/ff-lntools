// 모듈 표면. lnt doc 이 생성한다

mod candle;
#[cfg(test)]
mod tests;

pub use candle::Candle;
