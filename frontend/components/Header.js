import React from 'react'
import Link from 'next/link'
import styles from './Header.module.css'


function Header({ children }) {
  return (
    <div className={styles.header}>
      <div className='container'>
        <div className={styles.siteTitle}>
          <Link href='/'>
            <a style={{ color: 'white', textDecoration: 'none' }}>
              Firewatch
            </a>
          </Link>
        </div>
      </div>
    </div>
  )
}

export default Header
