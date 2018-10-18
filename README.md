# HashStagram

README written by [Audrey](https://github.com/ader003).

## Inspiration
We saw a paper ([HARRISON: A Benchmark on HAshtag Recommendation for Real-world Images in Social Networks, Park, et al.](https://arxiv.org/abs/1605.05054)) and re-implemented it.

## What it does
Given a picture, based on a models trained over 57,000 Instagram photos and their captions (gathered and preprocessed by grad students, return the top 5 hashtags (based on a set of the 1000 most popular hashtags on the platform) most reflective of the dataset.

## Team Members
- [Audrey Der](https://github.com/ader003)
  + Wrote the README, and did the frontend.
- [Calvin Ta](https://github.com/tacalvin)
  + Ran a GPU sweatshop.
  + Worked on the ResNet implementation, but it didn't work out.
- [Jerry Jiang](https://github.com/jjkjiang)
  + Admined for the team on Google Cloud Platform and wrote/set up a lot of the infrastructure involved, including webapp code.
  + Prototyped google cloud function use case, didn't work out :(
- [William Shiao](https://github.com/willshiao)
  + Worked primarily on implementing the Alexnet + VGG16 implementation.
  + Worked a little on the front end.

## How it was built
### 1. The Models
* [pytorch](https://github.com/pytorch)
* [AlexNet](https://github.com/pytorch/vision/blob/master/torchvision/models/alexnet.py)
* [VGG16](https://github.com/GKalliatakis/Keras-VGG16-places365)
* ~~a lot of black magic~~
* Google Cloud Platform
  * 2 x Deep Learning VM Image on Compute Engine Instance
    * PyTorch (new!)
    * 26 GB memory, 4 cores
    * GPUs: V100 x 1, K80 x 8
  * Storage
    * Exports trained models/weights to GCP Storage
* ~~80 days' worth of Passion Fruit flavored vitamin B12 in half the Deep Learning Team~~


### 2. The Web App
* Running on Flask, served with Gunicorn and Nginx on a GCP Compute Engine instance
  * 16 GB memory, 4 cores
* HTML, CSS, jQuery (just a little)
* The poster child of My First Bootstrap Website™ templates
* [filepond](https://github.com/pqina/filepond) by pqina
* A little bit of Photoshop and some Instagram mockup .psds


## Challenges we ran into
* Deep Learning by nature is black magic invoked by dancing around a fire under the full moon, neither of which the team had
* Half the ML team was allergic to the gym
* Running out of memory (and subsequent infighting within the ML team for memory)
* Originally wanted to use GCP serverless options, but size of model would take too long, needed to be preloaded for acceptable latencies
* Multi-threaded nature of web servers led to multiple copies of model being loaded, overwhelming memory limits  
  * Preloaded and shared as read-only across all threads to fix
* The web dev didn't know anything about web dev
* The intractable nature of the project 
* ~~ML is black magic~~
* ~~Deep Learning is black magic on steroids~~

## Accomplishments we're proud of
* The web dev has a nonzero number of skill points in web dev
* GCP Liaison has added to his ever growing knowledge base concerning cloud based services
* ~~We actually finished a project~~
* We finished a somewhat sizable project, given our history (or lack thereof)

## What we learned
* Planning projects beforehand is a good idea
* The most confusing thing about learning web dev was the fact that I was working with and integrating three different syntaxes I had no experience with on a platform I had no system knowledge about
* Code reviews are important and you should always be wary of particularly good results for precision and recall
* In our case, rapidly rising numbers in precision and recall (e.g. 0.005 --> 0.015 between batches) is Very Not Good™ and you should be skeptical

## What's next for HashStagram
* ~~A fire, full moon, and an ML team that's Dance 101 certified~~
* Scale it on GCP with load balancing
* Integration on mobile app

## Links
As included in the external form fields, the website can be found at [imehi.me](http://imehi.me/) (no longer true - the website has been taken down).
