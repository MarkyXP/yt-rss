<div align="center">
    <p align="center">

# YT-RSS ![](assets/icon_32.png)
[![Python](https://img.shields.io/badge/Python%203.14-3776AB?logo=python&logoColor=fff)](https://docs.astral.sh/uv/getting-started/installation/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions%20CI-2088FF?logo=github-actions&logoColor=white)](https://github.com/MarkyXP/artifactory_navigator) 
  </p>
</div>

---------
@Author(s): MarkyXP  

---------

## Summary:

## Documentation:
> https://github.com/mkdocstrings/mkdocstrings

### Backend structure
https://medium.com/the-pythonworld/how-to-structure-your-fastapi-projects-the-right-way-60969cbb224e

#### HTTP Requests
Consider https://github.com/jawah/niquests , maybe?

### Frontend structure
https://medium.com/@kaushalsinh73/fastapi-htmx-alpine-progressive-apps-without-spa-overhead-08b4ea9a2f5f

### Building for GHCR.io
> https://medium.com/@deepak1812002/get-started-with-github-ghcr-an-alternative-of-dockerhub-f7d5b2198b9a#:~:text=GHCR%20stands%20for%20Github%20Container,or%20organization%20account%20on%20GitHub.  
> https://medium.com/@shaliamekh/python-package-management-with-uv-for-dockerized-environments-f3d727795044



```
# Build the image
docker build -t ghcr.io/markyxp/yt-rss/yt-rss:20260406.01 .

# Push the image to GitHub Container Registry
docker push ghcr.io/markyxp/yt-rss/yt-rss:20260406.01
```

Output:
> [Image](ghcr.io/markyxp/yt-rss/yt-rss:latest)

# ToDo:
- [ ] Add Auth to adding/ removing channels
- [ ] Move update to a background thread (which checks if its already running. consider slowapi to rate limit)
- [ ] Move the version to match the tags
- [ ] Consider scraping the banner when adding the channel
- [ ] Finish moving the add channel logic to the new structure. 
