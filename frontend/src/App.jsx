import { useState, useEffect } from 'react'
import Header        from './components/Header.jsx'
import BottomNav     from './components/BottomNav.jsx'
import ProjectSelect from './components/ProjectSelect.jsx'
import StageSelect   from './components/StageSelect.jsx'
import StageForm     from './components/StageForm.jsx'
import Dashboard     from './components/dashboard/Dashboard.jsx'
import LoginPage     from './components/LoginPage.jsx'
import { clearSession, isLoggedIn } from './auth.js'

export default function App() {
  const [authed,  setAuthed]  = useState(isLoggedIn)
  const [mode,    setMode]    = useState('operator') // 'operator' | 'dashboard'
  const [step,    setStep]    = useState('project')  // 'project'  | 'stage' | 'form'
  const [project, setProject] = useState(null)
  const [stage,   setStage]   = useState(null)

  // Handle token expiry from any fetch call
  useEffect(() => {
    const onUnauthorized = () => setAuthed(false)
    window.addEventListener('rp:unauthorized', onUnauthorized)
    return () => window.removeEventListener('rp:unauthorized', onUnauthorized)
  }, [])

  if (!authed) {
    return <LoginPage onLogin={() => setAuthed(true)} />
  }

  const handleSelectProject = (p) => { setProject(p); setStep('stage') }
  const handleSelectStage   = (s) => { setStage(s);   setStep('form')  }

  const handleBack = () => {
    if (step === 'form')  { setStage(null);                   setStep('stage')   }
    if (step === 'stage') { setProject(null); setStage(null); setStep('project') }
  }

  const handleLogout = () => {
    clearSession()
    setAuthed(false)
  }

  const handleNewStage   = () => { setStage(null); setStep('stage') }
  const handleNewProject = () => { setProject(null); setStage(null); setStep('project') }

  const isDash  = mode === 'dashboard'
  const canBack = !isDash && step !== 'project'

  return (
    <div className="app">
      <Header
        step={step}
        onBack={canBack ? handleBack : null}
        title={isDash ? 'Dashboard' : null}
        onLogout={isDash ? handleLogout : undefined}
      />

      <main className="main">
        {isDash ? (
          <Dashboard />
        ) : (
          <>
            {step === 'project' && <ProjectSelect onSelect={handleSelectProject} />}
            {step === 'stage'   && <StageSelect project={project} onSelect={handleSelectStage} />}
            {step === 'form'    && (
              <StageForm
                project={project}
                stage={stage}
                onNewStage={handleNewStage}
                onNewProject={handleNewProject}
              />
            )}
          </>
        )}
      </main>

      <BottomNav active={mode} onChange={setMode} />
    </div>
  )
}
