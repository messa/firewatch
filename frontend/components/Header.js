import React from 'react'
import Link from 'next/link'
import useSWR from 'swr'
import { fetcher, swrOptions } from '../util/swr'
import styles from './Header.module.css'


function Header({ children }) {
  const { data, error } = useSWR('/api/user', fetcher)
  const user = data && data.user
  return (
    <div className={styles.header}>
      <div className='container'>
        <div className={styles.headerContent}>

          <div className={styles.siteTitle}>
            <Link href='/dashboard'>
              <a style={{ color: 'white', textDecoration: 'none' }}>
                Firewatch
              </a>
            </Link>
          </div>

          <div className={styles.userInfo}>
            {data && (
              !user ? (
                <span>
                  <Link href='/login'><a className='button'>Sign in</a></Link>
                </span>
              ) : (
                <span>
                  👤 {user.email}{' '}
                  <a href='/api/auth/logout' className='button'>Sign out</a>
                </span>
              )
            )}
          </div>

        </div>
      </div>
    </div>
  )
}

export default Header
