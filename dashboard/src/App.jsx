import { useState, useEffect } from 'react'
import { supabase } from './supabaseClient'

export default function App() {
  const [session, setSession] = useState(null)

  if (!session) {
    return (
      <div>
        <h1>Deprecated Dependency Auditor</h1>
        <button>Sign in with GitHub</button>
      </div>
    )
  }

  return (
    <div>
    </div>
  )
}