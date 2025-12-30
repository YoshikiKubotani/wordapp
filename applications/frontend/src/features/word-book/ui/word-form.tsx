import { type FormEvent, useState } from 'react'
import { useSetAtom } from 'jotai'
import { registerWordAtom, type WordDraft } from '@/features/word-book'
import { Button } from '@/shared/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/shared/ui/card'
import { Input } from '@/shared/ui/input'
import { Label } from '@/shared/ui/label'
import { Textarea } from '@/shared/ui/textarea'

type FormState = WordDraft

export function WordForm() {
  const registerWord = useSetAtom(registerWordAtom)
  const [form, setForm] = useState<FormState>({
    term: '',
    meaning: '',
    note: '',
  })
  const [feedback, setFeedback] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const updateField = (field: keyof FormState) => (value: string) => {
    setForm((prev) => ({ ...prev, [field]: value }))
    setFeedback(null)
    setError(null)
  }

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!form.term.trim() || !form.meaning.trim()) {
      setError('Please add both the word and its meaning.')
      return
    }

    registerWord(form)
    setForm({ term: '', meaning: '', note: '' })
    setFeedback('Saved! Add another word or jump into practice.')
  }

  return (
    <Card className="h-full backdrop-blur">
      <CardHeader>
        <CardTitle>Register a word</CardTitle>
        <CardDescription>
          Keep the deck fresh—adding a word with the same spelling updates its meaning.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form className="space-y-4" onSubmit={handleSubmit}>
          <div className="space-y-2">
            <Label htmlFor="term">Word</Label>
            <Input
              id="term"
              placeholder="meticulous"
              value={form.term}
              onChange={(event) => updateField('term')(event.target.value)}
              autoComplete="off"
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="meaning">Meaning</Label>
            <Input
              id="meaning"
              placeholder="Showing great attention to detail"
              value={form.meaning}
              onChange={(event) => updateField('meaning')(event.target.value)}
              autoComplete="off"
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="note">Memory hook (optional)</Label>
            <Textarea
              id="note"
              placeholder="e.g. Her notes were meticulous—every comma was intentional."
              value={form.note}
              onChange={(event) => updateField('note')(event.target.value)}
            />
          </div>
          {error ? <p className="text-sm font-medium text-destructive">{error}</p> : null}
          {feedback ? <p className="text-sm text-foreground">{feedback}</p> : null}
          <div className="flex items-center gap-2">
            <Button type="submit" className="flex-1">
              Save word
            </Button>
            <Button
              type="button"
              variant="ghost"
              onClick={() => setForm({ term: '', meaning: '', note: '' })}
            >
              Clear
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  )
}
