# sentipharos

## If pip packages need to be updated or added new packages

```bash
pip install pip-tools
pip-compile --strip-extras
pip install -r requirements.txt
```
