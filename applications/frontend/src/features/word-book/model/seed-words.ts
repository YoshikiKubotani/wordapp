import type { Word } from '@/entities/word'

export const seedWords: Word[] = [
  {
    id: 'seed-serendipity',
    term: 'serendipity',
    meaning: 'A pleasant surprise or valuable discovery found by accident',
    note: 'Think of stumbling upon a cozy cafe while getting lost.',
    createdAt: new Date().toISOString(),
  },
  {
    id: 'seed-meticulous',
    term: 'meticulous',
    meaning: 'Showing great attention to detail; very careful and precise',
    note: 'Perfect for someone who double-checks everything.',
    createdAt: new Date().toISOString(),
  },
  {
    id: 'seed-resilient',
    term: 'resilient',
    meaning: 'Able to withstand or recover quickly from difficult situations',
    note: 'A word you want to remember on tough days.',
    createdAt: new Date().toISOString(),
  },
]
