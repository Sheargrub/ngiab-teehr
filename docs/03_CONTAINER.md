# Container Management

STUB

5. Then checkout main and pull the new changes, and push your tag:
```bash
git checkout main
git pull
git tag -a v0.x.x -m "version 0.x.x"
git push origin v0.x.x
```

This will trigger a `github action` to build and push the image with your tag, and the `latest` tag, to the AWI CIROH registry.

To build and push locally:
```
docker build -t awiciroh/ngiab-teehr:<tag name> .
docker push awiciroh/ngiab-teehr:<tag name>
```

Now you can specify the image tag in the guide.sh script.