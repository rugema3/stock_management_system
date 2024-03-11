# Run gunicorn in the background. 
gunicorn -w 2 -b 0.0.0.0:8500 -D app:app

