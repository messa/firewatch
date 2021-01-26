import React from 'react'
import styles from './Header.module.css'


function Header({ children }) {
  return (
    <div className={styles.header}>
      <div className='container'>
        <div className={styles.siteTitle}>
          Firewatch
        </div>
      </div>
    </div>
  )
}

export default Header
