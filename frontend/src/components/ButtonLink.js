import React from 'react'
import Link from 'next/link'
import Button from '@material-ui/core/Button'


export const ButtonLink = ({ className, lhref, hrefAs, children, prefetch }) => (
  <Link href={lhref} as={hrefAs} prefetch>
    <a className={className}>
      {children}
    </a>
  </Link>
);
