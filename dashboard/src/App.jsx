import { useState, useEffect } from 'react'
import { supabase } from './supabaseClient'

export default function App() {
  const [session, setSession] = useState(null)

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

  async function signInWithGithub() {
    await supabase.auth.signInWithOAuth({
      provider: 'github',
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
          <p>Powered by Supabase</p>
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
    </>
  )
}