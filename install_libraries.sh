cd python_libraries

# Clone libraries
git clone https://github.com/pytorch/pytorch.git
git clone https://github.com/pallets/flask.git
git clone https://github.com/sloria/TextBlob.git
git clone https://github.com/RaRe-Technologies/gensim.git
git clone https://github.com/nateshmbhat/pyttsx3.git
git clone https://github.com/opencv/opencv-python.git

# Install each library
cd pytorch && python setup.py install && cd ..
cd flask && python setup.py install && cd ..
cd sloria && python setup.py install && cd ..
cd gensim && python setup.py install && cd ..
cd pyttsx3 && python setup.py install && cd ..
cd opencv-python && python setup.py install && cd ..