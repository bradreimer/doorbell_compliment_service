# Tests for Doorbell Compliment Service

## Manual Test

Run the curl script:

    ./curl_test.sh sample.jpg

Replace `sample.jpg` with any image.

## Automated Test

## Testing the Python code

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
pytest && pylint app tests
```
