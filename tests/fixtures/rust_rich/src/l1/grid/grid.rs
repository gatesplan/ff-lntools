use crate::l0::{Id, Tagged};

#[derive(Debug)]
pub struct Grid<const N: usize> {
    pub cells: [u8; N],
}

impl<const N: usize> Grid<N> {
    pub const SIZE: usize = N;

    pub fn filled(v: u8) -> Self {
        Self { cells: [v; N] }
    }

    pub fn total(&self) -> u32 {
        self.cells.iter().map(|&c| u32::from(c)).sum()
    }

    pub fn tagged(&self, tag: &'static str) -> Tagged<'static, [u8]> {
        Tagged::new(tag, self.cells.to_vec().into_boxed_slice())
    }

    pub fn id(&self) -> Id {
        Id::from(self.total())
    }
}
