from urllib.parse import urlparse, parse_qs     # for parsing urls & query strings

# fixed derived-component extractors
DERIVED = {
   "@method"        : lambda r: r.method,
   "@scheme"        : lambda r: urlparse(r.url).scheme,
   "@authority"     : lambda r: urlparse(r.url).netloc,
   "@target-uri"    : lambda r: r.url,
   "@path"          : lambda r: urlparse(r.url).path or "/",
   "@query"         : lambda r: "?" + urlparse(r.url).query if urlparse(r.url).query else "",
   "@request-target": lambda r: (urlparse(r.url).path or "/")
                       + (("?" + urlparse(r.url).query) if urlparse(r.url).query else ""),
}

#parses request.url  and return first value of ?param
def query_param(request, name):   # handles '@query-param';name="param"
   q_params = parse_qs(urlparse(request.url).query)   # dict returned
   val = q_params.get(name, "invalid")  # returns invalid if name (key) not found
   return val



#---------------------------- Testing --------------------------------
class MockRequest:
   def __init__(self, url):
       self.url = url


r = MockRequest("https://www.example.com/product?affiliate_id=56789")
print(query_param(r, "affiliate_id"))   # prints 56789
print(query_param(r, "name"))   # prints invalid