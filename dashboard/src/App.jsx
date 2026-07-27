import { useState, useEffect } from 'react'
import { supabase } from './supabaseClient'

export default function App() {
  const [session, setSession] = useState(null)

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
          <button>Sign in with GitHub</button>
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
    <div>
    </div>
  )
}