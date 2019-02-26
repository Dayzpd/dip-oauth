# dip-oauth
A simple class for including Oauth into Python applications.

There does exist well established Oauth packages for Python, but I prefer to keep it simple. I've used this in previous Flask applications 
multiple times and prefer it over alternatives such as Flask Dance. The Oauth 2.0 standard requires certain fields for Auth Keys, Token Keys, 
and Refresh Keys, but many services require extra information. However, regardless of which fields any given service requires, providing
any of the functions within the DipOauth class with a dictionary and then url encoding the data works just fine. In the case that 
a request fails, an error is thrown which provides useful information such as any potential missing fields.
