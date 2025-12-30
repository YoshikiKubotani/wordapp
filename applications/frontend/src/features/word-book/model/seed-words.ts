import type { Word } from '@/entities/word'

export const seedWords: Word[] = [
  {
    id: 'seed-apple',
    term: 'apple',
    meaning: 'りんご',
    note: 'おやつやデザートでよく見る、甘くてシャキッとした果物',
    createdAt: new Date().toISOString(),
  },
  {
    id: 'seed-book',
    term: 'book',
    meaning: '本',
    note: '勉強や読書でよく使う、ページがあるもの',
    createdAt: new Date().toISOString(),
  },
  {
    id: 'seed-water',
    term: 'water',
    meaning: '水',
    note: '毎日飲む、透明で無味の飲み物',
    createdAt: new Date().toISOString(),
  },
]
