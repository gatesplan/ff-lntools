/// 이름표가 붙은 값
#[derive(Debug)]
pub struct Tagged<'a, T: ?Sized> {
    pub tag: &'a str,
    pub value: Box<T>,
}

pub type Id = u64;

impl<'a, T: ?Sized> Tagged<'a, T> {
    pub fn new(tag: &'a str, value: Box<T>) -> Self {
        Self { tag, value }
    }
}
