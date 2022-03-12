Search Microservice

This microservice is made with Flask 1.1.2
This RESTful API contains the following endpoints:

GET /searchComics

    @params:
        -search: Optional. This parameters is a character name or a comic title
        -character: Required. This parameter must be either 1 or 0. If 1, indicates that the search params is a character name
        -comic: Required. This parameter must be either 1 or 0. If 1, indicates that the search params is a comic title

    @notes:
        If no params is given, the result will be an array of characters alphabetically arranged 
        Params character and comic cannot be the same. If character is 1, comic must be 0 and vice versa

How to run

This application is allocated in Docker Hub, so you can pull by typing this command:
    - docker pull alejandrorv/search-microservice:latest

Once pulled, you need to run the next command
    - docker run -it --name search -p 5000:5000 alejandrorv/search-microservice

You can change the first option for the local port if it causes any conflict
Flag --name is also optional

To test the endpoint you can make a request to the next url:
    - http://0.0.0.0:5000/searchComics?search=3-D Man&character=1&comic=0
