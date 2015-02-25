# django-cymon-firewall
Block malicious IP sources using [Cymon.io](http://cymon.io/) API.

## Usage
To use this library, and force SSL across your Django site, all you need to do is modify your ``settings.py`` file, 
and prepend ``djcymon.middleware.CymonFirewallMiddleware`` to your ``MIDDLEWARE_CLASSES`` setting:

```python
# settings.py

MIDDLEWARE_CLASSES = (
    'djcymon.middleware.CymonFirewallMiddleware',
    # ...
)
```


### Note
Make sure ``djcymon.middleware.CymonFirewallMiddleware`` is the first middleware
class listed, as this will ensure that if a malicious IP makes a request, 
it will dropped before any actual processing happens.


## Contributing

If you'd like to improve this library, please send me a pull request! I'm happy
to review and merge pull requests.

The standard contribution workflow should look something like this:

- Fork this project on Github.
- Make some changes in the master branch (*this project is simple, so no need to
  complicate things*).
- Send a pull request when ready.


