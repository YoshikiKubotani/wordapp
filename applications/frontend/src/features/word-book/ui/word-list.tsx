import { useEffect, useMemo, useState } from 'react'
import { useAtomValue, useSetAtom } from 'jotai'
import { removeWordAtom, sortedWordsAtom } from '@/features/word-book'
import { Badge } from '@/shared/ui/badge'
import { Button } from '@/shared/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/shared/ui/card'

const PAGE_SIZE = 5

export function WordList() {
  const words = useAtomValue(sortedWordsAtom)
  const removeWord = useSetAtom(removeWordAtom)
  const [page, setPage] = useState(1)

  const totalPages = useMemo(
    () => (words.length === 0 ? 1 : Math.ceil(words.length / PAGE_SIZE)),
    [words.length],
  )

  useEffect(() => {
    if (page > totalPages) {
      setPage(totalPages)
    }
  }, [page, totalPages])

  const startIndex = (page - 1) * PAGE_SIZE
  const visibleWords = words.slice(startIndex, startIndex + PAGE_SIZE)
  const hasPagination = words.length > PAGE_SIZE
  const displayStart = words.length === 0 ? 0 : startIndex + 1
  const displayEnd = Math.min(startIndex + PAGE_SIZE, words.length)

  return (
    <Card className="backdrop-blur">
      <CardHeader className="flex flex-row items-start justify-between">
        <div className="space-y-1">
          <CardTitle>単語一覧</CardTitle>
          <CardDescription>追加した単語の一覧（追加した順）</CardDescription>
        </div>
      </CardHeader>
      <CardContent className="space-y-3">
        {words.length === 0 ? (
          <p className="text-sm text-secondary-foreground">
            まだ単語が追加されていないよ！まずは学習したい単語を追加しよう
          </p>
        ) : (
          <>
            <div className="space-y-3">
              {visibleWords.map((word) => (
                <div
                  key={word.id}
                  className="group rounded-lg border border-border/70 bg-card/60 p-3 shadow-sm transition hover:-translate-y-[1px] hover:shadow-md"
                >
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <p className="text-base font-semibold text-foreground">{word.term}</p>
                      <p className="text-sm text-secondary-foreground">{word.meaning}</p>
                    </div>
                    <Button
                      type="button"
                      size="sm"
                      variant="ghost"
                      className="opacity-0 transition group-hover:opacity-100"
                      onClick={() => removeWord(word.id)}
                      aria-label={`Remove ${word.term}`}
                    >
                      削除
                    </Button>
                  </div>
                  {word.note ? (
                    <p className="mt-1 text-xs text-secondary-foreground">{word.note}</p>
                  ) : null}
                </div>
              ))}
            </div>
            {hasPagination ? (
              <div className="flex items-center justify-between border-t border-border/60 pt-3 text-sm">
                <p className="text-xs text-secondary-foreground">
                  {displayStart}-{displayEnd} / {words.length}
                </p>
                <div className="flex items-center gap-2">
                  <Button
                    type="button"
                    size="sm"
                    variant="outline"
                    onClick={() => setPage((value) => Math.max(1, value - 1))}
                    disabled={page === 1}
                  >
                    前へ
                  </Button>
                  <Button
                    type="button"
                    size="sm"
                    variant="outline"
                    onClick={() => setPage((value) => Math.min(totalPages, value + 1))}
                    disabled={page === totalPages}
                  >
                    次へ
                  </Button>
                </div>
              </div>
            ) : null}
          </>
        )}
      </CardContent>
    </Card>
  )
}
