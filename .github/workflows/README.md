
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