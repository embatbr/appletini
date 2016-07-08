echo python -m unittest discover
python -m unittest discover

echo

echo cd app
cd app
echo gunicorn -b localhost:9000 app
gunicorn -b localhost:9000 app