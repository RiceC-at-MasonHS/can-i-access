# can-i-access
A few tools to check if you can get to websites, within your organization's web-filtering permissions.

There is a webpage that can check a number of URLs for you, but this can run into [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS) issues. 

A better option (with a little more struggle) is to run the [python-script](python-script/url-check.py) on a computer that is in the network. This will avoid CORS issues. 