Frontend – JavaScript app
=========================

This is a fairly standard application implemented using:

- [React](https://reactjs.org/)
- [Next.js](https://nextjs.org/)
- [SWR](https://swr.vercel.app/)


Development mode
----------------

Run `npm run dev`.

Backend API is proxied via configuration `next.config.js`.


Production mode
---------------

In production only static export version is used.
It is served directly from the Python backend as set of static files.

Create the export using `npm run export`.
