# Sandwich shop app
Student no: 710069439

This is a demo app to be used by staff at the Sandwich Shop while taking orders from customers over the phone.
See the documentation in 'documents' folder for detailed information.

# Download and setup instructions

## Installing and running sandwich_shop app:
- Download zip file
- Extract all files into an accesible file location
- On your command line interface run:
   ``python -m pip install -e C:/Users/YOUR_DOWNLOAD_LOCATION/sandwich_shop``
- To launch the app run:
   ``python C:/Users/YOUR_DOWNLOAD_LOCATION/sandwich_shop/code/main.py``

## Running the app from within the package:
- Open the sandwich_shop folder in an IDE such as Visual Studio Code from the root directory 'sandwich_shop'
- Run the terminal and check that the file path ends with 'sandwich_shop'
- Install the package by running the command ``python -m pip install -e .``
- To launch the app run:
   ``python ../sandwich_shop/code/main.py``
- OR go to sub-directory 'code', go into the module main.py, run the file
- OR in a python file, add the following lines and run the file:
    ```
    from sandwich_shop.code import main
    main.run()
    ```
