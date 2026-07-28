import { useState, useEffect } from 'react'
import { supabase } from './supabaseClient'

const WORKFLOW_SNIPPET = `name: Deprecation Audit

on:
  pull_request:
    types: [opened, synchronize, reopened]

permissions:
  contents: read
  pull-requests: write

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run deprecation auditor
        uses: dxfeng/deprecation-auditor/scanner@main
        with:
          manifest-path: requirements.txt
`

export default function App() {
  const [session, setSession] = useState(null)
  const [repos, setRepos] = useState([])
  const [trackedRepoIds, setTrackedRepoIds] = useState(new Set())

  useEffect(() => {
    // Code fragmented from https://supabase.com/docs/guides/auth/quickstarts/react

    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session)
    })

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session)
    })

    return () => subscription.unsubscribe()
  }, [])

  useEffect(() => {
    if (!session) {
      setRepos([])
      return
    }

    // Public repos only -- no token needed, and the username is ordinary
    // profile metadata Supabase persists across sessions (unlike
    // provider_token, which it deliberately does not)
    const username = session.user.user_metadata.user_name
    fetch(`https://api.github.com/users/${username}/repos?per_page=100`)
      .then((res) => res.json())
      .then((data) => setRepos(Array.isArray(data) ? data : []))
  }, [session])

  useEffect(() => {
    if (!session) {
      setTrackedRepoIds(new Set())
      return
    }

    supabase
      .from('repos')
      .select('github_repo_id')
      .eq('user_id', session.user.id)
      .then(({ data, error }) => {
        if (error) {
          console.error(error)
          return
        }
        setTrackedRepoIds(new Set(data.map((r) => r.github_repo_id)))
      })
  }, [session])

  async function signInWithGithub() {
    await supabase.auth.signInWithOAuth({
      provider: 'github',
    })
  }

  async function trackRepo(repo) {
    const { error } = await supabase.from('repos').insert({
      user_id: session.user.id,
      github_repo_id: repo.id,
      repo_name: repo.full_name,
    })

    if (error && error.code !== '23505') {
      console.error(error)
      return
    }

    setTrackedRepoIds((prev) => new Set(prev).add(repo.id))
  }

  async function untrackRepo(repo) {
    const { error } = await supabase
      .from('repos')
      .delete()
      .eq('user_id', session.user.id)
      .eq('github_repo_id', repo.id)

    if (error) {
      console.error(error)
      return
    }

    setTrackedRepoIds((prev) => {
      const next = new Set(prev)
      next.delete(repo.id)
      return next
    })
  }

  if (!session) {
    return (
      <>
        <div>
          <h1>Deprecated Dependency Auditor</h1>
        </div>
        <div>
          <svg height="48" width="48" aria-hidden="true">
            <use href="/icons.svg#github-icon"></use>
          </svg>
        </div>
        <div>
          <button onClick = {signInWithGithub}>Sign in with GitHub</button>
        </div>
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
          <h3>Created by Daniel Feng</h3>
        </div>
        <div>
          <p>Powered by Supabase & Vercel</p>
        </div>
      </>
    )
  }

  return (
    <>
      <div>
        <h1>Dashboard</h1>
        <p>Logged in as: {session.user.email}</p>
        <button onClick={() => supabase.auth.signOut()}>Sign Out</button>
      </div>
      <div style={{ display: 'flex' }}>
        <div style={{ flex: 1 }}>
          <h2>Your repos</h2>
          <ul>
            {repos.map((repo) => (
              <li key={repo.id}>
                {repo.full_name}{' '}
                {trackedRepoIds.has(repo.id) ? (
                  <>
                    <button onClick={() => untrackRepo(repo)}>Untrack</button>
                  </>
                ) : (
                  <button onClick={() => trackRepo(repo)}>Track</button>
                )}
              </li>
            ))}
          </ul>
        </div>
        <div style={{ flex: 1, textAlign: 'left', fontSize: '14px' }}>
          <h2>Setup instructions:</h2>
          <p>
            Add this workflow to a tracked repo at{' '}
            <code>.github/workflows/deprecation-audit.yml</code>:
          </p>
          <pre>{WORKFLOW_SNIPPET}</pre>
          <button onClick={() => navigator.clipboard.writeText(WORKFLOW_SNIPPET)}>
            Copy
          </button>
        </div>
      </div>
    </>
  )
}