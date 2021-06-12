import { useState } from "react"

function PasswordLoginForm() {
  const [ emailValue, setEmailValue ] = useState('')
  const [ passwordValue, setPasswordValue ] = useState('')
  const [ inProgress, setInProgress ] = useState(false)
  const [ error, setError ] = useState(null)

  const handleSubmit = async (event) => {
    event.preventDefault()
    console.debug(`Form submitted: ${emailValue} ${passwordValue}`)
    setInProgress(true)
    try {
      const response = await fetch('/api/auth/password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: emailValue,
          password: passwordValue,
        }),
      })
      if (response.status === 200) {
        const reply = await response.json()
        if (reply.ok) {
          window.location = '/dashboard'
        } else {
          if (reply.code === 'invalid_credentials') {
            setError('Invalid credentials')
          } else {
            setError('Unknown error')
          }
        }
      }
    } catch (err) {
      setError(`Error: ${err}`)
    } finally {
      setInProgress(false)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <h2>Sign in using password</h2>
      {error && (
        <p>
          <strong style={{ color: 'red' }}>{error}</strong>
        </p>
      )}
      <p>
        <input
          type='text'
          name='email'
          placeholder='Your e-mail'
          value={emailValue}
          onChange={event => setEmailValue(event.target.value)}
          disabled={inProgress}
        />
      </p>
      <p>
        <input
          type='password'
          name='password'
          placeholder='Your password'
          value={passwordValue}
          onChange={event => setPasswordValue(event.target.value)}
          disabled={inProgress}
        />
      </p>
      <p>
        <input
          type='submit'
          value='Sign in'
          disabled={inProgress}
        />
      </p>
    </form>
  )
}

export default PasswordLoginForm
