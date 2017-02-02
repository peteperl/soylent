# soylent

Get soybean production and rainfall for any county in the USA

## Details

All of the code logic is in the 'ComputeApi' directory.  

My server is here: http://54.144.251.53/  
  
You can input any county in the USA and get soybean production for 2015 and today's rainfall.  
  
You can lookup any county's soybean production and rainfall: http://54.144.251.53/lookup  
  
The framework for the backend is a basic Flask deployment that I built for a few projects.  
  
  
## Comments
  
Problem:  
Create a service that shows today's total rainfall for counties that produce a lot of soybeans.  
  
Solutions:  
  
I built a full stack project. My focus was on back-end, but I built a front-end for usability testing and learning.  
    
Technical choices made during the project:  
My priorities were to compartmentalize the code for changeability, reusability, and scalability. I preload small (few KB) files into memory via functions. This allows for replaceability with a function that goes into a cache.  
  
Challenges, tradeoffs, or compromises faced during the project:  
The main challenges had to do with the learning curve for getting data from the external APIs. Also, caching needs to be built in to deal with the slowness of the APIs. This is especially true for the rain API as it seems each request for each county is independent.  
  
What I learned along the way:  
This was my first time building a front-end to an API.  
  
If you had more time, I would do the following:  
Break up some of the functional components into autonomous components.  
Build a proper caching system. I would probably use Redis for its premade data structures. The hashes make for easy keying that is similar to code data structures.  
Delving into a nicer front-end would also be fun.  
  
Scalability is addressed with the use compartmentalization and stateless requests.  This allows multiple instances to be replicated.  
  
There is some basic error handling for bad inputs (State and County). There is additional error handling for KeyErrors and communicating with any outside API as it may be unreachable.  
  
  
## Setup

Start an instance (Ubuntu 16.04) and open the HTTP ports.  

ssh into the instance.  

Download the repo and unzip (you may need to: sudo apt-get install unzip).  
Or git clone the repo.  

If you are on AWS you need to add the following line in '/etc/hosts' for you private IP:  

    xx.xx.xx.xx ip-xx-xx-xx-xx

You must now have a 'soylent' directory in your home directory.  

Go into the repo directory:  

    cd soylent

In the compute-api.conf file, change the ServerName to your domain or cloud server's IP address:  

    vi compute-api.conf

Install the necessary dependencies and setup by running:  

    ./setup_node
