Firewatch
=========

HTTP monitoring tool – as simple as possible, devops &amp; integration &amp; automation friendly

<img src="https://messa-shared-files.s3-eu-west-1.amazonaws.com/2021/20210207-firewatch-screenshot.png" width=400>


Tech stack
----------

Frontend:

- [Next.js](https://nextjs.org/)
- [React](https://reactjs.org/)
- [SWR](https://swr.vercel.app/)

Backend:

- Python
- [Aiohttp](https://docs.aiohttp.org/en/stable/web.html)

Configuration: one YAML file

Authentication: Google OAuth2 sign-in

No database :)
This thing is supposed to run in a single long-term process, it holds all data in the memory – which
basically means only short-term stats and current + recent alerts.
I think this approach has more advantages than downsides for this kind of project.

Deployment: build Docker image and deploy wherever Docker images can be deployed
