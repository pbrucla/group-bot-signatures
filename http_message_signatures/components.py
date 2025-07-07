from urllib.parse import urlparse, parse_qs

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

def query_param(request, name):
    # handles '@query-param';name="param"
    #parse request.url  and return first value of ?param
    # TODO: impl query param extraction
    return ""
