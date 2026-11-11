# Running QR Program

[← Back to project README](../README.md)

## QR Program

Open [The qr program](https://qr.io/) 

Run the program. The python file for it can be found under device, called Mediator.py

To run it in docker, first use docker compose build. Then run using this command: docker compose run --rm py -m device.concrete_mediator

Use the link from Running on public URL

place in enter Website
add this to the end /?floor=2&x=2&y=2

and when you now scan the qr code it will give the website with that info
run a subit and it will print the info in the otput on the pc.