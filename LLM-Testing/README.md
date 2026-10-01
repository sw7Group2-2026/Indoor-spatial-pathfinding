# Prelim info

This is my PBI with a bit of information before I go into it.

I looked up a few different solutions and found that a lot of people on Reddit liked Cloudflare, and it was also free. I also considered Gemini, but this seemed a bit more annoying to implement.

This may require some accounts, but it seems like we have a fair amount of tokens as long as we don't loop while connected to the API.

I've made a longer document below about setting it up just for reference.

I've used **uv** to manage the Python environment and dependencies locally. This means we don't need to manage python vm too much, but we need to discuss in group a better way to do this.

---

# Cloudflare AI Workers Setup Guide

This setup requires a **Cloudflare API key** and **Cloudflare Account ID**.

We have a fair amount of requests available each day, so we can use mine (Peter's), which we will distribute safely.

If you wish to use your own API key, follow the guide at the **bottom of this document**.

Below is a guide on how to run the code and what the different parts mean.

---

## How It Works

The `main.py` file contains a simple setup that uses the **LLM API class**.

This class uses environment variables to set up the connection with an LLM. It does all of this automatically when the class is initialized.

All you have to do is provide which AI model you want to use.

There are quite a few models available, but so far I've only used **Llama**.

You can find the available models here:

https://developers.cloudflare.com/workers-ai/models/

---

## Running the Code

The project uses **uv** to manage Python and the project's dependencies.

If you don't already have `uv` installed, follow the official installation guide:

https://docs.astral.sh/uv/getting-started/installation/

Once `uv` is installed, just write uv run llm-testing and it should work.