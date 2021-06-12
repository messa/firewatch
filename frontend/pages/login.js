import React from 'react'
import useSWR from 'swr'
import Layout from '../components/Layout'
import PasswordLoginForm from '../components/PasswordLoginForm'
import { fetcher, swrOptions } from '../util/swr'

function LoginPage() {
  const { data, error } = useSWR(`/api/auth/login-methods`, fetcher, swrOptions)
  return (
    <Layout>
      <h1>Login</h1>
      {error && <p style={{ color: 'red' }}>Failed to load</p>}
      {data && (
        <div>
          {data.login_methods.google || 1 && (
            <p><a href='/api/auth/google' className='button'>Sign in via Google</a></p>
          )}
          {data.login_methods.dev || 1 && (
            <p><a href='/api/auth/dev' className='button'>Development login</a></p>
          )}
          {data.login_methods.password && (
            <PasswordLoginForm />
          )}
        </div>
      )}
    </Layout>
  )
}

export default LoginPage
