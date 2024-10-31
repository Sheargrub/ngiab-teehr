# ngiab-teehr
A repository for coupling TEEHR with Nextgen-In-A-Box (NGIAB) simulation output.

Warning: This code is highly experimental!

The `example_guide.sh` script demonstrates running a TEEHR evaluation (see `scripts/teehr_ngen.py`) on NGIAB output.

#### To build and push the TEEHR image to the AWI CIROH registry

```bash
docker build -t awiciroh/ngiab-teehr:<tagname> .

# To login to the registry, you'll need the password
docker login -u awiciroh
<password>

docker push awiciroh/ngiab-teehr:<tagname>
```

**Note**: Currently the `example_guide.sh` script is hardcoded to always pull the TEEHR "latest" image from the AWI CIROH registry.