import { useState } from 'react'
import { supabase } from './supabaseClient'

function App() {
  const [session, setSession] = useState(null)


  if (!session) {
    return (
      <div>
        <h1>Deprecated Dependency Auditor</h1>
        <button>Sign in with Github</button>
      </div>
    )
  }

  return (
    <>
    </>
  )
}

export default App
